#include <stdio.h>
#include <stdint.h>
#include <netinet/in.h>
#include <string.h> 
#include "E30ModbusMsg.h"

#define RCVBUFSIZE 1024

char rxBuf[RCVBUFSIZE];       /* buffer for the reply message */
int rxBufLen = 0;             /* length of reply message */

void print_received_msg(uint8_t *buf, int buflen) {
  int c;

  /* Print the size of message */
  fprintf(stderr, "Number of received bytes: %d\n", buflen);
  
  /* Print the echo buffer */
  fprintf(stderr, "%s\n", buf);
  
  /* Display the received message as hex arrays */
  for (c = 0; c < buflen; c++) {
    fprintf(stderr, "%02X ", (uint8_t)*(buf + c));
  }
  fprintf(stderr, "\n");

  switch (buf[BYTEPOS_MODBUS_FUNC]) {
  case MODBUS_FUNC_READ_REG:
    print_modbus_reply_read_reg(buf, buflen);
    break;

  case MODBUS_FUNC_WRITE_REG:
    print_modbus_reply_write_reg(buf, buflen);
    break;

  case MODBUS_FUNC_WRITE_MULTIREG:
    print_modbus_reply_write_multireg(buf, buflen);
    break;

  case MODBUS_FUNC_REPORT_SLAVEID:
    print_modbus_reply_report_slaveid(buf, buflen);
    break;

  default:
    break;
  } 
}

void print_modbus_reply_read_reg(uint8_t *buf, int buflen) {
  uint8_t byte_cnt;
  int c;
  uint32_t crc_temp;
  modbus_reply_read_reg* reply_msg = (modbus_reply_read_reg*) buf;

  fprintf(stderr, "Response received:\n");
  fprintf(stderr, "  Modbus addr: %d\n", reply_msg->modbus_addr);
  fprintf(stderr, "  Modbus function: %d\n", reply_msg->modbus_func);
  fprintf(stderr, "  Modbus value bytes: %d\n", reply_msg->modbus_val_bytes);

  byte_cnt = reply_msg->modbus_val_bytes;

  /* Display registers */
  fprintf(stderr, "  registers (hex): \n");
  for (c = 0; c < byte_cnt / 2; c++) {
    fprintf(stderr, "%04X ", ntohs(reply_msg->modbus_reg_val[c]));
  }
  fprintf(stderr, "\n");

  fprintf(stderr, "  registers (unsigned dec): \n");
  for (c = 0; c < byte_cnt / 2; c++) {
    fprintf(stderr, "%u ", ntohs(reply_msg->modbus_reg_val[c]));
  }
  fprintf(stderr, "\n");

  fprintf(stderr, "  registers (signed dec): \n");
  for (c = 0; c < byte_cnt / 2; c++) {
    fprintf(stderr, "%d ", (short) ntohs(reply_msg->modbus_reg_val[c]));
  }
  fprintf(stderr, "\n");

  /* Check the CRC in the packet */
  crc_temp = read_crc16((uint8_t*) buf,
                        sizeof(modbus_reply_read_reg) +
                        reply_msg->modbus_val_bytes);
  fprintf(stderr, "  CRC (hex): %02X\n", crc_temp);

  for (c = 0; c < byte_cnt / 2; c++) {
    printf("%d ", (short) ntohs(reply_msg->modbus_reg_val[c]));
  }
  printf("\n"); 
}

void print_modbus_reply_write_reg(uint8_t *buf, int buflen) {
  uint32_t crc_temp;
  modbus_reply_write_reg* reply_msg = (modbus_reply_write_reg*) buf;

  fprintf(stderr, "Response received:\n");
  fprintf(stderr, "  Modbus addr: %d\n", reply_msg->modbus_addr);
  fprintf(stderr, "  Modbus function: %d\n", reply_msg->modbus_func);
  fprintf(stderr, "  Modbus register address: %d\n", ntohs(reply_msg->modbus_reg_addr));
  fprintf(stderr, "  Modbus register value (hex): %04X\n", 
          ntohs(reply_msg->modbus_reg_val));
  fprintf(stderr, "  Modbus register value (unsigned dec): %u\n", 
          ntohs(reply_msg->modbus_reg_val));
  fprintf(stderr, "  Modbus register value (signed dec): %d\n", 
          (short) ntohs(reply_msg->modbus_reg_val));

  /* Check the CRC in the packet */
  crc_temp = read_crc16((uint8_t*) buf, sizeof(modbus_reply_write_reg));
  fprintf(stderr, "  CRC (hex): %02X\n", crc_temp);
}

void print_modbus_reply_write_multireg(uint8_t *buf, int buflen) {
  uint32_t crc_temp;
  modbus_reply_write_multireg* reply_msg = (modbus_reply_write_multireg*) buf;

  fprintf(stderr, "Response received:\n");
  fprintf(stderr, "  Modbus addr: %d\n", reply_msg->modbus_addr);
  fprintf(stderr, "  Modbus function: %d\n", reply_msg->modbus_func);
  fprintf(stderr, "  Modbus register address: %d\n", ntohs(reply_msg->modbus_reg_addr));
  fprintf(stderr, "  Modbus register quantity: %d\n", ntohs(reply_msg->modbus_reg_qty));

  /* Check the CRC in the packet */
  crc_temp = read_crc16((uint8_t*) buf, sizeof(modbus_reply_write_multireg));
  fprintf(stderr, "  CRC (hex): %02X\n", crc_temp);
}


void print_modbus_reply_report_slaveid(uint8_t *buf, int buflen) {
  uint32_t crc_temp;
  uint8_t additionalData[80]; /* Buffer for additional data */

  modbus_reply_report_slaveid* reply_msg = (modbus_reply_report_slaveid*) buf;

  fprintf(stderr, "Response received:\n");
  fprintf(stderr, "  Modbus addr: %d\n", reply_msg->modbus_addr);
  fprintf(stderr, "  Modbus function: %d\n", reply_msg->modbus_func);
  fprintf(stderr, "  byte count: %d\n", reply_msg->modbus_val_bytes);
  fprintf(stderr, "  slave ID (hex): %02X\n", reply_msg->modbus_slaveid);
  fprintf(stderr, "  run indicator (0x00 - OFF, 0xFF - ON): %02X\n",
          reply_msg->modbus_run_indicator);
  strncpy((char*)additionalData, (char*) reply_msg->modbus_additional,
          reply_msg->modbus_val_bytes - 2);
  fprintf(stderr, "  additional data: %s\n", additionalData);

  /* Check the CRC in the packet */
  crc_temp = read_crc16((uint8_t*) buf,
                        sizeof(modbus_reply_report_slaveid) +
                        reply_msg->modbus_val_bytes - 2);
  fprintf(stderr, "  CRC (hex): %02X\n", crc_temp); 
}


