/*
 * sendermain.c -- TCP sender
 * 02/21/2023
 *	-- Contributor: CS438 Faculty        -- Source bone code
 *                  Jie Wang & Jiaxin Wu -- TCP sender simulation 
 */

#include<iostream>
#include <unordered_map>
#include <deque>

#include "TCP.h"

using namespace std;

#define DEBUG 1

/* Global Variable */
struct sockaddr_in si_other;
int s;
socklen_t slen;

unordered_map<int, Segment> sender_window;
int cwnd = CWND_SIZE;  // Initilize
// deque<int> seq_deque[CWND_SIZE];//use to realize window 


// unsigned long long int left_packet_number;

/* Declare functions */
void diep(char s);

void reliablyTransfer(char hostname, unsigned short int hostUDPport, char filename, uint64_t bytesToTransfer);
// void sendPacket(Segment packet);

#if DEBUG
time_t start = time(NULL); // used for testing code running time
#endif

// Given function
void diep(char *s) {
    perror(s);
    exit(1);
}

/* 
 *  reliablyTransfer
 *  DESCRIPTION: TCP-like reliable transfer function
 *   reliable transmission, fast recovery and congestion avoidance
 *  OUTPUTS: none
 *  RETURN VALUE: none
 *  SIDE EFFECTS: none
 */
void reliablyTransfer(char* hostname, unsigned short int hostUDPport, char* filename, uint64_t bytesToTransfer) {
    //Open the file
    FILE *fp;
    fp = fopen(filename, "rb");
    if (fp == NULL) {
        printf("Could not open file to send.");
        exit(1);
    }

    // left_packet_number = bytesToTransfer / MSS; // TODO
	/* Determine how many bytes to transfer */

    slen = sizeof (si_other);

    if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
        diep("socket");

    memset((char *) &si_other, 0, sizeof (si_other));
    si_other.sin_family = AF_INET;
    si_other.sin_port = htons(hostUDPport);
    if (inet_aton(hostname, &si_other.sin_addr) == 0) {
        fprintf(stderr, "inet_aton() failed\n");
        exit(1);
    }

    int seq_init = 0;
    int recv_byte = -1;
    int fin_is_activated = 0;
    int SendBase = seq_init;
    int NextSeqNum = seq_init;
    int dupAckNum = 0;  // number of duplicated ACKs

	/* Send data and receive acknowledgements on s*/
    #if DEBUG
    int cpu_loop = 0;
    time_t sender_timer = time(NULL);  // To be set
    #endif 
    cout << "establishing connection..." << endl;
    
    /*Socket timer*/
    struct timeval timeout;
    timeout.tv_sec = 0;
    timeout.tv_usec = TIMEOUT;
    if (setsockopt(s, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) == -1) {
        diep("Set socket timeout error");
    }

    Segment pkt;
    Segment* ack_pkt = new Segment;
    int notACKed = 0;   // number of sent be not yet ACKed packets
    while(1){
        char read_buffer[MSS];
        
        /*======Send the data within window=======*/
        #if DEBUG
        cout << "start sending file..." << endl;
        cpu_loop++;
        #endif

        while(!fin_is_activated && (notACKed<cwnd)){ // ADD window 
            pkt.FIN = 0; 
            pkt.sequenceNum = NextSeqNum;
            int read_byte = fread(pkt.data,sizeof(char),PAYLOAD,fp);
            // cout << "readbyte is " << read_byte <<endl;

            /*Close connection*/    
            if ((read_byte < PAYLOAD) || (pkt.sequenceNum + read_byte >= bytesToTransfer)){
                pkt.FIN = 1;
                fin_is_activated = 1;
                cout << "this is the last packet " << endl;
            }
            if (pkt.sequenceNum + read_byte >= bytesToTransfer){
                
                pkt.packet_length = bytesToTransfer - pkt.sequenceNum; 
                cout << "bytesToTransfer="<<bytesToTransfer <<" ,last pkt length=" << pkt.packet_length<<endl;
            }
            else {
                pkt.packet_length = read_byte; 
            }
            // cout << pkt.data << endl;
            if (sendto(s, &pkt, sizeof(pkt), 0, (struct sockaddr *)&si_other, sizeof(si_other)) == -1){
				diep("send data error");
            }
            cout << "sending packet# "<< SendBase/PAYLOAD + notACKed << " seq num " << pkt.sequenceNum << endl; notACKed++;
            NextSeqNum +=  pkt.packet_length; 

            sender_window[pkt.sequenceNum] = pkt;
        }

        /*====Recv ACK=====*/
        recv_byte = recvfrom(s, ack_pkt, sizeof(*ack_pkt), 0, (struct sockaddr*) &si_other, &slen);
        if (recv_byte == -1) {
            if (errno == EAGAIN) {
                cout << "timeout, resend #" << SendBase/PAYLOAD << endl;
                sendto(s, &sender_window[SendBase], sizeof(pkt), 0, (struct sockaddr *)&si_other, sizeof(si_other));
                // cwnd = max(1, cwnd/2);
            }
            else {
                diep("recvfrom error");
            }
        }
        if (recv_byte == MSS){
            if (ack_pkt->ackNum > SendBase){
                
                int recvNum = int((ack_pkt->ackNum - SendBase -1) / PAYLOAD) + 1;   // number of newly received packets in this ACK
                notACKed -= recvNum;
                SendBase = ack_pkt->ackNum; /* SendBase–1: last cumulatively ACKed byte */
                dupAckNum = 0;
                cwnd ++; // slow start
                cout << "receive ack " << int((ack_pkt->ackNum-1) / PAYLOAD)+1 << ", cwnd="<<cwnd << ", notACKed="<<notACKed<< endl;
                // if (notACKed>=0){
                    // sender_timer = time(NULL);
                    // cout << "reset timer for Base#" << SendBase/PAYLOAD<<endl;
                // }else{
                //     sender_timer = NULL;
                // }
            }     
            if (ack_pkt->FIN == 1){
                cout<<"received last ack"<<endl;
                break; // Get out of the cpu loop
            }      
            if (ack_pkt->ackNum == SendBase) {
                dupAckNum++;
                // fast recovery if there are 3 duplicated ACKs
                if (dupAckNum == 3) {
                    sendto(s, &sender_window[SendBase], sizeof(pkt), 0, (struct sockaddr *)&si_other, sizeof(si_other));
                    cout << "3dupAck, resend #" << SendBase/PAYLOAD << endl;
                    cwnd = max(1, cwnd/2); // Fast recovery 
                }
            }
            
        }

    }
    cout<< "finished sending file..." << endl;

    #if DEBUG
    cout << "\ncpu runs " << cpu_loop << " times" << endl;
    cout << "Sent " << ack_pkt->ackNum << " bits in " << time(NULL)-start <<" s!"<<endl;
    #endif

    /*===END===*/
    printf("Closing the socket\n");
    close(s);
    fclose(fp);
    return;

}


int main(int argc, char** argv) {

    unsigned short int udpPort;
    unsigned long long int numBytes;

    if (argc != 5) {
        fprintf(stderr, "usage: %s receiver_hostname receiver_port filename_to_xfer bytes_to_xfer\n\n", argv[0]);
        exit(1);
    }
    udpPort = (unsigned short int) atoi(argv[2]);
    numBytes = atoll(argv[4]);



    reliablyTransfer(argv[1], udpPort, argv[3], numBytes);


    return (EXIT_SUCCESS);
}
