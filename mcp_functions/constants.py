# SPI Instruction Set
cINSTRUCTION_RESET = 0b0000
cINSTRUCTION_READ = 0x03
cINSTRUCTION_READ_CRC = 0x0B
cINSTRUCTION_WRITE = 0x02
cINSTRUCTION_WRITE_CRC = 0x0A
cINSTRUCTION_WRITE_SAFE = 0x0C

# crc16 lookup table
crc16_table = (
    0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
    0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
    0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
    0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
    0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
    0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
    0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
    0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
    0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
    0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
    0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
    0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
    0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
    0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
    0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
    0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
    0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
    0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
    0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
    0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
    0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
    0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
    0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
    0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
    0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
    0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
    0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
    0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
    0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
    0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
    0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
    0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
)

# Register Addresses
# can_fd_ubp
cREGADDR_CiCON = 0x000
cREGADDR_CiNBTCFG = 0x004
cREGADDR_CiDBTCFG = 0x008
cREGADDR_CiTDC = 0x00C

cREGADDR_CiTBC = 0x010
cREGADDR_CiTSCON = 0x014
cREGADDR_CiVEC = 0x018
cREGADDR_CiINT = 0x01C
cREGADDR_CiINTFLAG = cREGADDR_CiINT
cREGADDR_CiINTENABLE = (cREGADDR_CiINT+2)

cREGADDR_CiRXIF = 0x020
cREGADDR_CiTXIF = 0x024
cREGADDR_CiRXOVIF = 0x028
cREGADDR_CiTXATIF = 0x02C

cREGADDR_CiTXREQ = 0x030
cREGADDR_CiTREC = 0x034
cREGADDR_CiBDIAG0 = 0x038
cREGADDR_CiBDIAG1 = 0x03C

cREGADDR_CiTEFCON = 0x040
cREGADDR_CiTEFSTA = 0x044
cREGADDR_CiTEFUA = 0x048
cREGADDR_CiFIFOBA = 0x04C

cREGADDR_CiFIFOCON = 0x050
cREGADDR_CiFIFOSTA = 0x054
cREGADDR_CiFIFOUA = 0x058
CiFIFO_OFFSET = (3*4)

CiFILTER_OFFSET = (2*4)

# MCP2517 Specific
cREGADDR_OSC = 0xE00
cREGADDR_IOCON = 0xE04
cREGADDR_CRC = 0xE08
cREGADDR_ECCCON = 0xE0C
cREGADDR_ECCSTA = 0xE10

# RAM addresses
cRAM_SIZE = 2048
cRAMADDR_START = 0x400
cRAMADDR_END = (cRAMADDR_START+cRAM_SIZE)

# CAN Operation Modes
NORMAL_MODE = 0x00
SLEEP_MODE = 0x01
INTERNAL_LOOPBACK_MODE = 0x02
LISTEN_ONLY_MODE = 0x03
CONFIGURATION_MODE = 0x04
EXTERNAL_LOOPBACK_MODE = 0x05
CLASSIC_MODE = 0x06
RESTRICTED_MODE = 0x07
INVALID_MODE = 0xFF

# Message IDs
FILE_START_ID = 0xd0
FILE_STOP_ID = 0xdf
FILE_DATA_ID = 0xda
TX_REQUEST_ID = 0x300
TX_RESPONSE_ID = 0x301
BUTTON_STATUS_ID = 0x201
LED_STATUS_ID = 0x200
BITTIME_SET_ID = 0x100
PAYLOAD_ID = 0x101
BITTIME_CFG_GET_ID = 0x600
BITTIME_CFG_125K_ID = 0x601
BITTIME_CFG_250K_ID = 0x602
BITTIME_CFG_500K_ID = 0x603
BITTIME_CFG_1M_ID = 0x604

#CAN FIFO channels
CAN_FIFO_CH0 = 0
CAN_FIFO_CH1 = 1
CAN_FIFO_CH2 = 2
CAN_FIFO_CH3 = 3
CAN_FIFO_CH4 = 4
CAN_FIFO_CH5 = 5
CAN_FIFO_CH6 = 6
CAN_FIFO_CH7 = 7
CAN_FIFO_CH8 = 8
CAN_FIFO_CH9 = 9
CAN_FIFO_CH10 = 10
CAN_FIFO_CH11 = 11
CAN_FIFO_CH12 = 12
CAN_FIFO_CH13 = 13
CAN_FIFO_CH14 = 14
CAN_FIFO_CH15 = 15
CAN_FIFO_CH16 = 16
CAN_FIFO_CH17 = 17
CAN_FIFO_CH18 = 18
CAN_FIFO_CH19 = 19
CAN_FIFO_CH20 = 20
CAN_FIFO_CH21 = 21
CAN_FIFO_CH22 = 22
CAN_FIFO_CH23 = 23
CAN_FIFO_CH24 = 24
CAN_FIFO_CH25 = 25
CAN_FIFO_CH26 = 26
CAN_FIFO_CH27 = 27
CAN_FIFO_CH28 = 28
CAN_FIFO_CH29 = 29
CAN_FIFO_CH30 = 30
CAN_FIFO_CH31 = 31
CAN_FIFO_TOTAL_CHANNELS = 32

cREGADDR_CiFLTCON = (cREGADDR_CiFIFOCON+(CiFIFO_OFFSET*CAN_FIFO_TOTAL_CHANNELS))
cREGADDR_CiFLTOBJ = (cREGADDR_CiFLTCON+CAN_FIFO_TOTAL_CHANNELS)
cREGADDR_CiMASK = (cREGADDR_CiFLTOBJ+4)

# Application states
APP_STATE_INIT = 0
APP_STATE_REQUEST_CONFIG = 1
APP_STATE_WAIT_FOR_CONFIG = 2
APP_STATE_INIT_TXOBJ = 3
APP_STATE_TRANSMIT = 4
APP_STATE_RECEIVE = 5
APP_STATE_PAYLOAD = 6
APP_STATE_TEST_RAM_ACCESS = 7
APP_STATE_TEST_REGISTER_ACCESS = 8