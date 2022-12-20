import sys, time,atexit, ftd2xx as ftd
from numpy import true_divide

FTDI_TIMEOUT = 1000
FTDI_VID = 0x0403   # Default FTDI FT4232H vendor ID
FTDI_PID = 0x6011   # Default FTDI FT4232H product ID

MSBFIRST = 0
LSBFIRST = 1

_REPEAT_DELAY = 4

'''
Commands found here:
http://www.ftdichip.com/Support/Documents/AppNotes/AN_108_Command_Processor_for_MPSSE_and_MCU_Host_Bus_Emulation_Modes.pdf
'''

class FT4232H():
    def __init__(self,vid=FTDI_VID, pid=FTDI_PID, serial=None,index=0):
        #open index 0,1,2,3 for each channel. For MPSSE: 0=channel A, 1=channel B
        self.d=ftd.open(index)
        atexit.register(self.dclose)
        if not self.d:
            print("Can't open device")
        #set device timouts
        self.d.setTimeouts(FTDI_TIMEOUT, FTDI_TIMEOUT)
        #set usb max bits that can be sent
        self.d.setUSBParameters(65535,65535)
        #Enable MPSSE(SPI)
        self._mpsse_enable()
        #Send Bad Command, recieve bad command response
        self._mpsse_sync()
        rbuffer = self.d.getQueueStatus()
        #cleare recieve buffer
        if (rbuffer>0 and self.d.status ==1):
            s=self.dreadarr(rbuffer)
        #set all pins as input
        #x80 is the command, following bits indicate level, direction
        self.d.write('\x80\x00\x00')
        self._direction = 0x00
        self._level = 0x00
    #close ftdi channel
    def dclose(self):
        self.d.close()
    #print channel info
    def info(self):
        print(self.d.getDeviceInfo())
    #set bitmode
    def set_bitmode(self, bits, mode):
        return self.d.setBitMode(bits, mode)
    #Read byte into bytearray
    def dread(self,nbytes):
        s = self.d.read(nbytes)
        return s
    #Read byte data into list of integers
    def dreadarr(self,nbytes):
        s = self.d.read(nbytes)
        return [ord(c) for c in s] if type(s) is str else list(s)
    #Write list of integers as byte data
    def dwrite(self,data):
        s = str(bytearray(data)) if sys.version_info<(3,) else bytes(data)
        # print("write:",s)
        return self.d.write(s)
    #Set SPI clock rate
    def set_spi_clock(self,hz):
        div = int((12000000/(hz*2))-1)
        self.dwrite((0x86,div%256,div//256))
    #enable internal DI & DO connection, used for testing sending and recieving functionality
    def loopback(self):
        self.d.write('\x84')
    #reset mode then set to MPSSE
    def _mpsse_enable(self):
        self.set_bitmode(0,0)
        self.set_bitmode(0,2)
    #sends bad command xAB then checks for response xFA followed by the bad command xAB
    def _mpsse_sync(self, max_retries=10):
        self.d.write('\xAB')
        tries=0
        sync=False
        while not sync:
            data = self.dreadarr(2)
            if data == [250,171]:
                sync=True
            tries+=1
            if tries >= max_retries:
                raise RuntimeError('Could not synchornize with FT4232H')
    #returns the levels of GPIO pins
    def mpsse_read_gpio(self):
        self.d.write('\x81')
        return self.dreadarr(2)
    #returns the command to write level and direction to GPIO
    def mpsse_gpio(self):
        level_low = self._level & 0xFF
        dir_low = self._direction & 0xFF
        return (0x80, level_low, dir_low)
    #writes the level and direction to GPIO Pins
    def mpsse_write_gpio(self):
        self.dwrite(self.mpsse_gpio())
    #Sets the class variable of direction and level to user input
    def _setup_pin(self, pin, mode):
        if pin<0 or pin>7:
            raise ValueError('Pin must be between 0 and 7 (inclusive).')
        if mode not in ("input", "output"):
            raise ValueError('Mode must be in "input" or "output"')
        if mode == "input":
            self._direction &= ~(1<<pin)&0xFF
            self._level &= ~(1<<pin)&0xFF
        else:
            self._direction |= (1<<pin)&0xFF
    #writes the level and directionto a pin
    def setup(self,pin,mode):
        self._setup_pin(pin,mode)
        self.mpsse_write_gpio()
    #writes the level and directionto multiple pins
    def setup_pins(self,pins,values={},write=True):
        for pin, mode in iter(pins.items()):
            self._setup_pin(pin,mode)
        for pin, value in iter(values.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()
    #set the level of a pin to user input
    def _output_pin(self, pin, value):
        if value:
            self._level |= (1<<pin)&0xFF
        else:
            self._level &= ~(1<<pin)&0xFF
    #writes the level of a pin
    def output(self, pin, value):
        if pin < 0 or pin > 7:
            raise ValueError('Pin must be between 0 and 7 (inclusive).')
        self._output_pin(pin, value)
        self.mpsse_write_gpio()
    #writes the level of multiple pins
    def output_pins(self, pins, write=True):
        for pin, value in iter(pins.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()
    #set a pin as input
    def input(self, pin):
        return self.input_pins([pin])[0]
    #set pins to input
    def input_pins(self, pins):
        if [pin for pin in pins if pin < 0 or pin > 7]:
            raise ValueError('Pin must be between 0 and 7 (inclusive).')
        _pins = self.mpsse_read_gpio()
        return [((_pins >> pin) & 0x01) == 1 for pin in pins]

class SPI(object):
    def __init__(self, ftdi, cs=None, max_speed_hz=1000000, mode=0, bitorder = MSBFIRST):
        self.ftdi=ftdi
        #set selected cs pin as output and pulls it high (cs on MCP is active low)
        if cs is not None:
            self.ftdi.setup(cs,"output")
            self.ftdi.output(cs,1)
        self._cs=cs
        #set clock speed of ftdi
        self.set_clock_hz(max_speed_hz)
        #sets mode of ftdi, write on positive or negative edge of clk, read on positive or negative edge of clk, and clock starting level
        self.set_mode(mode)
        #sets clocked data out and in as MSB first or LSB first
        self.set_bit_order(bitorder)
        #flushes recieve buffer
        rbuffer = self.ftdi.d.getQueueStatus()
        if (rbuffer>0 and self.ftdi.d.status ==1):
            s=self.ftdi.dreadarr(rbuffer)
    #command to pull cs low
    def _assert_cs(self):
        if self._cs is not None:
            self.ftdi.output(self._cs,0)
    #command to pull cs high
    def _deassert_cs(self):
        if self._cs is not None:
            self.ftdi.output(self._cs,1)
    #set spi clock
    def set_clock_hz(self, hz):
        self.ftdi.set_spi_clock(hz)
    #set read write to positive or negative edge and base clock level
    def set_mode(self, mode):
        if mode<0 or mode>3:
            raise ValueError('Mode must be a value 0,1,2, or 3')
        if mode == 0:
            self.write_clock_ve = 1
            self.read_clock_ve = 0
            clock_base = 0
        elif mode ==1:
            self.write_clock_ve = 0
            self.read_clock_ve = 1
            clock_base = 0
        elif mode==2:
            self.write_clock_ve = 1
            self.read_clock_ve = 0
            clock_base = 1
        elif mode==3:
            self.write_clock_ve = 0
            self.read_clock_ve = 1
            clock_base = 1
            #sets CLK,DO,CS as outputs and DI as input, pulls clock low and cs high
        self.ftdi.setup_pins({0:"output",1:"output",2:"input",3:"output"},{0:clock_base,3:1})
    #set msb or lsb first
    def set_bit_order(self, order):
        if order == MSBFIRST:
            self.lsbfirst = 0
        elif order == LSBFIRST:
            self.lsbfirst = 1
        else:
            raise ValueError('Order must be MSBFIRST or LSBFIRST.')
    #SPI write command
    def write(self,data):
        #changes command in accordance to mode and bitorder
        command = 0x10|(self.lsbfirst<<3)|self.write_clock_ve
        length = len(data)-1
        len_low = length&0xFF
        self._assert_cs()
        #writes command, length low bit(no high bit on ft4232h)
        self.ftdi.dwrite((command,len_low,0))
        #clocks out data
        self.ftdi.dwrite(data)
        self._deassert_cs()
    def read(self,length):
        #changes command in accordance to mode and bitorder
        command = 0x20|(self.lsbfirst<<3)|(self.read_clock_ve<<2)
        len_low = (length-1)&0xFF
        self._assert_cs()
        #writes command, length of data to read, and flushes buffer command
        self.ftdi.dwrite((command,len_low,0,0x87))
        self._deassert_cs()
        return self.ftdi.dread(length)
    def transfer(self,data):
        #changes command in accordance to mode and bitorder
        command = 0x30|(self.lsbfirst<<3)|(self.read_clock_ve<<2)|self.write_clock_ve
        length = len(data)
        len_low = (length-1)&0xFF
        #flushes recieve buffer
        rbuffer = self.ftdi.d.getQueueStatus()
        if (rbuffer>0 and self.ftdi.d.status ==1):
            s=self.ftdi.dreadarr(rbuffer)
        #pulls cs low
        self._assert_cs()
        #writes command and length of data to write
        self.ftdi.dwrite((command,len_low,0))
        #writes data
        self.ftdi.dwrite(data)
        #send command to flush buffer to pc
        self.ftdi.d.write('\x87')
        #pull cs high
        self._deassert_cs()
        #read data
        return (self.ftdi.dread(length))