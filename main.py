import sys, time, ftd2xx as ftd
from ftd_functions import Ftdi
from mcp_functions import Mcp

if __name__ == "__main__":
    dev=Ftdi()
    #dev.SPI_Initial()
    dev.set_bitmode(0x00,0x02)
    dev.set_spi_clock(1000000)
    dev.SPI_CSDisable('a')
    dev.info()
    dev.loopback()
    dev.SPI_CSEnable('a')
    dev.write_cmd_bytes(0x31,(0x90,0xF3))#0xA9,0x5D
    print(dev.dread(2))
    dev.dwrite((0xAA,0x00))
    print(dev.dread(4))
    dev.SPI_CSDisable('a')
    dev.dclose()
    


