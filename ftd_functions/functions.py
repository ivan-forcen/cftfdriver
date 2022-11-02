import sys, time, ftd2xx as ftd
from numpy import true_divide
FTDI_TIMEOUT = 1000
class Ftdi:
    def __init__(self):
        #Open device r/w
        self.d=ftd.open(0)
        if not self.d:
            print("Can't open device")
        self.d.setTimeouts(FTDI_TIMEOUT, FTDI_TIMEOUT)
    #get device info
    def info(self):
        print(self.d.getDeviceInfo())
    #Set mode MPSSE self,0x08,2
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
    #output:io=1,input:io=0
    #set input output of pins
    def set_iomode(self,bus,io,data,bits):
        if bus=='a' and io==1:
            self.dwrite((0x80,data,bits))
        elif bus=='a' and io==0:
            self.dwrite((0x81,data,bits))
        elif bus=='b' and io==1:
            self.dwrite((0x82,data,bits))
        elif bus=='b' and io==0:
            self.dwrite((0x83,data,bits))
        else:
            print("invalid cmd")
    #Set SPI clock rate
    def set_spi_clock(self,hz):
        div = int((12000000/(hz*2))-1)
        self.dwrite((0x86,div%256,div//256))
    #Commands:
    #0x10 - Data Out, Bytes,+ve edge
    #0x11 - Data Out, Bytes,-ve edge
    #0x20 - Data In, Bytes,+ve edge
    #0x24 - Data In, Bytes,-ve edge
    def write_cmd_bytes(self, cmd, data):
        try:
            n = len(data) -1
            self.dwrite([cmd,n%256,n//256]+list(data))
        except TypeError:
            n=0x07
            self.dwrite((cmd,n,data))
    def dclose(self):
        self.d.close()

    #Enable SPI, CS,MOSI,CLK pulled low, set as outputs
    def SPI_CSEnable(self,bus):
        i=0
        if bus=='a':
            while i < 5:
                self.dwrite((0x80,0x00,0x0b))
                i=i+1
        elif bus=='b':
            while i < 5:
                self.dwrite((0x82,0x00,0x0b))
                i=i+1

    #Disable SPI, CS Pulled High, MOSI, CLK pulled low, set as outputs
    def SPI_CSDisable(self,bus):
        i=0
        if bus=='a':
            while i < 5:
                self.dwrite((0x80,0x08,0x0b))
                i=i+1
        elif bus=='b':
            while i < 5:
                self.dwrite((0x82,0x08,0x0b))
                i=i+1
    #Clear recieve and output buffer, reset device/parameters, check synchronisation
    def SPI_Initial(self):
        self.d.resetDevice()
        rbuffer = self.d.getQueueStatus()
        if (rbuffer>0 and self.d.status ==1):
            s=self.dread(rbuffer)
        self.d.setUSBParameters(65535,65535)
        self.d.setChars(0,0,0,0)
        self.d.setTimeouts(3000,3000)
        self.d.setLatencyTimer(1)
        self.d.setBitMode(0x0,0x00)
        self.d.setBitMode(0x0,0x02)
        self.set_spi_clock(1000000)
        time.sleep(0.05)
        self.dwrite((0xAA,0x00))
        if self.dread(4)==[250,170,250,0]:
            print("synchronised to MPSSE 0xAA")
        else:
            print("failed to synchronise MPSSE with command '0xAA'")
        time.sleep(0.05)
        self.dwrite((0xAB,0x00))
        if self.dread(4)==[250,171,250,0]:
            print("synchronised to MPSSE 0xAB")
        else:
            print("failed to synchronise MPSSE with command '0xAB'")
        time.sleep(0.02)
        self.d.write('\x85')
        time.sleep(0.03)
        print("SPI initialised successfully")
        return True

    def loopback(self):
        self.d.write('\x84')
        
 
        

