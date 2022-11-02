from ftd_functions import Ftdi

class Mcp:
    def __init__(self,dev):
        self.d=dev
    #resets the mcp chip
    def reset(self):
        self.SPI_CSEnable()
        self.d.write_cmd_bytes(0x10,(0b0000,0x000))
        self.SPI_CSDisable()
    #reads data from specific address
    def read(self,a,length):
        self.SPI_CSEnable()
        self.d.write_cmd_bytes(0x10,(0b0011,a))
        self.d.write_cmd_bytes(0x21,(length))
        self.d.read(length)
        self.SPI_CSDisable()
    #writes data to specific address
    def write(self,a,data):
        self.SPI_CSEnable()
        self.d.write_cmd_bytes(0x10,(0b0010,a,data))
        self.SPI_CSDisable()
    #reads the cyclic redundancy test
    def read_crc(self,a,n):
        self.SPI_CSEnable()
        self.d.write_cmd_bytes(0x10,(0b1011,a))
        self.d.read(1)
        self.SPI_CSDisable()
    #writes crc 2 bytes, calculated from Address/N data bytes/Data
    def write_crc(self,a,data,crc):
        self.SPI_CSEnable()
        self.d.write_cmd_bytes(0x10,(0b1010,a,data,crc))
        self.SPI_CSDisable()
    #write sfr/ram to address A
    def write_safe(self,a,data,crc):
        self.SPI_CSEnable()
        self.d.write_cmd_bytes(0x10,(0b1100,a,data,crc))
        self.SPI_CSDisable()
    
    