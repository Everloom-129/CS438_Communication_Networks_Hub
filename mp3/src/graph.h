#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <set>
#include <algorithm>

using namespace std;

#define INFINITE 999


class Graph {
public:
    Graph() {}

    void add_vertex() {
        adjacency_list.emplace_back();
    }

    void add_edge(int u, int v, int cost) {
        if (u==v){
            adjacency_list[u].emplace_back(v, 0);
        }else{
        adjacency_list[u].emplace_back(v, cost);
        adjacency_list[v].emplace_back(u, cost); // TODO: remove duplicate case
        }
    }


    void change_edge(int u, int v, int change) {
        for (auto &e : adjacency_list[u]) {
            if (e.first==v) {
                e.second += change;
                break;
            }
        }
        for (auto &e : adjacency_list[v]) {
            if (e.first==u) {
                e.second += change;
                break;
            }
        }
        
    }

    void delete_edge(int u, int v) {
        if(u != v ){
            adjacency_list[u].erase(
                remove_if(adjacency_list[u].begin(), adjacency_list[u].end(),
                [&](const std::pair<int, int>& e) {
                    return e.first == v;
                }),
            adjacency_list[u].end()
            );
            adjacency_list[v].erase(
                remove_if(adjacency_list[v].begin(), adjacency_list[v].end(),
                [&](const std::pair<int, int>& e) {
                    return e.first == u;
                }),
            adjacency_list[v].end()
            );
        }
        
    }

    const vector<pair<int, int>>& neighbors(int vertex) const {
        return adjacency_list[vertex];
    }

    int num_vertices() const {
        return adjacency_list.size();
    }

    void print_graph() const {
        for (int i = 0; i < adjacency_list.size(); ++i) {
            cout << "Vertex " << (i + 1) << ": ";
            for (const auto& neighbor : adjacency_list[i]) {
                cout << "(" << (neighbor.first + 1) << ", " << neighbor.second << ") ";
            }
            cout << endl;
        }
    }
    void output_graph(FILE* fpOut) const {
        for (int i = 0; i < adjacency_list.size(); ++i) {
            fprintf(fpOut, "Vertex %d: ", i + 1);
            for (const auto& neighbor : adjacency_list[i]) {
                fprintf(fpOut, "(%d, %d) ", neighbor.first + 1, neighbor.second);
            }
            fprintf(fpOut, "\n");
        }
    }

    const vector<vector<pair<int, int>>>& get_table(int vertex) const {
        return all_tables[vertex];
    }

    void set_table(int vertex, vector<vector<pair<int, int>>>& forw_table) {
        all_tables[vertex] = forw_table;
    }

    void set_all_table(vector<vector<vector<pair<int, int>>>>& t) {
        all_tables = t;
    }

    vector<int> find_path(int source, int dest) const {
        cout<<"finding path from "<< source+1<< " to "<<dest+1<<endl;
        vector<int> path;

        if (source == dest) {
            return path;
        }
        
        int curr = source;
        while (curr != dest) {
            curr = all_tables[curr][curr][dest].second;
            // cout<<"curr:"<<curr+1<<endl;
            path.push_back(curr);
        }
        path.pop_back();
        // cout<<"path from "<<source+1 << " to " << dest+1 <<endl;
        // for (int i:path) {
        //     cout<<i<<' ';
        // }
        return path;
    }


private:
    vector<vector<pair<int, int>>> adjacency_list;
    vector<vector<vector<pair<int, int>>>> all_tables;
};


void create_graph(const string& file_path, Graph& graph) {
    ifstream file(file_path);

    int u, v, cost, max_vertex = 0;
    while (file >> u >> v >> cost) {
        max_vertex = max(max_vertex, max(u, v));
    }

    for (int i = 0; i < max_vertex; ++i) {
        graph.add_vertex();
    }

    file.clear();
    file.seekg(0, ios::beg);

    while (file >> u >> v >> cost) {
        graph.add_edge(u - 1, v - 1, cost); // Assuming vertices are 1-indexed in the input file
    }

    file.close();
}

/**
 * Sends a message from a source vertex to a destination vertex in the given graph.
 * 
 * @param source    The source vertex, index starting from 0.
 * @param dest      The destination vertex, index starting from 0.
 * @param msg       The message to be sent.
 * @param graph     The Graph object representing the graph.

 * @note            To send message from source to dest, use send_msg(source-1, dest-1, msg, graph)
 */
string send_msg(int source, int dest, string msg, Graph graph) {
    // if not reachable
    if (graph.get_table(source)[source][dest].first == INFINITE) {
        return "from "+to_string(source+1)+ " to "+to_string(dest+1)+" cost infinite hops unreachable message "+msg;
    }
    vector<int> path = graph.find_path(source, dest);
    int cost =  graph.get_table(source)[source][dest].first;
    string output = "from " + to_string(source+1) + " to "+ to_string(dest+1) + " cost "+ to_string(cost) + " hops ";
    for (int i: path) {
        output += to_string(i+1) + ' ';
    }
    output += "message " + msg + "\n";
    return output;
}