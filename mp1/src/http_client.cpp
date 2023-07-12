/*
 * http_client.c -- a stream socket client 
 *	-- Contributor: Beej&CS438 Faculty  -- Source bone code
 *                  Jie Wang & Jiaxin Wu -- Connect msg to server, pretend as a wget program
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include <arpa/inet.h>

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#define MAXDATASIZE 1500 // max number of bytes we can get at once 




// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}
// Usage: ./http_client http://xx.xx.xx.xx/somefile.xx 
// Take ip into argv[1]
// TODO: port?
int main(int argc, char *argv[])
{
	int sockfd, numbytes;  
	char buf[MAXDATASIZE];
	struct addrinfo hints, *servinfo, *p;
	int rv;
	char s[INET6_ADDRSTRLEN];

	if (argc != 2) {
	    fprintf(stderr,"usage: ./http_client hostname\n");
	    exit(1);
	}

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;

	/* URL parse */
	string url = argv[1];
	url = url.substr(7);
	int idx = url.find_first_of('/');
	string host = url.substr(0, idx);
	size_t found = host.find(':');
	string port = "80";
	if (found != string::npos) {
    	port = host.substr(found+1, idx);
        host = host.substr(0, found);
	}

	string path = url.substr(idx+1);
	// cout << "host:" << host << " port:" << port << " path: " << path << endl;
	// Connected to the address
	if ((rv = getaddrinfo(host.c_str(), port.c_str(), &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and connect to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
				p->ai_protocol)) == -1) {
			perror("client: socket");
			continue;
		}

		if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("client: connect");
			continue;
		}

		break;
	}

	if (p == NULL) {
		fprintf(stderr, "client: failed to connect\n");
		return 2;
	}

	inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
			s, sizeof s);
	printf("client: connecting to %s\n", s);

	freeaddrinfo(servinfo); // all done with this structure


	/*Connect to server, GET sth from it*/
	string request = "GET "+ path + " HTTP/1.1" + "\r\n"
	+ "User-Agent:  Wget/1.12 (linux-gnu)" +"\r\n"
	+ "Host: " + host +  ":" + port +"\r\n"
	+ "Connection: Keep-Alive" +"\r\n"; 

	cout << request << endl; // TEST
	
	// Response output generation
	const char* request_buf = request.c_str(); 
	send(sockfd,request_buf,strlen(request_buf),0); 

	/*Write response into output*/
	ofstream new_file("./output",ios::binary); // The object to store response data
	if (!new_file) {
    	std::cerr << "Failed to open file:output." << std::endl;
    	return 1;
  	}


	memset(buf,'\0',MAXDATASIZE);
	/*Improved as while-loop to recv multiple packets from server*/
	while ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) > 0) {
		cout<< "------------------" <<endl;			//TEST	
		// cout << "BUF contents:   " << buf << endl; //  TEST
		string check_header(buf); 
		int pos = check_header.find("\r\n\r\n");

		if(pos != string::npos){
			string substr = check_header.substr(0, pos+4);
      		cout << substr << endl; // Print header
			new_file << check_header.substr(pos + 4 );
			// buf = (check_header.substr(pos + 4 ) ).c_str();
		}else{
			// handle header, don't show on the screen
			new_file << check_header;
		}
	    // clean the response buf
		memset(buf,'\0',MAXDATASIZE);
		check_header.clear();
	}


	printf("client: received file\n");

	new_file.close();
	close(sockfd);

	return 0;
}

