import sys, time, ftd2xx as ftd
from ftd_functions import Ftdi
from mcp_functions import Mcp

if __name__ == "__main__":
    dev=Ftdi()
    dev.SPI_Initial()
    dev.SPI_CSDisable('a')
    dev.info()
    dev.loopback()
    time.sleep(2)
    dev.SPI_CSEnable('a')
    dev.write_cmd_bytes(0x31,(0x14,0x8B))#0xA9,0x5D
    print(dev.dread(2))
    dev.dwrite((0xAA,0x00))
    print(dev.dread(4))
    dev.SPI_CSDisable('a')
    dev.dclose()
    


