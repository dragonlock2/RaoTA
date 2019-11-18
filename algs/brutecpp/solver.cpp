#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>

#include "car.h"
#include "pq.h"

using namespace std;

// If necessary, can probs use uint8_t for indices

void processArgsBuildGraph(char** argv) {
	// Get starting location
	Car::start_loc = atoi(argv[1]);
	// Get TAs
	int num_tas = atoi(argv[2]);
	for (int i = 0; i < num_tas; i++) {
		Car::start_tas.insert(atoi(argv[3+i]));
	}
	// Construct graph (note: must be connected)
	int num_locs = atoi(argv[3+num_tas]);
	for (int i = 0; i < num_locs; i++) { //only access upper triangle
		for (int j = i; j < num_locs; j++) {
			char *str = argv[4 + num_tas + i*num_locs + j];
			if (str[0] != 'x') {
				boost::add_edge(i, j, atof(str), Car::G);
			}
		}
	}
	Car::wm = boost::get(boost::edge_weight, Car::G);
}

void allPairsDijkstras() {
	int num_nodes = boost::num_vertices(Car::G);
	for (int i = 0; i < num_nodes; i++) {
		Car::all_dists.push_back(vector<double>(num_nodes));
		Car::all_pcessors.push_back(vector<int>(num_nodes));
	}
	for (int s = 0; s < num_nodes; s++) {
        boost::dijkstra_shortest_paths(Car::G, s, boost::predecessor_map(&Car::all_pcessors[s][0]).distance_map(&Car::all_dists[s][0]));
    }
}

int main(int argc, char** argv) {
	// auto start = chrono::high_resolution_clock::now();

	processArgsBuildGraph(argv);

	allPairsDijkstras();

	// Initialize variables for Dijkstra's
	FibPQ pq;
	unordered_map<Car, Car> paths;
	unordered_map<Car, double> costs;
	Car startcar(Car::start_loc, Car::start_tas, set<int>());

	// Add source point
	pq.pushOrChangeKey(startcar, 0.0);
	paths.insert(pair<Car, Car>(startcar, startcar));
	costs[startcar] = 0.0;

	// Perform Dijkstra;s
	while (!pq.empty()) {
		// Pop off minimum
		Car currcar = pq.removeMin();
		double currcost = costs[currcar];

		// If at target, then we done
		if (currcar.loc == Car::start_loc && currcar.tas.size() == 0) {
			break;
		}

		// Relax all edges
		for (auto& n: currcar.neighbors()) {
			Car ncar = n.first;
			double ncost = n.second + currcost;
			if (costs.find(ncar) == costs.end()) { //if doesn't exist
				paths.insert(pair<Car, Car>(ncar, currcar));
				costs[ncar] = ncost;
				pq.pushOrChangeKey(ncar, ncost);
			} else {
				if (ncost < costs[ncar]) {
					paths.find(ncar)->second = currcar;
					costs[ncar] = ncost;
					pq.pushOrChangeKey(ncar, ncost);
				}
			}
		}
	}

	// Reconstruct paths
	vector<Car> cycleCar;
	Car endcar(Car::start_loc, set<int>(), set<int>());
	Car *currcarptr = &endcar;
	while (!(*currcarptr == startcar)) {
		currcarptr = &paths.find(*currcarptr)->second; 
		cycleCar.push_back(*currcarptr);
	}
	reverse(cycleCar.begin(), cycleCar.end());
	vector<int> pathToEnd;
	int src = cycleCar.back().loc;
	int curr = Car::start_loc;
	while (curr != src) {
		pathToEnd.push_back(curr);
		curr = Car::all_pcessors[src][curr];
	}
	reverse(pathToEnd.begin(), pathToEnd.end());
	for (auto& i: pathToEnd) {
		cycleCar.push_back(Car(i, set<int>(), set<int>()));
	}

	// Convert to correct format
	vector<int> listlocs;
	unordered_map<int, set<int>> listdropoffs;
	for (auto cp = cycleCar.begin(); cp != cycleCar.end(); cp++) {
		listlocs.push_back(cp->loc);
		if (cp != cycleCar.end() - 1) {
			set<int> drops;
			set_difference(cp->tas.begin(), cp->tas.end(), (cp+1)->tas.begin(), (cp+1)->tas.end(), inserter(drops, drops.end()));
			if (drops.size() > 0) {
				listdropoffs[cp->loc] = drops;
			}
		}
	}
	if (listlocs.size() == 1) { // case of drop everyone off at the beginning
		listdropoffs[cycleCar[0].loc] = cycleCar[0].tas;
	}

	// Print out
	for (auto& i: listlocs) {
		cout << i << " ";
	}
	cout << endl;
	for (auto& i: listdropoffs) {
		cout << i.first << " ";
		for (auto& d: i.second) {
			cout << d << " ";
		}
		cout << endl;
	}


	// auto end = chrono::high_resolution_clock::now();
	// auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

	// cout << " Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}