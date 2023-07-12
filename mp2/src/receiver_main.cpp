/*
 * receiver_main.c -- TCP sender
 * 02/21/2023
 *	-- Contributor: CS438 Faculty        -- Source bone code
 *                  Jie Wang & Jiaxin Wu 
 */

#include <iostream>
#include <unordered_map>
#include "TCP.h"

using namespace std;

/*Global Variable*/
struct sockaddr_in si_me, si_other;
int s;
socklen_t slen;
FILE* fp;
unordered_map<int, Segment*> buf;
int delayedACK = 0; // flag for waiting for delayed ACK
int lastPkt = 0; // flag to check whether this is the last packet

void diep(char *s) {
    perror(s);
    exit(1);
}

/**
 * Send ack packet with ackNum to the sender.
 *
 * @param ackNum The acknowledge number to be sent.
 * TODO: twice time send ack?
 */
void sendAck(int ackNum) {
    Segment pkt;
    pkt.ackNum = ackNum;
    if (lastPkt) {
        pkt.FIN = 1;
    }
    memset(pkt.data, 0, MSS-18);
    if (sendto(s, &pkt, sizeof(pkt), 0, (struct sockaddr*) &si_other, slen)==-1) {
        diep("send ack error");
    }
    cout << "sent ack " << int((ackNum-1) / PAYLOAD)+1 << endl;
}

/**
 * Writes buf data to the destination file starting from the packet with seqNum.
 *
 * @param seqNum The sequence number of the packet from which to start writing.
 *
 * @return The sequence number of the next packet that needs to be written to the file.
 */
int writeFile(int seqNum) {
    cout << "writing file" << endl;
    Segment* pkt = buf[seqNum];
    fwrite(pkt->data, sizeof(char), pkt->packet_length, fp);
    buf.erase(seqNum);
    // if it is the last packet
    if (pkt->FIN == 1) {
        lastPkt = 1;
    }
    int nextSeg = seqNum+pkt->packet_length;

    while (buf.count(nextSeg)>0) {  // write to file if the next packet is already in buffer
        Segment* pkt = buf[nextSeg];
        if (pkt->FIN == 1) {
            lastPkt = 1;
        }
        fwrite(pkt->data, sizeof(char), pkt->packet_length, fp);
        buf.erase(nextSeg);
        nextSeg += pkt->packet_length;
    }
    return nextSeg;
}


/* 
 *  reliablyReceive
 *  DESCRIPTION: 
 *  INPUTS: 
 *      -- unsigned short int myUDPport
 *      -- char* destinationFile
 *  OUTPUTS: none
 *  RETURN VALUE: none
 *  SIDE EFFECTS: none
 */


void reliablyReceive(unsigned short int myUDPport, char* destinationFile) {
    fp = fopen(destinationFile, "wb");

    slen = sizeof (si_other);


    if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
        diep("socket");

    memset((char *) &si_me, 0, sizeof (si_me));
    si_me.sin_family = AF_INET;
    si_me.sin_port = htons(myUDPport);
    si_me.sin_addr.s_addr = htonl(INADDR_ANY);
    printf("Now binding\n");
    if (bind(s, (struct sockaddr*) &si_me, sizeof (si_me)) == -1)
        diep("bind");
 

	/* Now receive data and send acknowledgements */    
    int expectedSeqNum = 0; // expected sequence number
    int receivedBytes;      // number of bytes received
    // time_t receiver_timer = NULL;

    while (true) {
        Segment* pkt = new Segment;  // 
        receivedBytes = recvfrom(s, pkt, sizeof(*pkt), 0, (struct sockaddr*) &si_other, &slen);
        if (receivedBytes == -1) diep("recvfrom error");
        // cout << "Received Bytes: " << receivedBytes << endl;
        cout << "Received pkt# " << int((pkt->sequenceNum-1)/PAYLOAD)+1;
        cout<< " seq# "<<pkt->sequenceNum<<endl;
        // cout << "received data: " << pkt->data << endl;
        if (pkt->sequenceNum > expectedSeqNum) {
            // cout <<"if case"<<endl;
            buf[pkt->sequenceNum] = pkt;
            cout << "sent dup ACK#" << expectedSeqNum/PAYLOAD <<endl;
            sendAck(expectedSeqNum);    // send duplicated ACK for last in-order packet
        }else if (pkt->sequenceNum == expectedSeqNum) {
            // cout << "else if case" << endl;
            buf[pkt->sequenceNum] = pkt;
            // cout << "current buf: " ;
            // for (const auto& pair : buf) {
            //     std::cout << pair.first << " ";
            // }
            // cout << endl;
            // int receivedSeqNum = expectedSeqNum;
            // expectedSeqNum = cumACK(expectedSeqNum);
            expectedSeqNum = writeFile(expectedSeqNum);

            sendAck(expectedSeqNum);    // send ACK for next expected packet
            // writeFile(receivedSeqNum); // write data to file
        } 
        else {
            cout << "sent dup ACK#" << (expectedSeqNum-1)/PAYLOAD+1 <<endl;
            sendAck(expectedSeqNum); // send ACK for last in-order packet
        }
        if (lastPkt == 1) {
            for (int i=0; i < 5; i++) {
                sendAck(expectedSeqNum);
            }
            break;
        }
    }
    close(s);
    fclose(fp);
	printf("%s received.\n\n", destinationFile);
    return;
}

/*
 * 
 */
int main(int argc, char** argv) {

    unsigned short int udpPort;

    if (argc != 3) {
        fprintf(stderr, "usage: %s UDP_port filename_to_write\n\n", argv[0]);
        exit(1);
    }

    udpPort = (unsigned short int) atoi(argv[1]);

    reliablyReceive(udpPort, argv[2]);
}

