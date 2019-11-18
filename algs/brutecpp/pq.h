#ifndef PQ_H
#define PQ_H

#include <boost/heap/fibonacci_heap.hpp>
#include <unordered_map>

#include "car.h"

// Wrapper class for Fibonnaci Heap, can probably make this a template one day

typedef std::pair<Car, double> fibpq_pair;

struct compare_fibpq_pair {
	bool operator()(const fibpq_pair& p1, const fibpq_pair& p2) const {
		return p1.second > p2.second; // turns into a minpq
	}
};

class FibPQ {
	private:
		std::unordered_map<Car, boost::heap::fibonacci_heap<fibpq_pair, boost::heap::compare<compare_fibpq_pair>>::handle_type> mapcth;
		boost::heap::fibonacci_heap<fibpq_pair, boost::heap::compare<compare_fibpq_pair>> pq;
	public:
		FibPQ();

		void pushOrChangeKey(Car c, double v);
		Car removeMin();
		bool empty();
};

#endif