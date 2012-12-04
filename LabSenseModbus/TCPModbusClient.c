#include <stdio.h>      /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), connect(), send(), and recv() */
#include <arpa/inet.h>  /* for sockaddr_in and inet_addr() */
#include <stdlib.h>     /* for atoi() and exit() */
#include <string.h>     /* for memset() */
#include <unistd.h>     /* for close() */

#include "E30ModbusMsg.h"

// Zeromq helper file
#include <zmq.h>

#define RCVBUFSIZE 1024   /* Size of receive buffer */ 

#define ARGS_QUERY  5
#define ARGS_READ   6
#define ARGS_WRITE  7
#define ARGS_WRITEM_REGVAL_POS 7

#define SAMPLING_RATE 1


void print_usage_top(char *str);
void print_usage_query(char *str);
void print_usage_read(char *str);
void print_usage_write(char *str);
void print_usage_writem(char *str);
int prepare_msg_query(int argc, char* argv[], char* buf, 
                      struct sockaddr_in *pServAddr);
int prepare_msg_read(int argc, char* argv[], char* buf,
                      struct sockaddr_in *pServAddr);
int prepare_msg_write(int argc, char* argv[], char* buf,
                      struct sockaddr_in *pServAddr);
int prepare_msg_writem(int argc, char* argv[], char* buf,
                      struct sockaddr_in *pServAddr);

int main(int argc, char *argv[])
{
    int sock;                     /* Socket descriptor */
    struct sockaddr_in servAddr;  /* Echo server address */
    char txBuf[RCVBUFSIZE];       /* String to send to echo server */
    char rxBuf[RCVBUFSIZE];       /* Buffer for echo string */ 
    uint32_t txBufLen;            /* Length of string to echo */
    int bytesRcvd;                /* Bytes read in single recv() */ 
    int c;
    int i;
    Type read_type = Normal;      /* This type is used for zeromq_special_mode */
    int first_iteration_finished = 0;

    // Zeromq context and publisher
    void *context = zmq_init(1);
    void *publisher = zmq_socket (context, ZMQ_PUB);
    zmq_bind(publisher, "tcp://*:5557");

    txBufLen = 0;

    /* Zero out the server address structure */
    memset(&servAddr, 0, sizeof(servAddr));     

    if (argc < 2) {
      print_usage_top(argv[0]); 
    }
    /* Check arguments for help command */
    else if (strcmp(argv[1], "help") == 0 || strcmp(argv[1], "h") == 0) {
      print_usage_top(argv[0]); 
    }
    /* Check arguments for query command */
    else if (strcmp(argv[1], "query") == 0 || strcmp(argv[1], "q") == 0) {
      if (argc >= 3 && 
          (strcmp(argv[2], "help") == 0 || strcmp(argv[2], "h") == 0)) {
        print_usage_query(argv[0]);
      }
      /* Test for correct number of arguments */
      else if (argc != ARGS_QUERY) {
        print_usage_query(argv[0]);
      }

      /* Prepare tx buffer for query command */
      txBufLen = prepare_msg_query(argc, argv, txBuf, &servAddr);
    } 
    /* Check arguments for read command */
    else if (strcmp(argv[1], "read") == 0 || strcmp(argv[1], "r") == 0) {
      if (argc >= 3 &&
          (strcmp(argv[2], "help") == 0 || strcmp(argv[2], "h") == 0)) {
        print_usage_read(argv[0]);
      }
      else if (argc == 3 && strcmp(argv[2], "eaton") == 0) {

eaton_loop:
          read_type = Eaton;

          printf("Tracking Voltages, Currents, Power, VARS, VAS, Power Factor\n");

          // Set the arguments according to the prepare_msg_read function
          argc = 7;
          argv[1] = "read";             // Read from the eaton
          argv[2] = "128.97.11.100";    // IP address of eaton
          argv[3] = "4660";             // Server Port
          argv[4] ="1";                 // Modbus Address
          argv[5] = "999";              // Modbus Register Address
          argv[6] = "54";               // Reading 54 Registers

      }
      else if (argc == 3 && strcmp(argv[2], "veris") == 0) {
    
veris_loop:
          // Special case to read all power and current readings 
          // and send over zeromq
          printf("Tracking power, current, energy ,and power factor\n");

          if(read_type == Normal) {
              read_type = Power;
          }
          else if(read_type == Power) {
            read_type = PowerFactor;
          }
          else if(read_type == PowerFactor) {
              read_type = Current;
          }
          else if(read_type == Current) {
              read_type = Power;
          }
          else {
              printf("Error in read type\n");
          }

          // Set the arguments according to the prepare_msg_read function
          argc = 7;
          argv[1] = "read";             // Read from the veris
          argv[2] = "172.17.5.177";     // IP Address of Veris
          /*argv[2] = "128.97.93.201";     // IP Address of Veris*/
          argv[3] = "4660";             // Server Port
          argv[4] ="1";                 // Modbus Address
          argv[6] = "42";               // Reading 42 Registers

          // Set the Register address
          switch(read_type) {
              case Power:
                  // Get Power Readings (KW)
                  argv[5] = "2083";
                  read_type = Power;
                  break;

              case PowerFactor:
                  // Get Power Readings (KW)
                  argv[5] = "2267";
                  read_type = PowerFactor;
                  break;
                  
              case Current:
                  // Get Current Readings (A)
                  argv[5] = "2251";
                  read_type = Current;
                  break;
              default: 
                  printf("Error in read type\n");
                  break;
          }
      }
      /* Test for correct number of arguments */
      else if (argc != ARGS_READ && argc != ARGS_READ + 1) {
          print_usage_read(argv[0]); 
      }

      /* Prepare tx buffer for read command */
      txBufLen = prepare_msg_read(argc, argv, txBuf, &servAddr);
      printf("argc: %d\n", argc);
      printf("argv: ");
      for(i = 0; i < argc; i++) {
          printf("%s, ", argv[i]);
      }
      printf("\n");

    }
    /* Check arguments for write command */
    else if (strcmp(argv[1], "write") == 0 || strcmp(argv[1], "w") == 0) {
        if (argc >= 3 &&
                (strcmp(argv[2], "help") == 0 || strcmp(argv[2], "h") == 0)) {
            print_usage_write(argv[0]);
        }
        /* Test for correct number of arguments */
        else if (argc != ARGS_WRITE) {
            print_usage_write(argv[0]); 
        }

        /* Prepare tx buffer for write command */
        txBufLen = prepare_msg_write(argc, argv, txBuf, &servAddr); 
    }
    /* Check arguments for writem command */
    else if (strcmp(argv[1], "writem") == 0 || strcmp(argv[1], "m") == 0) {
        if (argc >= 3 &&
                (strcmp(argv[2], "help") == 0 || strcmp(argv[2], "h") == 0)) {
            print_usage_writem(argv[0]);
        }
        /* Test for correct number of arguments */
      else if (argc < ARGS_WRITEM_REGVAL_POS) { 
        print_usage_writem(argv[0]);
      }

      /* Prepare tx buffer for writem command */
      txBufLen = prepare_msg_writem(argc, argv, txBuf, &servAddr); 
    }
    else {
      print_usage_top(argv[0]); 
    }


    if(first_iteration_finished == 0) {
        /* Create a reliable, stream socket using TCP */
        if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
            DieWithError("socket() failed");

        /* Establish the connection to the echo server */
        if (connect(sock, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0)
            DieWithError("connect() failed");
    }

    /* Print the size of message */
    fprintf(stderr, "Number of transmitting bytes: %d\n", txBufLen);

    /* Print the echo buffer */
    fprintf(stderr, "%s\n", txBuf);

    /* Display the received message as hex arrays */

    for (c = 0; c < txBufLen; c++) {
      fprintf(stderr, "%02X ", (uint8_t)*(txBuf + c));
    }
    fprintf(stderr, "\n"); 

    /* Send the string to the server */
    if (send(sock, txBuf, txBufLen, 0) != txBufLen)
        DieWithError("send() sent a different number of bytes than expected");

    bytesRcvd = 0;
    /* Receive the same string back from the server */
    while (bytesRcvd == 0)
    {
        /* Receive up to the buffer size bytes from the sender */
        if ((bytesRcvd = recv(sock, rxBuf, RCVBUFSIZE - 1, 0)) <= 0)
            DieWithError("recv() failed or connection closed prematurely");
        rxBuf[bytesRcvd] = '\0';  /* Terminate the string! */ 
    }

    print_received_msg((uint8_t *)rxBuf, bytesRcvd, read_type, publisher);

    if(read_type != Normal) {
        first_iteration_finished = 1;
        sleep(SAMPLING_RATE);
        if(read_type == Eaton)
            goto eaton_loop;
        else
            goto veris_loop;
    }

    zmq_close(publisher);
    close(sock);
    exit(0);

}


void print_usage_top(char *str) {
fprintf(stderr,"E30 TCP Modbus Client\n");
fprintf(stderr,"Usage: %s {(q)uery | (r)ead | (w)rite | write(m) | (h)elp} ...\n",str);
fprintf(stderr,"  query  - queries the slave ID\n");
fprintf(stderr,"  read   - read one or multiple registers\n");
fprintf(stderr,"  write  - write to a register\n");
fprintf(stderr,"  writem - write to one or multiple registers\n");
fprintf(stderr,"  help   - print this message\n"); 
exit(1);
}

void print_usage_query(char *str) {
  fprintf(stderr,"E30 TCP Modbus Client\n");
  fprintf(stderr,"Usage: %s query <Server IP> <Server Port> <Modbus Addr>\n",
          str);
  exit(1);
};

void print_usage_read(char *str) {
  fprintf(stderr,"E30 TCP Modbus Client\n");
  fprintf(stderr,"Usage: %s read <Server IP> <Server Port> <Modbus Addr> <Register Addr> [<Qty Registers>]\n", str);
  exit(1); 
}

void print_usage_write(char *str) {
  fprintf(stderr,"E30 TCP Modbus Client\n");
  fprintf(stderr,"Usage: %s write <Server IP> <Server Port> <Modbus Addr> <Register Addr> <Register Val>\n", str); 
  exit(1); 
}

void print_usage_writem(char *str) {
  fprintf(stderr,"E30 TCP Modbus Client\n");
  fprintf(stderr,"Usage: %s writem <Server IP> <Server Port> <Modbus Addr> <Register Addr> <Register Qty> <Val 1> <Val 2> ... \n", str);
  exit(1); 
}

int prepare_msg_query(int argc, char* argv[], char* buf, 
                      struct sockaddr_in *pServAddr) {
  uint16_t servPort;            /* Server port */
  char *servIP;                 /* Server IP address (dotted quad) */
  int bufLen;                   /* Length of string to echo */
  uint8_t modbus_addr;          /* 8-bit modbus addr */
  uint32_t crc_temp;
  uint32_t crc_offset;
  
  modbus_req_report_slaveid* req_msg = NULL;

  servIP = argv[2];             /* First arg: server IP address */ 
  servPort = atoi(argv[3]);     /* Use given port, if any */ 
  modbus_addr = (uint8_t) atoi(argv[4]);   /* modbus address */

  pServAddr->sin_family      = AF_INET;     /* Internet address family */
  pServAddr->sin_addr.s_addr = inet_addr(servIP); /* Server IP address */
  pServAddr->sin_port        = htons(servPort);   /* Server port */

  req_msg = (modbus_req_report_slaveid*) buf;
  req_msg->modbus_addr = modbus_addr;
  req_msg->modbus_func = MODBUS_FUNC_REPORT_SLAVEID;

  /* Calculate CRC16 for the request msg */
  crc_offset = sizeof(modbus_req_report_slaveid); 
  crc_temp = calc_crc16((uint8_t*) buf, crc_offset); 
  buf[crc_offset]   = (uint8_t) crc_temp & 0x0ff; /* lower 8bit */
  buf[crc_offset+1] = (uint8_t) (crc_temp >> 8) & 0x0ff;  /* upper 8bit */
  buf[crc_offset+2] = 0; /* end of string */

  bufLen = crc_offset + CRC16_SIZE;

  return bufLen; 
}

int prepare_msg_read(int argc, char* argv[], char* buf,
                     struct sockaddr_in *pServAddr) {
  uint16_t servPort;            /* Server port */
  char *servIP;                 /* Server IP address (dotted quad) */
  int bufLen;                   /* Length of string to echo */
  uint8_t modbus_addr;          /* 8-bit modbus addr */
  uint32_t crc_temp;
  uint32_t crc_offset;
  uint16_t reg_addr;            /* 16-bit register addr */
  uint16_t reg_qty;             /* quantity of registers to read (1-125) */

  modbus_req_read_reg* req_msg = NULL;

  servIP = argv[2];         /* First arg: server IP address (dotted quad) */
  servPort = atoi(argv[3]); /* Use given port, if any */
  modbus_addr = (uint8_t) atoi(argv[4]);   /* modbus address */
  reg_addr = (uint16_t) atoi(argv[5]);     /* register address */

  pServAddr->sin_family      = AF_INET;     /* Internet address family */
  pServAddr->sin_addr.s_addr = inet_addr(servIP); /* Server IP address */
  pServAddr->sin_port        = htons(servPort);   /* Server port */

  if (argc == 7) {
    reg_qty = (uint16_t) atoi(argv[6]);    /* quantity of registers */
    /* Ensure that reg_qty between 1 to 125. */
    if (reg_qty < MODBUS_REG_READ_QTY_MIN ||
        reg_qty > MODBUS_REG_READ_QTY_MAX) {
      reg_qty = MODBUS_REG_READ_QTY_DEFAULT;
    }
  }
  else {
    reg_qty = MODBUS_REG_READ_QTY_DEFAULT;
  }

  /* Fill in each field of buf */
  req_msg = (modbus_req_read_reg*) buf;
  req_msg->modbus_addr = modbus_addr;
  req_msg->modbus_func = MODBUS_FUNC_READ_REG;
  req_msg->modbus_reg_addr = htons(reg_addr);
  req_msg->modbus_reg_qty  = htons(reg_qty);

  /* Calculate CRC16 for the request msg */
  crc_offset = sizeof(modbus_req_read_reg);
  crc_temp = calc_crc16((uint8_t*) buf, crc_offset);
  buf[crc_offset]   = (uint8_t) crc_temp & 0x0ff; /* lower 8bit */
  buf[crc_offset+1] = (uint8_t) (crc_temp >> 8) & 0x0ff;  /* upper 8bit */
  buf[crc_offset+2] = '\0'; /* end of string */

  bufLen = crc_offset + CRC16_SIZE; 

  return bufLen; 
}

int prepare_msg_write(int argc, char* argv[], char* buf,
                      struct sockaddr_in *pServAddr) {
  uint16_t servPort;            /* Server port */
  char *servIP;                 /* Server IP address (dotted quad) */
  int bufLen;                   /* Length of string to echo */
  uint8_t modbus_addr;          /* 8-bit modbus addr */
  uint32_t crc_temp;
  uint32_t crc_offset;
  uint16_t reg_addr;            /* 16-bit register addr */
  uint16_t reg_val;             /* 16-bit register value to write with */

  modbus_req_write_reg* req_msg      = NULL;

  servIP = argv[2];         /* First arg: server IP address (dotted quad) */
  servPort = atoi(argv[3]); /* Use given port, if any */
  modbus_addr = (uint8_t) atoi(argv[4]);   /* modbus address */
  reg_addr = (uint16_t) atoi(argv[5]);     /* register address */
  reg_val = (uint16_t) atoi(argv[6]);      /* register value */

  pServAddr->sin_family      = AF_INET;     /* Internet address family */
  pServAddr->sin_addr.s_addr = inet_addr(servIP); /* Server IP address */
  pServAddr->sin_port        = htons(servPort);   /* Server port */

  /* Fill in each field of buf */
  req_msg = (modbus_req_write_reg*) buf;
  req_msg->modbus_addr = modbus_addr;
  req_msg->modbus_func = MODBUS_FUNC_WRITE_REG;
  req_msg->modbus_reg_addr = htons(reg_addr);
  req_msg->modbus_reg_val  = htons(reg_val);

  /* CRC: first lower 8-bit, then upper 8-bit */
  /* Exception to Big-endianess */
  crc_offset = sizeof(modbus_req_write_reg);
  crc_temp = calc_crc16((uint8_t*) buf, crc_offset);
  buf[crc_offset]   = (uint8_t) crc_temp & 0x0ff; /* lower 8bit */
  buf[crc_offset+1] = (uint8_t) (crc_temp >> 8) & 0x0ff;  /* upper 8bit */
  buf[crc_offset+2] = '\0'; /* end of string */

  bufLen = crc_offset + CRC16_SIZE;

  return bufLen; 
}

int prepare_msg_writem(int argc, char* argv[], char* buf,
                       struct sockaddr_in *pServAddr) {
  uint16_t servPort;            /* Server port */
  char *servIP;                 /* Server IP address (dotted quad) */
  int bufLen;                   /* Length of string to echo */
  uint8_t modbus_addr;          /* 8-bit modbus addr */
  uint32_t crc_temp;
  uint32_t crc_offset;
  uint16_t reg_addr;            /* 16-bit register addr */
  uint16_t reg_qty;             /* quantity of registers to write */
  uint16_t reg_val;             /* 16-bit register value to write with */
  int c;

  modbus_req_write_multireg* req_msg = NULL;

  servIP   = argv[2];       /* First arg: server IP address (dotted quad) */
  servPort = atoi(argv[3]); /* Use given port, if any */
  modbus_addr = (uint8_t) atoi(argv[4]);  /* modbus address */
  reg_addr    = (uint16_t) atoi(argv[5]); /* register address */
  reg_qty     = (uint16_t) atoi(argv[6]); /* quantity of registers */
  
  pServAddr->sin_family      = AF_INET;     /* Internet address family */
  pServAddr->sin_addr.s_addr = inet_addr(servIP); /* Server IP address */
  pServAddr->sin_port        = htons(servPort);   /* Server port */

  /* Test for correct number of register values */
  if (argc - ARGS_WRITEM_REGVAL_POS != reg_qty)  {
    fprintf(stderr, "Usage: %s <Server IP> <Server Port> <Modbus Addr> <Register Addr> <Register Qty> <Val 1> <Val 2> ... \n", argv[0]);
    fprintf(stderr, "<Register Qty> and number of registers <Val 1>, <Val 2>, ... should match. \n");
    exit(1);
  }

  /* Fill in each field of buf */
  req_msg = (modbus_req_write_multireg*) buf;
  req_msg->modbus_addr = modbus_addr;
  req_msg->modbus_func = MODBUS_FUNC_WRITE_MULTIREG;
  req_msg->modbus_reg_addr = htons(reg_addr);
  req_msg->modbus_reg_qty  = htons(reg_qty);
  req_msg->modbus_val_bytes = (uint8_t) 2 * reg_qty;
  for (c = 0; c < reg_qty; c++) {
    reg_val = (uint16_t) atoi(argv[ARGS_WRITEM_REGVAL_POS + c]);
    req_msg->modbus_reg_val[c] = htons(reg_val);
  }

  /* CRC: first lower 8-bit, then upper 8-bit */
  /* Exception to Big-endianess */
  crc_offset = sizeof(modbus_req_write_multireg) + 2 * reg_qty;
  crc_temp = calc_crc16((uint8_t*) buf, crc_offset);
  buf[crc_offset]   = (uint8_t) crc_temp & 0x0ff; /* lower 8bit */
  buf[crc_offset+1] = (uint8_t) (crc_temp >> 8) & 0x0ff;  /* upper 8bit */
  buf[crc_offset+2] = '\0'; /* end of string */

  bufLen = crc_offset + CRC16_SIZE;

  return bufLen; 
}

