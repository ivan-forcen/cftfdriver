from ftd_functions import Ftdi
#from constants import*
#from classes import*

"""class Mcp:
    def __init__(self,dev):
        dev=Ftdi()
        self.d=dev
    #resets the mcp chip
    def reset(self):
        self.d.SPI_CSEnable('a')
        self.d.write_cmd_bytes(0x10,(0b0000,0x000))
        self.d.SPI_CSDisable('a')
    #reads data from specific address
    def read(self,a,length):
        self.d.SPI_CSEnable('a')
        self.d.write_cmd_bytes(0x11,(0b0011,a))
        self.d.write_cmd_bytes(0x20,(length))
        state = self.d.dread(length)
        self.d.SPI_CSDisable('a')
        return state
    #writes data to specific address
    def write(self,a,data):
        self.d.SPI_CSEnable('a')
        self.d.write_cmd_bytes(0x11,(0b0010,a,data))
        self.d.SPI_CSDisable('a')
    #reads the cyclic redundancy test
    def read_crc(self,a,n):
        self.d.SPI_CSEnable('a')
        self.d.write_cmd_bytes(0x10,(0b1011,a))
        self.d.dread(1)
        self.d.SPI_CSDisable('a')
    #writes crc 2 bytes, calculated from Address/N data bytes/Data
    def write_crc(self,a,data,crc):
        self.d.SPI_CSEnable('a')
        self.d.write_cmd_bytes(0x10,(0b1010,a,data,crc))
        self.d.SPI_CSDisable('a')
    #write sfr/ram to address A
    def write_safe(self,a,data,crc):
        self.d.SPI_CSEnable('a')
        self.d.write_cmd_bytes(0x10,(0b1100,a,data,crc))
        self.d.SPI_CSDisable('a')

    def clearTx(self):
        self.d.SPI_CSEnable('a')
        self.write(0x033,1)
        self.d.SPI_CSDisable('a')
    
    def getOpMode(self):
        self.d.SPI_CSEnable('a')
        state = self.read(0x025,1)
        return state

    def setOpMode(self,mode):#only possible in configuration mode, mode int 0 to 7
        self.d.SPI_CSEnable('a')
        #0:normal can fd mode (supports can fd and can 2.0 frames)
        #1:sleep mode
        #2:internal loopback mode
        #3:listen only mode
        #4:configuration mode
        #5:external loopback mode
        #6:normal can 2.0 mode, error on fd frames
        #7:restricted operation mode
        self.write(0x030,mode)
        self.d.SPI_CSDisable('a')
    def txQEn(self):

    def storeTxEvFifo():

    def canBusy():
        if self.read(0x013,1)==[1]:
            return True
        else:
            return False
    """
    