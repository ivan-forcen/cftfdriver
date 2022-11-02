import sys, time, ftd2xx as ftd
from ftd_functions import Ftdi
from mcp_functions import Mcp

if __name__ == "__main__":
    dev=Ftdi()
    dev.SPI_Initial()
    dev.SPI_CSDisable
    dev.info()
    dev.loopback()
    dev.SPI_CSEnable
    dev.write_cmd_bytes(0x31,(169,93))#0b10101001,0b01011101
    print(dev.dread(2))
    dev.dwrite((0xAA,0x00))
    print(dev.dread(4))
    dev.SPI_CSDisable('a')
    dev.dclose()
    


