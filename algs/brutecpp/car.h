#ifndef CAR_H
#define CAR_H

#include <vector>
#include <set>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, boost::no_property, boost::property<boost::edge_weight_t, double> > Graph;
typedef boost::property_map<Graph, boost::edge_weight_t>::type WeightMap;

typedef int16_t node_t; // using this to save memory

// Intended for use inside an unordered_map (hash map)

class Car {
	public:
		static Graph G;
		static WeightMap wm;
		static std::vector<std::vector<double>> all_dists;
		static std::vector<std::vector<node_t>> all_pcessors;
		static node_t start_loc;
		static std::set<node_t> start_tas;

		node_t loc;
		std::set<node_t> tas;
		std::set<node_t> reached;

		Car(node_t l, std::set<node_t> t, std::set<node_t> r);

		std::vector<std::pair<Car, double>> neighbors();

		bool operator==(Car other) const;
		friend std::ostream& operator<<(std::ostream &strm, const Car &c);
	private:
		static std::vector<std::set<node_t>> powerset(std::set<node_t> s);
		static int intpow(int b, int n);
};

namespace std { //TODO improve hashcode
	template <>
	struct hash<Car> {
	    size_t operator()(const Car& c) const {
	    	size_t h = 0;
	    	for (auto i: c.tas) {
	    		size_t l = i;
	    		h += l*l*l;
	    	}
	    	h += ((size_t)c.loc * (size_t)c.loc) << 29;
	        return h;
	    }
	};
}

#endif