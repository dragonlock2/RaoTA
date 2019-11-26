#include "globals.h"
#include "graph.h"
#include "car.h"

unique_ptr<Graph> G;

void processArgs() {
	// Read inputs
	vector<string> argv;
	ifstream file("algs/sortedcppCC/in.txt");
	if (!file) {
		cerr << "No input file found!" << endl;
		exit(1);
	}
	string str;
	while (getline(file, str, ' ')) {
		argv.push_back(str);
	}
	file.close();
	// Get TAs
	vector<node_t> tas(stoi(argv[2]));
	int num_tas = tas.size();
	for (int i = 0; i < num_tas; i++) {
		tas[i] = stoi(argv[3+i]);
	}
	// Construct graph (note: must be connected)
	int num_locs = stoi(argv[3+num_tas]);
	G.reset(new Graph(num_locs));
	for (int i = 0; i < num_locs; i++) { // only access upper triangle
		for (int j = i; j < num_locs; j++) {
			str = argv[4 + num_tas + i*num_locs + j];
			if (str.compare("x") != 0) {
				G->addEdge(i, j, stod(str));
			}
		}
	}
	// Initialize Car, get starting location, needs graph first
	Car::init(stoi(argv[1]), &tas);
}

int main() {
	// auto start = chrono::high_resolution_clock::now();

	processArgs();

	G->allPairsDijkstras();

	// Initialize variables for Dijkstra's
	CarPQ pq;
	unordered_map<carid_t, carid_t> paths;
	unordered_map<carid_t, weight_t> costs;
	Car startcar(Car::startid, 0, 0);

	// Add source point
	paths[startcar.cid] = startcar.cid;
	costs[startcar.cid] = startcar.cost;
	pq.push(startcar);

	// Get naive cost
	weight_t naivecost = 0;
	for (int i = 0; i < LOC_OFFSET; i++) {
		if ((carid_t) 1 << i & Car::startid) {
			naivecost += G->alldists[Car::startloc][i];
		}
	}

	// Run Dijkstra's
	while (!pq.empty()) {
		Car curr = pq.top(); // can't use reference, must copy
		pq.pop();

		if (curr.cid == Car::doneid) { // if I'm done, break
			break;
		}

		if (curr.cost <= costs[curr.cid]) { // To prevent looking at double inserted
			curr.neighbors();
			for (int i = 0; i < Car::num_neighs; i++) {
				Car &ncar = Car::neighs[i];
				weight_t ncost = curr.cost + ncar.cost;

				if (ncost <= naivecost) { // only consider if better than naive
					if (costs.find(ncar.cid) == costs.end()) { // if haven't seen before
						paths[ncar.cid] = curr.cid;
						costs[ncar.cid] = ncost;
						ncar.cost = ncost; // neighbors() returns edge cost, but PQ needs total cost
						pq.push(ncar);
					} else {
						if (ncost < costs[ncar.cid]) {
							paths[ncar.cid] = curr.cid;
							costs[ncar.cid] = ncost;
							ncar.cost = ncost;
							pq.push(ncar);
						}
					}
				}
			}
		}
	}

	// Reconstruct path
	deque<carid_t> cyclecarid;
	carid_t curr = Car::doneid;
	while (curr != Car::startid) {
		curr = paths[curr];
		cyclecarid.push_front(curr);
	}
	deque<carid_t> cyclecaridtoend; // handle the jump to end
	node_t end = Car::startloc;
	node_t src = (node_t) ((carid_t) cyclecarid.back() >> LOC_OFFSET);
	while (end != src) {
		cyclecaridtoend.push_front((carid_t) end << LOC_OFFSET);
		end = G->pcessors[src][end];
	}
	cyclecarid.insert(cyclecarid.end(), cyclecaridtoend.begin(), cyclecaridtoend.end());
	if (cyclecarid.size() == 1) { // handle case of dropping everyone off immediately
		cyclecarid.push_back(Car::doneid);
	}

	// Convert to correct format
	vector<node_t> listlocs;
	unordered_map<node_t, vector<node_t>> listdropoffs;
	for (auto i = cyclecarid.begin(); i != (cyclecarid.end() - 1); i++) {
		node_t loc = (node_t) (*i >> LOC_OFFSET);
		listlocs.push_back(loc);
		vector<node_t> drops;
		for (int j = 0; j < LOC_OFFSET; j++) {
			if ((*i & ((carid_t) 1 << j)) ^ (*(i+1) & ((carid_t) 1 << j))) { // set difference
				drops.push_back(j);
			}
		}
		if (drops.size() > 0) {
			listdropoffs[loc] = drops;
		}
	}
	if (listlocs.size() != 1) { // handle case of dropping everyone off immediately
		listlocs.push_back(Car::startloc);
	}

	// Print out
	for (auto& i: listlocs) {
		cout << int(i) << " ";
	}
	cout << endl;
	for (auto& i: listdropoffs) {
		cout << int(i.first) << " ";
		for (auto& d: i.second) {
			cout << int(d) << " ";
		}
		cout << endl;
	}

	// auto end = chrono::high_resolution_clock::now();
	// auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	// cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}