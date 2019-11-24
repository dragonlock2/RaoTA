#include "globals.h"
#include "graph.h"

Graph::Graph(int n) {
	adjlist = vector<vector<node_t>>(n);
	weights = vector<vector<weight_t>>(n, vector<weight_t>(n, 0));
	alldists = vector<vector<weight_t>>(n, vector<weight_t>(n, INF));
	pcessors = vector<vector<node_t>>(n, vector<node_t>(n, 0));
}

void Graph::addEdge(node_t u, node_t v, weight_t w) {
	if (weights[u][v] == 0) { //if edge doesn't exist
		weights[u][v] = w;
		weights[v][u] = w;
		adjlist[u].push_back(v);
		adjlist[v].push_back(u);
	}
}

void Graph::allPairsDijkstras() {
	for (node_t s = 0; s < adjlist.size(); s++) {
		singleSourceDijkstras(s);
	}
}

void Graph::singleSourceDijkstras(node_t s) {
	vector<weight_t>& dists = alldists[s];
	vector<node_t>& paths = pcessors[s];
	priority_queue<dijkpair, vector<dijkpair>, dijkcompair> pq;

	dists[s] = 0;
	paths[s] = s;
	pq.push(dijkpair{s, 0});

	while (!pq.empty()) {
		node_t currnode = pq.top().loc;
		weight_t currdist = pq.top().dist;
		pq.pop();

		for (auto n = adjlist[currnode].begin(); n != adjlist[currnode].end(); n++) {
			if (currdist + weights[currnode][*n] < dists[*n]) {
				dists[*n] = currdist + weights[currnode][*n];
				paths[*n] = currnode;
				pq.push(dijkpair{*n, dists[*n]});
			}
		}
	}
}

//Debug
ostream& operator<<(ostream &strm, const Graph &g) {
	strm << "Graph - source -> (target, weight)..." << endl;
	for (int i = 0; i < g.adjlist.size(); i++) {
		strm << i << " -> ";
		for (auto j = g.adjlist[i].begin(); j != g.adjlist[i].end(); j++) {
			strm << "(" << (int) *j << ", " << g.weights[i][*j] << ") ";
		}
		strm << endl;
	}
	strm << "Distances - source -> (target, predecessor, distance)..." << endl;
	for (int s = 0; s < g.adjlist.size(); s++) {
		strm << s << " -> ";
		for (int t = 0; t < g.adjlist.size(); t++) {
			if (g.alldists[s][t] < INF) {
				strm << "(" << t << ", " << (int) g.pcessors[s][t] << ", " << g.alldists[s][t] << ") ";
			} else {
				strm << "(" << t << ", " << "\u221E) ";
			}
		}
		strm << endl;
	}
	return strm;
}