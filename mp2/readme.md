# MP2 reliable packet transfer

## Requirement

Use UDP **SOCK_DGRAM (UDP)** to implement your own version of TCP. 

- tolerate packet drops, 
- allow other concurrent connections a fair chance, 
- must not be overly nice to other connections (should not give up the entire bandwidth to other
connections)


## Function prototype
### sender_main.c
WJ
- void reliablyTransfer(char* hostname, unsigned short int hostUDPport, char* filename, unsigned long long int bytesToTransfer).
> This function should transfer the first bytesToTransfer bytes of filename to the receiver at hostname: hostUDPport correctly and efficiently, even if the network drops or reorders some of your packets. 
- Congestion control 

  important, 20MB sender test

- URL parse?
  No need, this is handled by Test program
- 


### receiver_main.c
WJX
- void reliablyReceive(unsigned short int myUDPport, char* destinationFile)
> This function is counterpart to reliablyTransfer , and should write what it receives to a file called **destinationFile**.






## Points: 
If our code can pass all the test case, that is fine
test results:

Test 1: sanity check: transfer single byte failed: wrote 0 of 1 (text: ).

Test 2: transfer 50K failed: only received 0 of 50000 after 6s.

Test 3: utilize empty link failed: 0 of 65000000 were written.

Test 6: quick convergence failed: failed to send 20MB in 20s (receiver wrote 0 bytes)

Test 7: TCP friendliness failed: your process died or ended early. (note: it's being given 999000999000 as the numBytes argument)

Test 8: TCP friendliness with 1% loss failed: your process died or ended early. (note: it's being given 999000999000 as the numBytes argument)
Q: where is T4, T5?
- There are no test 4,5 for this MP. We removed these tests to make the MP less challenging.
Q: how to avoid the problem of multiple RTT problem
- However, sometimes will come out **infinite loop problem**, it is because the missing side effect of test 4, 5. The key is not to send too much packet at one time( never infinite loop sending pkt)


## Test Case:
- 391.txt
- t391.txt -- 391.txt copy-paste*3
- 10 mb test case
- 50 MB txt file 


## test environment
- Limited to 20Mbps connection, and a 20ms RTT.
- http://fa21-cs438-01.cs.illinois.edu:8080/queue/queue_mp2.html 
- 