#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"graph.h"
#include<string>

#include <queue>

#define UNDEFINED -1

#define DEBUG 1

/**
 * Performs Dijkstra's algorithm on the given graph 
 * to find the shortest path from the source vertex to all other vertices.
 * 
 * @param source  The source vertex, index starting from 1.
 * @param graph   The Graph object representing the graph.
 *
 * @return        A pair of vectors, 
 * - the first vector represents the minimum distances from the source vertex to all other vertices,
 * - the second vector represents the predecessors of each vertex in the shortest path.
 *
 * @note 
 *  - uses a priority queue to efficiently find the minimum distance vertex in each iteration.
 *  - The returned predecessor vector may need debugging.
 */

pair<vector<int>,vector<int>> dijkstra(int source ,const Graph& graph )  {
    int num_vertices = graph.num_vertices();
    source = source - 1 ;
    #if DEBUG
    cout <<"source is " << source +1 << endl;
    #endif
    vector<int> dist(num_vertices, INFINITE);   // distance from source to other vertices
    vector<int> prev(num_vertices,UNDEFINED);
    vector<bool> visited(num_vertices, false);
    priority_queue< pair<int, int>, vector< pair<int, int> > , greater< pair<int, int> > > PQ;
    
    dist[source] = 0; // Self dist must be 0
    prev[source] = source; // self loop?
    for(int v = 0; v < num_vertices; v++){
        PQ.push(make_pair(dist[v],v));
    } // Sequence matter

    while (!PQ.empty()){
        int current_vertex = PQ.top().second; // heap top is the smallest 
        PQ.pop();

        for (const auto& neighbor : graph.neighbors(current_vertex)) {
            int neighbor_vertex = neighbor.first;
            int neighbor_cost = neighbor.second;
            int new_distance = dist[current_vertex] + neighbor_cost;

            if (new_distance < dist[neighbor_vertex] || 
               (new_distance == dist[neighbor_vertex] && current_vertex < prev[neighbor_vertex])) {
                dist[neighbor_vertex] = new_distance;
                prev[neighbor_vertex] = current_vertex;
                // update need to change, instead of add duplicate vertex!
                // add a line to modifiy the distance pf neighbor_vertex
                PQ.push(make_pair(new_distance, neighbor_vertex));
            }
        }
        
    }
    return make_pair(dist, prev);
}




/*Used for pretty print on terminal*/
void test_shortest_tree(int source, const Graph& graph){
    
    pair<vector<int>, vector<int>> dispair= dijkstra(source,graph);
    cout << "----------"<< source << "---------" <<endl;
    for (int i = 0; i < graph.num_vertices(); i++){
        cout << "dist " << i+1<<  " is " << dispair.first[i] ;
        cout << " | nexthop is " << dispair.second[i]     << endl;
    }
    
}

void output_forward_table(int source, const Graph& graph,FILE *fpOut){
    
    pair<vector<int>, vector<int>> dispair= dijkstra(source,graph);
    /*The forwarding table format should be:
        <destination> <nexthop> <pathcost> */
    for (int i = 0; i < graph.num_vertices(); i++){
        int dest = i; 
        int pathcost = dispair.first[i]; //distance from source to i 
        if(pathcost == INFINITE){
            continue;  //If a destination is not reachable, do not print its entry
        }
        int next_hop = dest; // prev[i] is the next hop? 
        while (dispair.second[next_hop] != source -1 ) {
            next_hop = dispair.second[next_hop];
        }
        // Write the forwarding table entry to the output file
        fprintf(fpOut, "%d %d %d\n", dest + 1, next_hop + 1, pathcost); 
    }
    #if DEBUG
    // Add a newline to separate different source vertex entries
    fprintf(fpOut, "\n");
    #endif
}

/**
 * Parses the message file and finds the shortest path between
 *  the source and destination vertices in the given graph.
 * 
 * @param messagefile  file containing the messages, source, and destination vertices.
 * @param graph        The Graph object representing the graph.
 *
 * @note 
 * - reads messages from the file 
 * - performs Dijkstra's algorithm to find the shortest path
 * - then prints the results (path, cost, and message).
 */
void parse_message(const string& messagefile, const Graph& graph, FILE *fpOut) {
    ifstream file(messagefile);

    if (!file.is_open()) {
        cerr << "Error opening file: " << messagefile << endl;
        return;
    }
    string line;
    while (getline(file, line)) {
        if(line.empty()){continue;}
        stringstream ss(line);
        int source, destination;
        string message;
        ss >> source >> destination;
        getline(ss, message);
        message = message.substr(1);

        if (source < 1 || source > graph.num_vertices() || destination < 1 || destination > graph.num_vertices()) {
            cout << "Error: Invalid source or destination node in message file: " << messagefile << endl;
            continue;
        }

        pair<vector<int>, vector<int>> di_pair = dijkstra(source, graph);

        int path_cost = di_pair.first[destination - 1];
        fprintf(fpOut, "from %d to %d cost ", source, destination);

        if (path_cost == INFINITE) {
            fprintf(fpOut, "infinite hops unreachable ");
        } else {
            fprintf(fpOut, "%d hops ", path_cost);
        
            // Store the path in a stack to print it in the correct order
            vector<int> path;
            int nexthop = destination - 1;
            while (nexthop != source - 1) {
                path.push_back(nexthop);
                nexthop = di_pair.second[nexthop];
            }
            path.push_back(source-1);
            // Print the path in the correct order
            for (int i = path.size() - 1; i >= 1; --i) { // why not hop to 1?
                fprintf(fpOut, "%d", path[i] + 1);
                fprintf(fpOut, " ");
            }
        }
        fprintf(fpOut, "message %s\n", message.c_str());
    }

    file.close();
    return;
}



/**
 * @brief Applies a series of changes to the graph 
 *  and updates the forwarding tables and message paths accordingly.
 * 
 * @param changesfile file containing the changes to apply to the graph.
 * @param graph  Graph object representing the network topology.
 * @param fpOut file where the forwarding tables and message paths will be written.
 * @param messagefile  file containing the messages to be sent in the network.
 */
void applyChanges(const string& changesfile, Graph& graph, FILE *fpOut,const string& messagefile) {
    ifstream file(changesfile);
    if (!file.is_open()) {
        cout << "Failed to open change file!" << std::endl;
        return;
    }
    string line;
    #if DEBUG
    int change = 1;
    #endif 
    while (getline(file, line)) {
        if (line.empty()) {continue;}
        stringstream ss(line);
        int source, destination, newcost;
        ss >> source >> destination >> newcost;
        if(newcost == -999){
            graph.delete_edge(source-1,destination-1);
        }else{
            graph.delete_edge(source-1,destination-1);
            graph.add_edge(source-1,destination-1, newcost);
        }
        #if DEBUG
        cout << change << "th change:" << endl;
        graph.print_graph();
        change++;
        #endif
        for(int i = 1; i <= graph.num_vertices(); i++){
            #if DEBUG
            // test_shortest_tree(i,graph);
            #endif
            output_forward_table(i,graph,fpOut);
        }
        parse_message(messagefile,graph,fpOut);
    }
   
    file.close();
}


int main(int argc, char** argv) {
    //printf("Number of arguments: %d", argc);
    if (argc != 4) {
        printf("Usage: ./linkstate topofile messagefile changesfile\n");
        return -1;
    }
    string topofile = argv[1];
    string messagefile = argv[2];
    string changesfile = argv[3];

    Graph graph;
    create_graph(topofile, graph);
    #if DEBUG
    cout << "Graph created successfully!" << endl;
    cout << "Graph representation:" << endl;
    graph.print_graph();
    #endif
    FILE *fpOut;
    fpOut = fopen("output.txt", "w");

    for(int i = 1; i <= graph.num_vertices(); i++){
        // test_shortest_tree(i,graph);
        output_forward_table(i,graph,fpOut);
    }
    #if DEBUG
    cout << "=====complete first step=====" <<endl;
    #endif
    parse_message(messagefile,graph,fpOut);
    #if DEBUG
    cout << "=====complete parse original msg step=====" <<endl;
    #endif
    applyChanges(changesfile,graph,fpOut,messagefile);

    #if DEBUG
    cout << "=====all clear=====" <<endl;
    #endif
    fclose(fpOut);
    return 0;
}