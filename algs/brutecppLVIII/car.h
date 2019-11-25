#ifndef CAR_H
#define CAR_H

#include "globals.h"
#include "graph.h"

extern unique_ptr<Graph> G;

class Car {
	public:
		static node_t startloc;
		static carid_t startid;
		static carid_t doneid;
		static uint32_t num_neighs; //if above 2^32 neighbors, probs not good
		static vector<Car> neighs; //reduce amount of allocation we do
		static void init(node_t sloc, vector<node_t> *tas);

		carid_t cid;
		reach_t rec;
		weight_t cost; //Cars are identified by carids, so Car object used for PQs simplifies things

		Car(carid_t cid, reach_t rec, weight_t way);

		void neighbors() const;

		bool operator<(const Car& other) const;

		//Debug
		Car(node_t loc, vector<node_t> *tas, vector<node_t> *reached, weight_t weight);
		friend ostream& operator<<(ostream &strm, const Car &c);
};

typedef priority_queue<Car> CarPQ;

#endif