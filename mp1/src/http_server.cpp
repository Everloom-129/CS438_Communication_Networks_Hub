/*
 * server.c -- a stream socket server 
 *  -- Contributor: Beej&CS438 Faculty  -- Source bone code
 *                  Jie Wang & Jiaxin Wu -- Deal with request msg, send corrsponding file
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

#define BACKLOG 10	 // how many pending connections queue will hold
#define BUF_SIZE 1000

void sigchld_handler(int s)
{
	while(waitpid(-1, NULL, WNOHANG) > 0);
}

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{
	int sockfd, new_fd;  // listen on sock_fd, new connection on new_fd
	struct addrinfo hints, *servinfo, *p;
	struct sockaddr_storage their_addr; // connector's address information
	socklen_t sin_size;
	struct sigaction sa;
	int yes=1;
	char s[INET6_ADDRSTRLEN];
	int rv;

	if (argc != 2) {
	    fprintf(stderr,"usage: ./http_server port\n");
	    exit(1);
	}

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE; // use my IP

	if ((rv = getaddrinfo(NULL, argv[1], &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and bind to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
				p->ai_protocol)) == -1) {
			perror("server: socket");
			continue;
		}

		if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
				sizeof(int)) == -1) {
			perror("setsockopt");
			exit(1);
		}

		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("server: bind");
			continue;
		}

		break;
	}

	if (p == NULL)  {
		fprintf(stderr, "server: failed to bind\n");
		return 2;
	}

	freeaddrinfo(servinfo); // all done with this structure

	if (listen(sockfd, BACKLOG) == -1) {
		perror("listen");
		exit(1);
	}

	sa.sa_handler = sigchld_handler; // reap all dead processes
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;
	if (sigaction(SIGCHLD, &sa, NULL) == -1) {
		perror("sigaction");
		exit(1);
	}

	printf("server: waiting for connections...\n");

	while(1) {  // main accept() loop
		sin_size = sizeof their_addr;
		new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
		if (new_fd == -1) {
			perror("can't accept more socket fd");
			continue;
		}

		inet_ntop(their_addr.ss_family,
			get_in_addr((struct sockaddr *)&their_addr),
			s, sizeof s);
		printf("server: got connection from %s\n", s);

		if (!fork()) { // this is the child process
			close(sockfd); // child doesn't need the listener

			// receive request from client
			char req_buf[BUF_SIZE];
			// cout << "req_buf created" << endl; // TEST
			if (recv(new_fd, req_buf, BUF_SIZE, 0) == -1){
				perror("recv");
				cout << "can not recieve" <<endl;
				close(new_fd);
				exit(0);
			}
			// TEST
			cout << "receives: "<< endl <<req_buf << endl;
			string req = string(req_buf);
			
			int idx = req.find("HTTP/1.1");
			// cout <<"idx "<<idx<<endl;
			if (idx == string::npos) {
				string header = "HTTP/1.1 400 Bad Request\r\n\r\n";
				if (send(new_fd, header.c_str(), header.length(), 0) == -1){
					perror("send400");
					cout << "can not send back" <<endl;
					close(new_fd);
					exit(0);
				}
			}
			string file_path = req.substr(4, idx-1-4);
			if (file_path[0] == '/') {
				file_path = file_path.substr(1);
			}
			// cout <<"file_path: "<<file_path <<endl; // TEST 

			FILE* file_pointer = fopen(file_path.c_str(), "rb");
			if (!file_pointer) {
				string header = "HTTP/1.1 404 Not Found\r\n\r\n";
				if (send(new_fd, header.c_str(), header.length(), 0) == -1)
					perror("send404");
				close(new_fd);
				cout << "Child process finished, close fd" << endl;
				exit(0);
				
			}
			else { 
				
				/*Valid Header send first*/
				char str_buffer[BUF_SIZE];
				string header = "HTTP/1.1 200 OK\r\n\r\n";
				send(new_fd,header.data(), (header).length(),0);
				
				int numbytes = 1;

				while(numbytes > 0) {
					numbytes = fread(str_buffer, 1, BUF_SIZE, file_pointer);
					if(numbytes == 0){
						break;
					}
					// cout << numbytes;
					if(send(new_fd, str_buffer, numbytes,0) == -1){
						perror("send200");
						cout << "can not send file" <<endl;
						close(new_fd);
						exit(0);
					}

					memset(str_buffer,'\0',BUF_SIZE);
				}

			}
			
			close(new_fd);
			exit(0);
			
		}
		close(new_fd);  // parent doesn't need this
	}
	
	return 0;
}
