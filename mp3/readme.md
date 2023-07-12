# MP3
distvec.cpp    WJX  
linkstate.cpp  WJ  

## functions
input  
- create_graph(topofile)
- parse_msg(msg_file)
- 
output  
send msg  

## data structure
Topo map: graph -- adjacency_list, done
Forwarding table  <destination> <nexthop> <pathcost> -- where to store it?


## Instructions

A line in the **topology** file represents a link between two nodes and is structued this way:  
<ID of a node> <ID of another node> <cost of the link between them>

A line in the **message** file looks like  
<source node ID> <dest node ID> <message text>

Example **changes** file:  
2 4 1
2 4 -999
This would add a cost 1 link between 2 and 4, and then remove it afterwards

### Output format:  
Write all output described in this section to a file called "output.txt".
The **forwarding table format** should be:
<destination> <nexthop> <pathcost>  
where nexthop is the neighbor we hand destination's packets to, and pathcost is the total cost of this path to destination. The table should be sorted by destination.  

When a message is to be sent, print the **source, destination, path cost, path taken** (including the
source, but NOT the destination node), and message contents in the following format:
"from <x> to <y> cost <path_cost> hops <hop1> <hop2> <...> message <message>"  
e.g. : "from 2 to 1 cost 6 hops 2 5 4 message here is a message from 2 to 1"  
Print messages in the order they were specified in the messages file.  
 If the destination is not reachable, please say "from <x> to <y> cost infinite hops unreachable message <message>"  

 Both messagefile and changesfile can be empty. In this case, the program should just print the
forwarding table.  

```
/* Algorithm
1  function Dijkstra(Graph, source):
2      dist[source] ← 0                           // Initialization
3
4      create vertex priority queue Q
5
6      for each vertex v in Graph.Vertices:
7          if v ≠ source
8              dist[v] ← INFINITY                 // Unknown distance from source to v
9              prev[v] ← UNDEFINED                // Predecessor of v
10
11         Q.add_with_priority(v, dist[v])
12
13
14     while Q is not empty:                      // The main loop
15         u ← Q.extract_min()                    // Remove and return best vertex
16         for each neighbor v of u:              // Go through all v neighbors of u
17             alt ← dist[u] + Graph.Edges(u, v)  // alternative way, If this path is shorter than 
18             if alt < dist[v]:                   // the current shortest path recorded for v, 
19                 dist[v] ← alt                  // that current path is replaced with this alt path
20                 prev[v] ← u
21                 Q.decrease_priority(v, alt)
22
23     return dist, prev
*/
```
- Ineffiecient approach, fail 
```
    for (int i = 0; i < num_vertices; i++) {
        int min_distance = INFINITE;
        int current_vertex = -1;

        // Find the minimum distance vertex
        for (int v = 0; v < num_vertices; v++) {
            if (!visited[v] && dist[v] < min_distance) {
                min_distance = dist[v];
                current_vertex = v;
            }
        }

        visited[current_vertex] = true;

        for (const auto& neighbor : graph.neighbors(current_vertex)) {
            int neighbor_vertex = neighbor.first;
            int neighbor_cost = neighbor.second;
            int new_distance = dist[current_vertex] + neighbor_cost;

            if (new_distance < dist[neighbor_vertex] ||
                (new_distance == dist[neighbor_vertex] && current_vertex < prev[neighbor_vertex])) {
                dist[neighbor_vertex] = new_distance;
                prev[neighbor_vertex] = current_vertex;
            }
        }
    }
```



## Test cases  

test results: 
- Simple topology has an error - [10]
- Two paths with equal costs test failed. Tie breaker applied? 
- Path change to unreachable failed 
- Link addition failed. Tie breaker applied? 
- Topology in MP instructions failed 
- Changes to topology in MP instructions failed 
- Changes to topology in MP instructions, 1 path unreachable failed 
- Multiple changes to topology in MP instructions failed 
- 8 node topology failed 
 -10: DV: Simple topology has an error 
- DV: Two paths with equal costs test failed. Tie breaker applied? 
- DV: Path change to unreachable failed 
- DV: Link addition failed. Tie breaker applied? 
- DV: Topology in MP instructions failed 
- DV: Changes to topology in MP instructions failed 
- DV: Changes to topology in MP instructions, 1 path unreachable failed 
- DV: Multiple changes to topology in MP instructions failed 
- DV: 8 node topology failed 

