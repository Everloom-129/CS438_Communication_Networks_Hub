# CS438 Assignment 4

04/27/2023

***Wang, Jie  [jiew5]***
***Wu, Jiaxin [jiaxin19]***



## 1. BGP Policy

![image-20230427205902434](./CS438_Assignment_4.assets/image-20230427205902434.png)

![image-20230427210005765](./CS438_Assignment_4.assets/image-20230427210005765.png)

### 1. ASes to X:

- A: A, D, C, Z, X
- B: B, A, D, C, Z, X
- C: C, Z ,X 
- D: D, C, Z, X
- V: V, W, Z, X
- W: W, Z, X
- X: X
- Y: Y, Z, X
- Z: Z, X

### 2. Y hate W

Yes, it is possible.

Y can still reach all ASes by the following paths:

A: Y, Z, C, D, A
B: Y, Z, C, D, A, B
C: Y, Z, C
D: Y, Z, C, D
V: Y, Z, C, D, A, V
X: Y, Z, X
Y: Y
Z: Y, Z

### 3.  W hate X

Yes, it is possible.

X can still reach all ASes by the following paths:
A: X, Z, C, D, A
B: X, Z, C, D, A, B
C: X, Z, C
D: X, Z, C, D
V: X, Z, C, D, A, V
X: X
Y: X, Z, Y
Z: X, Z






## 2. SDNs

![image-20230427210030857](./CS438_Assignment_4.assets/image-20230427210030857.png)

![image-20230427210043711](./CS438_Assignment_4.assets/image-20230427210043711.png)

![image-20230427210107821](./CS438_Assignment_4.assets/image-20230427210107821.png)

### 1. 
Matching rule: (source ip = 10.1.0.2 or source ip = 10.3.0.5) and dest ip = 10.2.0.3
Action: forward to 3
Matching rule: (source ip = 10.1.0.2 or source ip = 10.3.0.5) and dest ip = 10.2.0.4
Action: forward to 4
### 2. 
Matching rule: TCP and dest ip = 10.2.0.3
Action: forward to 3
Matching rule: TCP and dest ip = 10.2.0.4
Action: forward to 4
### 3. 
Matching rule: dest ip = 10.2.0.4
Action: forward to 4
### 4. 
Matching rule: source ip = 10.3.0.6 and source ip = 10.3.0.5 and dest ip = 10.2.0.3
Action: forward to 3





## 3. Synthesis

![image-20230429152238209](./CS438_Assignment_4.assets/image-20230429152238209.png)

![image-20230429152537556](./CS438_Assignment_4.assets/image-20230429152537556.png)

![image-20230429152626911](./CS438_Assignment_4.assets/image-20230429152626911.png)



## 4. Error Detection

![image-20230427213055209](./CS438_Assignment_4.assets/image-20230427213055209.png)

### 1. Parity Check 

#### (a) 1

#### (b) 4+4 +1 = 9

#### (c) array:

#### (d)
In this example, the first, second and fifth bits are flipped, but the parity bits remain the same, so two-dimensional parity cannot detect the 3 errors.
#### (e)

- Advantage: 2D parity can self-detect and correct single-bit errors. It is more powerful

- Disadvantage: 2D parity requires more parity bits, increasing the overhead and space complexity



### 2. CRC

![image-20230427213527407](./CS438_Assignment_4.assets/image-20230427213527407.png)

#### (a) Shown below:

TODO

#### (b) 1110011 10001001 11001110

#### (c) The receiver divides the received bit stream <D,R> by G using modulo 2 long division. If the remainder is not zero, error is detected.

#### (d) Shown below





### 3. Checksum

![image-20230427213806999](./CS438_Assignment_4.assets/image-20230427213806999.png)

0x7EFF=0111 1110 1111 1111
0xAAC8=1010 1010 1100 1000
0xEC05=1110 1100 0000 0101
0x7EFF+0xAAC8=1 0010 1001 1100 0111
Wrap around: 0x7EFF+0xAAC8=0010 1001 1100 1000
0x7EFF+0xAAC8+0xEC05=1 0001 0101 1100 1101
Wrap around: 0x7EFF+0xAAC8+0xEC05=0001 0101 1100 1110
1’s complement sum=1110 1010 0011 0001.

## 5. 


### 1.
At round i, each node can wait $0, 1, …, 2^{(i-1)}-1$ slots, all $ 2^{i-1}$ choices having $\frac{1}{2^{i-1}} $ probability.
A collision happens in i-th round if A and B both choose to wait k slots, where $k=0, 1, …, 2^{i-1}-1$, the probability is $ 2^{i-1}*\frac{1}{2^{i-1}}*\frac{1}{2^{i-1}}=\frac{1}{2^{i-1}} $.

### 2.
The first success happens at the exactly i-th rounds if there are collisions in the first (i-1) rounds and success in the i-th round.
$$
\begin{align}
p1=& 1-\frac{1}{2^{1-1}}=0 \\
p2=& \frac{1}{2^{1-1}}*(1-\frac{1}{2^{2-1}})=\frac{1}{2}\\
p3=& \frac{1}{2^{1-1}}*\frac{1}{2^{2-1}}*(1-\frac{1}{2^{3-1}})=\frac{3}{8}\\
p3=& \frac{1}{2^{1-1}}*\frac{1}{2^{2-1}}*\frac{1}{2^{3-1}}*(1-\frac{1}{2^{4-1}})=\frac{7}{64}

\end{align}
$$

### 3.
For A, since 2 collisions have occurred, A can wait 0,1,2,3 slots until the next transmission.
For B, since 3 collisions have occurred, B can wait 0,...,7 slots until the next attempt.
In the case A wins the channel for the next packet, if A wait i slot, then B should wait more than i slots. 

If i=0, the probability is  $\frac{1}{4} \times \frac{7}{8}=\frac{7}{32}$
If i=1, the probability is $\frac{1}{4} \times \frac{6}{8}=\frac{6}{32}$
If i=2, the probability is $\frac{1}{4} \times \frac{5}{8}=\frac{5}{32}$
If i=3, the probability is $\frac{1}{4} \times \frac{4}{8}=\frac{4}{32}$
The total probability is $\frac{7}{32}+\frac{6}{32}+\frac{5}{32}+\frac{4}{32}=\frac{11}{16}$





## 6. Wireless

### 1. 
F(A)B, A(B)C, B(C)D, E(A)B

### 2.
