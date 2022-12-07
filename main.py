import sys, time, ftd2xx as ftd
from mcp_functions import ft
from mcp_functions import mcplib
from mcp_functions.constants import *

#bbus = SPI0
#abus = SPI1

dicc = {NORMAL_MODE:'NORMAL_MODE',
    SLEEP_MODE:'SLEEP_MODE',
    INTERNAL_LOOPBACK_MODE: 'INTERNAL_LOOPBACK_MODE',
    LISTEN_ONLY_MODE: 'LISTEN_ONLY_MODE',
    CONFIGURATION_MODE: 'CONFIGURATION_MODE',
    EXTERNAL_LOOPBACK_MODE: 'EXTERNAL_LOOPBACK_MODE',
    CLASSIC_MODE:'CLASSIC_MODE',
    RESTRICTED_MODE: 'RESTRICTED_MODE',
    INVALID_MODE:'INVALID_MODE'
}

if __name__ == "__main__":  
    ft4232ha = ft.FT4232H(index=0)
    ft4232hb = ft.FT4232H(index=1)
    spi1 = ft.SPI(ft4232ha,cs=3,max_speed_hz=1000000,mode=0,bitorder=ft.MSBFIRST)
    spi0 = ft.SPI(ft4232hb,cs=3,max_speed_hz=1000000,mode=0,bitorder=ft.MSBFIRST)
    spi1.ftdi.loopback()
    print(spi1.transfer((0x90,0xf3)))
    spi0.ftdi.loopback()
    print(spi0.transfer((0x90,0xf3)))
    spi0.ftdi.dread(100)
    spi1.ftdi.dread(100)

#     cINSTRUCTION_READ = 0x03
#     cINSTRUCTION_WRITE = 0x02

#     canfd = mcplib.CANFD_SPI(ft4232h, cs, max_speed_hz, mode, bitorder, SPI_DEFAULT_BUFFER_LENGTH, SPI_MAX_BUFFER_LENGTH, SPI_BAUDRATE)

#     canfd.reset()
#     canfd.initialise()

#     address = 0x000
#     word = canfd.readWord(address)
#     print ('Reading CiCON:')
#     print(word)

#     write_word = 0x600798F4
#     print("Word to write: ")
#     print(write_word)
#     canfd.writeWord(address, write_word)
#     word = canfd.readWord(address)
#     print ('Reading CiCON with 0x600798F4 written on it:')
#     print(word)

#     canfd.reset()
#     print("Resetting...")

#     write_byte = 0x6F
#     canfd.writeByte(address, write_byte)
#     word = canfd.readWord(address)
#     print ('Reading CiCON with 0x00 written on its 1st byte:')
#     print(word)

#     canfd.reset()
#     print("Resetting...")
#     write_byte_array = [0x60, 0x07, 0x98, 0xF4]
#     canfd.writeByteArray(address, write_byte_array)
#     word = canfd.readWord(address)
#     print ('Reading CiCON with [0x60, 0x07, 0x98, 0xF4] array written on it (4 bytes):')
#     print(word)

#     canfd.reset()
#     print("Resetting...")

#     write_word_array = [0x600798F4, 0x7f0f3eff]
#     canfd.writeWordArray(address, write_word_array)
#     word = canfd.readWordArray(address, 2)
#     print ('Reading CiCON and CiNBTCFG with [0x600798F4, 0x7f0f3eff] written on it:')
#     print(word)
#    # print(binascii.hexlify(bytearray([word])))
    
    


