/*******************************************************************************
 * MCP2517FD API Readme
 * 
 * This header file provides brief instructions on how to setup the Hardware and how to use the API example project.
 * The project uses the MCP2517FD click, the SAM V71 Xplained Ultra Evaluation Kit with the ATSAMV71Q21 processor and the mikroBus Xplained Pro adapter board.
 * The example project uses the MCP2517FD API in the Atmel Software Framework (ASF).
 *
 * Please visit the following webpages for more information:
 * - https://www.mikroe.com/mcp2517fd-click
 * - http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMV71-XULT
 * - http://www.microchip.com/developmenttools/productdetails.aspx?partno=atmbusadapter-xpro
 * - http://www.microchip.com/avr-support/atmel-studio-7
 * 
 */

//DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2018 Microchip Technology Inc. and its subsidiaries.

Subject to your compliance with these terms, you may use Microchip software and
any derivatives exclusively with Microchip products. It is your responsibility
to comply with third party license terms applicable to your use of third party
software (including open source software) that may accompany Microchip software.

THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER EXPRESS,
IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED WARRANTIES
OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.

IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND WHATSOEVER
RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS BEEN ADVISED OF
THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE FULLEST EXTENT ALLOWED
BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO
THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID
DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *******************************************************************************/
//DOM-IGNORE-END

#ifndef _README_H
#define _README_H

/*
 * Hardware setup:
 * 
 * 1) Plug the mikroBus Xplained Pro adapter board into connector EXT1 of the SAM V71 Xplained Ultra evaluation kit.
 * 2) Select 3.3V as the jumper selection: VDD of the MCP2517FD.
 * 3) Connect 5V of the POWER connector of SAM V71 Xplained to 5V External Power Header of the adapter board (jumper wire): 5V for VCC of ATA6563.
 * 4) Plug MCP2517FD click into adapter board.
 * 5) Power SAM V71 Xplained by connecting a USB cable to the DEBUG connector and plugging it into your PC.
 * 6) Connect a CAN bus cable to D-sub 9 connector of MCP2517FD click board and to a second CAN FD node, e.g. K2L OptoLyzer® MOCCA FD tool.
 * 7) Make sure both ends of the CAN bus are terminated.
 * 
 * 
 * Example project:
 * 
 * - V71_CANFDSPI:
 *      This is an example project that uses the MCP2517FD API together with the ATSAMV71Q21 processor in Atmel Studio.
 *      CAN messages are transmitted when switch SW0 is pressed.
 *      LED0 and LED1 can be controlled by CAN FD messages.
 *      The MCP2517FD API files can be found in "driver\canfdspi".
 *		The API uses the processor specific SPI functions DRV_SPI_Initialize(), and DRV_SPI_TransferData() to interface with the MCP2517FD.
 *		The definition of the CAN FD messages can be found in Demo.dbc.
 * 
 */

#endif /* _README_H */

/*******************************************************************************
 End of File
 */

