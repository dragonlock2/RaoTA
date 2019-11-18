#ifndef CAR_H
#define CAR_H

#include <vector>
#include <set>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, boost::no_property, boost::property<boost::edge_weight_t, double> > Graph;
typedef boost::property_map<Graph, boost::edge_weight_t>::type WeightMap;

// Intended for use inside an unordered_map (hash map)

class Car {
	public:
		static Graph G;
		static WeightMap wm;
		static std::vector<std::vector<double>> all_dists;
		static std::vector<std::vector<int>> all_pcessors;
		static int start_loc;
		static std::set<int> start_tas;

		int loc;
		std::set<int> tas;
		std::set<int> reached;

		Car(int l, std::set<int> t, std::set<int> r);

		std::vector<std::pair<Car, double>> neighbors();

		bool operator==(Car other) const;
		friend std::ostream& operator<<(std::ostream &strm, const Car &c);
	private:
		static std::vector<std::set<int>> powerSet(std::set<int> s);
		static int intpow(int b, int n);
};

namespace std {
	template <>
	struct hash<set<int>> {
		size_t operator()(const set<int>& s) const {
			size_t h = 0;
			for (auto i: s) {
				h += hash<int>()(i);
			}
			return h;
		}
	};
	template <>
	struct hash<Car> {
	    size_t operator()(const Car& c) const {
	        return hash<int>()(c.loc) + hash<set<int>>()(c.tas);
	    }
	};
}

#endif