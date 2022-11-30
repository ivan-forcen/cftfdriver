import sys, time,atexit, ftd2xx as ftd
from numpy import true_divide

FTDI_TIMEOUT = 1000
FTDI_VID = 0x0403   # Default FTDI FT4232H vendor ID
FTDI_PID = 0x6011   # Default FTDI FT4232H product ID

MSBFIRST = 0
LSBFIRST = 1

_REPEAT_DELAY = 4

class FT4232H():
    def __init__(self,vid=FTDI_VID, pid=FTDI_PID, serial=None):
        self.d=ftd.open(0)
        atexit.register(self.dclose)
        if not self.d:
            print("Can't open device")
        self.d.setTimeouts(FTDI_TIMEOUT, FTDI_TIMEOUT)
        self.d.setUSBParameters(65535,65535)
        self._mpsse_enable()
        self._mpsse_sync()
        rbuffer = self.d.getQueueStatus()
        if (rbuffer>0 and self.d.status ==1):
            s=self.dread(rbuffer)
        self.d.write('\x80\x00\x00')
        self._direction = 0x00
        self._level = 0x00
    def dclose(self):
        self.d.close()
    def info(self):
        print(self.d.getDeviceInfo())
    def set_bitmode(self, bits, mode):
        return self.d.setBitMode(bits, mode)
    #Read byte data into list of integers
    def dread(self,nbytes):
        s = self.d.read(nbytes)
        return [ord(c) for c in s] if type(s) is str else list(s)
    #Write list of integers as byte data
    def dwrite(self,data):
        s = str(bytearray(data)) if sys.version_info<(3,) else bytes(data)
        return self.d.write(s)
    #Set SPI clock rate
    def set_spi_clock(self,hz):
        div = int((12000000/(hz*2))-1)
        self.dwrite((0x86,div%256,div//256))
    
    def loopback(self):
        self.d.write('\x84')

    def _mpsse_enable(self):
        self.set_bitmode(0,0)
        self.set_bitmode(0,2)
    def _mpsse_sync(self, max_retries=10):
        self.d.write('\xAB')
        tries=0
        sync=False
        while not sync:
            data = self.dread(2)
            if data == [250,171]:
                sync=True
            tries+=1
            if tries >= max_retries:
                raise RuntimeError('Could not synchornize with FT4232H')
    def mpsse_read_gpio(self):
        self.d.write('\x81')
        return self.dread(1)
    def mpsse_gpio(self):
        level_low = self._level & 0xFF
        dir_low = self._direction & 0xFF
        return (0x80, level_low, dir_low)
    def mpsse_write_gpio(self):
        self.dwrite(self.mpsse_gpio())

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
    def setup(self,pin,mode):
        self._setup_pin(pin,mode)
        self.mpsse_write_gpio()
    def setup_pins(self,pins,values={},write=True):
        for pin, mode in iter(pins.items()):
            self._setup_pin(pin,mode)
        for pin, value in iter(values.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()
    def _output_pin(self, pin, value):
        if value:
            self._level |= (1<<pin)&0xFF
        else:
            self._level &= ~(1<<pin)&0xFF
    def output(self, pin, value):
        if pin < 0 or pin > 7:
            raise ValueError('Pin must be between 0 and 15 (inclusive).')
        self._output_pin(pin, value)
        self.mpsse_write_gpio()
    def output_pins(self, pins, write=True):
        for pin, value in iter(pins.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()
    def input(self, pin):
        return self.input_pins([pin])[0]
    def input_pins(self, pins):
        if [pin for pin in pins if pin < 0 or pin > 7]:
            raise ValueError('Pin must be between 0 and 7 (inclusive).')
        _pins = self.mpsse_read_gpio()
        return [((_pins >> pin) & 0x01) == 1 for pin in pins]

class SPI(object):
    def __init__(self, ftdi, cs=None, max_speed_hz=1000000, mode=0, bitorder = MSBFIRST):
        self.ftdi=ftdi
        if cs is not None:
            self.ftdi.setup(cs,"output")
            self.ftdi.output(cs,1)
        self._cs=cs

        self.set_clock_hz(max_speed_hz)
        self.set_mode(mode)
        self.set_bit_order(bitorder)
        rbuffer = self.ftdi.d.getQueueStatus()
        if (rbuffer>0 and self.ftdi.d.status ==1):
            s=self.ftdi.dread(rbuffer)
    def _assert_cs(self):
        if self._cs is not None:
            self.ftdi.output(self._cs,0)
    def _deassert_cs(self):
        if self._cs is not None:
            self.ftdi.output(self._cs,1)
    def set_clock_hz(self, hz):
        self.ftdi.set_spi_clock(hz)
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
        self.ftdi.setup_pins({0:"output",1:"output",2:"input",3:"output"},{0:clock_base,3:1})
    def set_bit_order(self, order):
        if order == MSBFIRST:
            self.lsbfirst = 0
        elif order == LSBFIRST:
            self.lsbfirst = 1
        else:
            raise ValueError('Order must be MSBFIRST or LSBFIRST.')
    
    def write(self,data):
        command = 0x10|(self.lsbfirst<<3)|self.write_clock_ve
        length = len(data)-1
        len_low = length&0xFF
        self.ftdi.dwrite((command,len_low))
        self.ftdi.dwrite(data)
    def read(self,length):
        command = 0x20|(self.lsbfirst<<3)|(self.read_clock_ve<<2)
        len_low = (length-1)&0xFF
        self.ftdi.dwrite((command,len_low,0x87))
        return self.ftdi.dread(length)
    def transfer(self,data):
        command = 0x30|(self.lsbfirst<<3)|(self.read_clock_ve<<2)|self.write_clock_ve
        length = len(data)
        len_low = (length-1)&0xFF
        rbuffer = self.ftdi.d.getQueueStatus()
        if (rbuffer>0 and self.ftdi.d.status ==1):
            s=self.ftdi.dread(rbuffer)
        self._assert_cs()
        self.ftdi.dwrite((command,len_low))
        self.ftdi.dwrite(data)
        self.ftdi.d.write('\x87')
        self._deassert_cs()
        return (self.ftdi.dread(length))            