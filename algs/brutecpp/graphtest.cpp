#include <iostream>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, boost::no_property, boost::property<boost::edge_weight_t, double> > Graph;
typedef boost::property_map<Graph, boost::edge_weight_t>::type WeightMap;

int main() {
    Graph G;

    std::cout << "Adding stuff to graph..." << std::endl;

    for (int i = 0; i < 10; i++) {
        boost::add_edge(i, i+1, 6.9, G);
    }

    WeightMap wm = boost::get(boost::edge_weight, G);

    auto b = boost::edge(1, 0, G);
    if (!b.second) {
        boost::add_edge(1, 0, 0.1, G);
    } else {
        std::cout << "Edge exists!" << b.first << wm[b.first] << std::endl;
    }

    boost::add_edge(10, 0, 1.2, G); //Cool! weightmaps work even when edges are added and weights change, has direct access to graph (makes sense...)

    std::cout << "Printing out graph..." << std::endl;

    for (auto vi = boost::vertices(G); vi.first != vi.second; vi.first++) { // for each vertex
        int v = *vi.first;
        std::cout << v << " : ";
        for (auto ei = boost::out_edges(v, G); ei.first != ei.second; ei.first++) { //for each outgoing edge (use boost::adjacent_vertices for just neighbors)
            auto e = *ei.first; // get the edge
            double w = wm[e]; //boost::get(boost::edge_weight_t(), G, e);
            int s = boost::source(e, G);
            int t = boost::target(e, G);
            std::printf("(%d, %d, %.3f) ", s, t, w); // print out edges + weight
        }
        std::cout << std::endl;
    }

    std::cout << "Getting shortest paths from 0..." << std::endl;

    std::vector<double> ddists(boost::num_vertices(G)); //vector always initialized to 0 if not specified
    std::vector<int> dpaths(boost::num_vertices(G));

    int source = 1;
    boost::dijkstra_shortest_paths(G, source, boost::predecessor_map(&dpaths[0]).distance_map(&ddists[0])); // doesn't need weight map

    for (int i = 0; i < ddists.size(); i++) {
        std::cout << source << "->" << i << " = " << ddists[i] << " ";

        std::vector<int> path;
        int curr = i;
        while (curr != source) {
            path.push_back(curr);
            curr = dpaths[curr];
        }
        path.push_back(source);
        for (auto i = path.rbegin(); i != path.rend(); i++) {
            std::cout << *i << ">";
        }

        std::cout << std::endl;
    }

    std::cout << "Getting all paths..." << std::endl;

    // Ok for some reason BGL's all pairs doesn't return predecessors, so we're just gonna do Dijkstra's |V| times
    // Basically very similar to Johnson's algorithm

    std::vector<std::vector<double>> dists;
    std::vector<std::vector<int>> paths;

    int num_vertices = boost::num_vertices(G);
    for (int i = 0; i < num_vertices; i++) {
        dists.push_back(std::vector<double>(num_vertices));
        paths.push_back(std::vector<int>(num_vertices));
    }

    for (int s = 0; s < num_vertices; s++) {
        boost::dijkstra_shortest_paths(G, s, boost::predecessor_map(&paths[s][0]).distance_map(&dists[s][0]));
    }

    // printing out all distances
    for (int s = 0; s < num_vertices; s++) {
        std::cout << s << " = ";
        for (int t = 0; t < num_vertices; t++) {
            std::cout << t << ":" << dists[s][t] << " ";
        }
        std::cout << std::endl;
    }
}