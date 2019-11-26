#ifndef GRAPH_H
#define GRAPH_H

#include "globals.h"

class Graph {
	public:
		// Graph representation
		vector<vector<node_t>> adjlist;
		vector<vector<weight_t>> weights;
		// For use with Dijkstra's
		vector<vector<weight_t>> alldists;
		vector<vector<node_t>> pcessors;

		Graph(int n);

		void addEdge(node_t u, node_t v, weight_t w);
		void allPairsDijkstras();

		//Debug
		friend ostream& operator<<(ostream &strm, const Graph &g);
	private:
		void singleSourceDijkstras(node_t s);
};

struct dijkpair {
	node_t loc;
	weight_t dist;
};

struct dijkcompair {
	bool operator()(const dijkpair& l, const dijkpair& r) {
		return l.dist > r.dist;
	}
};

#endif