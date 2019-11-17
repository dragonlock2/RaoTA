#ifndef PAIR_H
#define PAIR_H

#include "car.h"

// Intended for use with priority queues and neighbors, stores a Car and double

class Pair {
	public:
		Car car;
		double val;

		Pair(Car c, double v);

		bool operator<(Pair p) const;
		friend std::ostream& operator<<(std::ostream &strm, const Pair &p);
};

#endif