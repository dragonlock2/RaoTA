#include "globals.h"
#include "graph.h"
#include "car.h"

// Static level definitions
node_t Car::startloc;
carid_t Car::startid;
carid_t Car::doneid;
uint32_t Car::num_neighs = 0;
vector<Car> Car::neighs;

void Car::init(node_t sloc, vector<node_t> *tas) {
	startloc = sloc;
	doneid = (carid_t) startloc << LOC_OFFSET;
	startid = doneid;
	for (auto i = tas->begin(); i != tas->end(); i++) {
		startid |= (carid_t) 1 << *i;
	}
	int maxd = 0;
	for (auto i = G->adjlist.begin(); i != G->adjlist.end(); i++) {
		if (i->size() > maxd) {
			maxd = i->size();
		}
	}
	neighs.resize(maxd * (1 << tas->size()), Car(0, 0, 0)); // At size 50, this can take up to 37.5GB, same for PQ
}

// Object level definitions
Car::Car(carid_t cid, reach_t rec, weight_t way) : cid(cid), rec(rec), cost(way) {}

bool Car::operator<(const Car& other) const {
	return cost > other.cost;
}

void Car::neighbors() const { //parallelizable?
	node_t curloc = (node_t) (cid >> LOC_OFFSET);
	vector<node_t> &ns = G->adjlist[curloc]; //list of neighbors
	num_neighs = ns.size();

	if ((reach_t) 1 << curloc & rec) { //if been here before, can't dropoff here
		carid_t blankid = (~((carid_t) 0) >> LOC_BITS) & cid; //make room for new location
		int i = 0;
		for (auto n = ns.begin(); n != ns.end(); n++) { //travel to each neighbor
			neighs[i].cid = blankid | ((carid_t) *n << LOC_OFFSET);
			neighs[i].rec = rec;
			neighs[i].cost = G->weights[curloc][*n] * 2/3;
			i++;
		}
	} else {
		weight_t maxcost = 0;
		carid_t tas = cid;
		for (int i = 0; i < LOC_OFFSET; i++) { //first compute cost of dropping everyone off
			if (tas & 1) {
				maxcost += G->alldists[curloc][i];
			}
			tas >>= 1;
		}
		reach_t newrec = rec | (reach_t) 1 << curloc;
		for (int i = 0; i < num_neighs; i++) { //add in naive case, also base for powerset
			neighs[i].cid = (carid_t) ns[i] << LOC_OFFSET;
			neighs[i].rec = newrec;
			neighs[i].cost = maxcost + G->weights[curloc][ns[i]] * 2/3;
		}
		tas = cid;
		for (int i = 0; i < LOC_OFFSET; i++) {
			if (tas & 1 && curloc != i) { //for each TA, consider leaving them in car, but if at TA's home, don't
				for (int j = 0; j < num_neighs; j++) {
					neighs[j + num_neighs].cid = neighs[j].cid; //copy over the current neighs
					neighs[j + num_neighs].rec = newrec;
					neighs[j + num_neighs].cost = neighs[j].cost;

					neighs[j].cid |= (carid_t) 1 << i; //leave them in car
					neighs[j].cost -= G->alldists[curloc][i]; //cost decreases by keeping them
				}
				num_neighs <<= 1;
			}
			tas >>= 1;
		}
		num_neighs = num_neighs - ns.size() + 1; //naive case drop everyone off, head home, get rid of extras
		neighs[num_neighs - 1].cid = doneid;
		neighs[num_neighs - 1].cost = maxcost + G->alldists[curloc][startloc] * 2/3;
	}
}

//Debug
Car::Car(node_t loc, vector<node_t> *tas, vector<node_t> *reached, weight_t weight) {
	cid = (carid_t) loc << LOC_OFFSET;
	for (auto i = tas->begin(); i != tas->end(); i++) {
		if (*i < LOC_OFFSET) { //make sure it's a valid node
			cid |= (carid_t) 1 << *i; //need to cast bc default is 32 bit i think
		}
	}
	rec = 0;
	for (auto i = reached->begin(); i != reached->end(); i++) {
		if (*i < LOC_OFFSET) {
			rec |= (carid_t) 1 << *i;
		}
	}
	cost = weight;
}

ostream& operator<<(ostream& strm, const Car& c) {
	strm << "Car(" << (c.cid >> LOC_OFFSET) << ", {";
	if (c.cid << LOC_BITS) { //check if has any TAs
		for (int i = 0; i < LOC_OFFSET; i++) {
			if (c.cid >> i & 1) {
				strm << i << ", ";
			}
		}
		strm << "\b\b";
	}
	strm << "}, {";
	if (c.rec) { //check if has been anywhere
		for (int i = 0; i < LOC_OFFSET; i++) {
			if (c.rec >> i & 1) {
				strm << i << ", ";
			}
		}
		strm << "\b\b";
	}
	return strm << "}, " << c.cost << ")";
}