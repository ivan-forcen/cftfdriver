import sys, time, ftd2xx as ftd
from mcp_functions import ft
from ftd_functions import Ftdi

if __name__ == "__main__":  
    ft4232h = ft.FT4232H()
    spi = ft.SPI(ft4232h,cs=3,max_speed_hz=1000000,mode=0,bitorder=ft.MSBFIRST)
    spi.ftdi.loopback()
    print(spi.transfer((0x90,0xf3)))
    
    


