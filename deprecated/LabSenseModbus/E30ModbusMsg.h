#ifndef E30_MODBUS_MSG_H
#define E30_MODBUS_MSG_H

#include <stdint.h>
#include <sys/time.h>
#include "SensorAct/SensorActUploader.h"

#define SUCCESS     0
#define FAIL        1

#define CRC16_SIZE  2

/* Modbus function codes supported by E30 */
#define MODBUS_FUNC_READ_REG        0x03
#define MODBUS_FUNC_WRITE_REG       0x06
#define MODBUS_FUNC_WRITE_MULTIREG  0x10 
#define MODBUS_FUNC_REPORT_SLAVEID  0x11 
#define MODBUS_ERR_READ_REG         0x83
#define MODBUS_ERR_WRITE_REG        0x86
#define MODBUS_ERR_WRITE_MULTIREG   0x90 
#define MODBUS_ERR_REPORT_SLAVEID   0x91

/* Byte position within a message */
#define BYTEPOS_MODBUS_ADDR             0
#define BYTEPOS_MODBUS_FUNC             1
#define BYTEPOS_MODBUS_EXCEPTION_CODE   2

#define MODBUS_REG_READ_QTY_DEFAULT   1
#define MODBUS_REG_READ_QTY_MIN       1
#define MODBUS_REG_READ_QTY_MAX       125

/* Run indicator for report_slaveid msg */
#define MODBUS_RUN_INDICATOR_ON       0xff  
#define MODBUS_RUN_INDICATOR_OFF      0x00

/* Zeromq Special Mode Reads 42 Channels */
#define NUMBER_CHANNELS 42

/* Align message structures within byte boundary */
#pragma pack(push)
#pragma pack(1)

/* Message structures for requests excluding CRC16 */

typedef struct modbus_req_read_reg {
  uint8_t   modbus_addr;
  uint8_t   modbus_func; 
  uint16_t  modbus_reg_addr;
  uint16_t  modbus_reg_qty;
} modbus_req_read_reg;

typedef struct modbus_req_write_reg {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
  uint16_t  modbus_reg_addr;
  uint16_t  modbus_reg_val; 
} modbus_req_write_reg;

typedef struct modbus_req_write_multireg {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
  uint16_t  modbus_reg_addr;
  uint16_t  modbus_reg_qty;
  uint8_t   modbus_val_bytes; 
  uint16_t  modbus_reg_val[0]; 
} modbus_req_write_multireg;

typedef struct modbus_req_report_slaveid {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
} modbus_req_report_slaveid;


/* Message structures for replies excluding CRC16 */

typedef struct modbus_reply_read_reg {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
  uint8_t   modbus_val_bytes;
  union { 
    uint16_t  modbus_reg_val[0]; 
    uint32_t  modbus_reg_val32[0];
  };
} modbus_reply_read_reg;

typedef struct modbus_reply_write_reg {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
  uint16_t  modbus_reg_addr;
  uint16_t  modbus_reg_val; 
} modbus_reply_write_reg;

typedef struct modbus_reply_write_multireg {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
  uint16_t  modbus_reg_addr;
  uint16_t  modbus_reg_qty;
} modbus_reply_write_multireg;

typedef struct modbus_reply_report_slaveid {
  uint8_t   modbus_addr;
  uint8_t   modbus_func;
  uint8_t   modbus_val_bytes; 
  uint8_t   modbus_slaveid;
  uint8_t   modbus_run_indicator;
  uint8_t   modbus_additional[0]; 
} modbus_reply_report_slaveid;

#pragma pack(pop)

/* Function declarations */

/* Error handling function */
void DieWithError(char *errorMessage);  

/* Calculate 16-bit CRC */
uint16_t calc_crc16(uint8_t* modbusframe, uint16_t length);

/* The function reads 16-bit CRC from the byte array */
uint16_t read_crc16(uint8_t* byteArr, uint16_t byteOffset);

/* Print the contents of the buffer */
void print_received_msg(uint8_t *buf, int buflen, Type type, time_t timestamp, SensorActConfig *Sconfig); 
void print_modbus_reply_read_reg(uint8_t *buf, int buflen, Type type, time_t timestamp, SensorActConfig *Sconfig);
void print_modbus_reply_write_reg(uint8_t *buf, int buflen);
void print_modbus_reply_write_multireg(uint8_t *buf, int buflen);
void print_modbus_reply_report_slaveid(uint8_t *buf, int buflen);

#endif

