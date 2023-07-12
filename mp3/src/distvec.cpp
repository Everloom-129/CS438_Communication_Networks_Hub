#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"graph.h"

using namespace std;

#define DEBUG 0

// forw_table:<<path_cost,next_hop>>
set<int> toUpdate;  // set of nodes to be updated
int num_vertices;

void init_tables(Graph& graph) {
    num_vertices = graph.num_vertices();
    vector<vector<vector<pair<int, int>>>> all_tables(num_vertices, vector<vector<pair<int, int>>>(num_vertices, vector<pair<int, int>>(num_vertices, make_pair(INFINITE,-2))));
    graph.set_all_table(all_tables);
    // Initialize the distance vector with direct edge costs
    for (int i = 0; i < num_vertices; ++i) {
        vector<vector<pair<int, int>>> forw_table = graph.get_table(i);
        forw_table[i][i] = make_pair(0, i);
        for (const auto& neighbor : graph.neighbors(i)) {
            // cout << "neighbor: "<< neighbor.first << ',' << neighbor.second<< endl;
            int j = neighbor.first;
            int edge_cost = neighbor.second;
            forw_table[i][j] = make_pair(edge_cost,j);
        }
        graph.set_table(i, forw_table);
        #if DEBUG
        cout << "init forw table for node " <<i+1<<endl;
        for (int j = 0; j < num_vertices; ++j) {
            for (int k = 0; k < num_vertices; ++k) {
                cout << '('<<graph.get_table(i)[j][k].first<<','<<graph.get_table(i)[j][k].second+1<<") ";
            }
        cout<<endl;
        }
        #endif 
    }
    for (int i=0; i<num_vertices; ++i) {
        toUpdate.insert(i);
    }
}

// Update the distance vector using the Bellman-Ford algorithm
void update_tables(Graph& graph) {
    while (!toUpdate.empty()) {
        int i = *toUpdate.begin();
        #if DEBUG
        // cout <<"updating "<<i+1<<endl;
        #endif
        vector<vector<pair<int, int>>> forw_table = graph.get_table(i);

        // get updated distance vector from its neighbors
        for (const auto& neighbor : graph.neighbors(i)) {
            int j = neighbor.first;
            forw_table[j] = graph.get_table(j)[j];
        }

        // update its own distance vector
        for (int j = 0; j < num_vertices; ++j) {
            for (const auto& neighbor : graph.neighbors(i)) {
                int k = neighbor.first;
                int edge_cost = neighbor.second;
                if (forw_table[i][k].first != INFINITE && forw_table[k][j].first != INFINITE &&
                    edge_cost + forw_table[k][j].first < forw_table[i][j].first) {
                    forw_table[i][j].first = forw_table[i][k].first + forw_table[k][j].first;
                    forw_table[i][j].second = forw_table[i][k].second;
                    for (const auto& neighbor : graph.neighbors(i)) {
                        toUpdate.insert(neighbor.first);
                    }
                }
                // when two equally good paths are available, choose the one whose next-hop node ID is lower
                else if (edge_cost + forw_table[k][j].first == forw_table[i][j].first &&
                        forw_table[i][j].second > forw_table[i][k].second) {
                            forw_table[i][j].second = forw_table[i][k].second;
                            for (const auto& neighbor : graph.neighbors(i)) {
                                toUpdate.insert(neighbor.first);
                            }
                }
            }
        }
        graph.set_table(i,forw_table);
        #if DEBUG
        cout << "updated forw table for node " <<i+1<<endl;
        for (int j = 0; j < num_vertices; ++j) {
            for (int k = 0; k < num_vertices; ++k) {
                cout << '('<<graph.get_table(i)[j][k].first<<','<<graph.get_table(i)[j][k].second+1<<") ";
            }
            cout<<endl;
        }
        #endif

        toUpdate.erase(i);
        #if DEBUG // WJ: seems buggy here
        // cout<< "to update:";
        // for (int i : toUpdate) {
        //     cout <<i+1<<' ';
        // }
        // cout<<endl;
        #endif
        
    }
    #if DEBUG
    // cout<<"nothing to update"<<endl;
    #endif
}


string parse_send_msg(const string& messagefile, const Graph& graph) {
    ifstream file(messagefile);
    string output;
    if (!file.is_open()) {
        cerr << "Error opening file: " << messagefile << endl;
        return output;
    }
    string line;
    
    while (getline(file, line)) {
        if (line.empty()) {continue;}
        stringstream ss(line);
        int source, destination;
        string message, temp;

        ss >> source >> destination;

        // Read the rest of the line as the message
        getline(ss, message);
        message = message.substr(1); // Remove the leading space

        output += send_msg(source-1, destination-1, message, graph);
    }

    file.close();
    return output;
}

string table_output(Graph graph) {
    string output;
    for (int i = 0; i < num_vertices; i++) {
        for (int j = 0; j < num_vertices; j++) {
            output += to_string(j+1)+' ';
            output += to_string(graph.get_table(i)[i][j].second+1)+' ';
            output += to_string(graph.get_table(i)[i][j].first)+'\n';
        }
    }
    return output;
}



void applyChanges(const string& changesfile, Graph& graph, FILE *fpOut,const string& messagefile) {
    ifstream file(changesfile);
    if (!file.is_open()) {
        cout << "Failed to open change file!" << std::endl;
        return;
    }
    string line;
    #if DEBUG
    int change = 0;
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
        init_tables(graph);
        update_tables(graph);
        fprintf(fpOut, "%s", table_output(graph).c_str());

        fprintf(fpOut, "%s", parse_send_msg(messagefile, graph).c_str());

    }
   
    file.close();
}



int main(int argc, char** argv) {
    //printf("Number of arguments: %d", argc);
    if (argc != 4) {
        printf("Usage: ./distvec topofile messagefile changesfile\n");
        return -1;
    }

    string file_path = argv[1];
    string messagefile = argv[2];
    string changesfile = argv[3];

    Graph graph;
    create_graph(file_path, graph);
    #if DEBUG
    cout << "Graph created successfully!" << endl;
    cout << "Graph representation:" << endl;
    #endif
    graph.print_graph();

    // to do: write to output
    FILE *fpOut;
    fpOut = fopen("output.txt", "w");
    
    init_tables(graph);
    
    update_tables(graph);

    fprintf(fpOut, "%s", table_output(graph).c_str());
    fprintf(fpOut, "%s", parse_send_msg(messagefile, graph).c_str());

    // to do: apply changes to edge cost
    applyChanges(changesfile, graph,fpOut,messagefile);


    
    fclose(fpOut);
    return 0;
}

