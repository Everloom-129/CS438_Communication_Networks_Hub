#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/stat.h>
#include <signal.h>
#include <string.h>
#include <sys/time.h>

#include <iostream>
#include <string>
#include <vector>


// Each tcp segment is 1500B, with 20B header info and 1480B data  
#define MSS 1500 // max number of bytes we can get at once 
#define PAYLOAD (MSS - 18)
// #define TIMEOUT 2
#define CWND_SIZE  1 // initial cwnd size
#define SSTHRESH int(512000/PAYLOAD) // initial ssthresh size, =64KB
#define TIMEOUT 30000 // usec, = 50 ms

typedef struct Segment {
    uint32_t sequenceNum;   // 4 byte
    uint32_t ackNum;        // 4 byte
    uint32_t offset;        // 4 byte, used for 
    int32_t  packet_length; // 4 byte
    uint8_t  FIN;          // 1 byte
    uint8_t  SYN;          // 1 byte
    char data[PAYLOAD];
}Segment;                        // Total: 17 bytes
