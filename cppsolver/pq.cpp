#include <iostream>
#include <boost/heap/fibonacci_heap.hpp>
#include "pq.h"

FibPQ::FibPQ() {}

// Also replaces what's currently inside PQ
void FibPQ::pushOrChangeKey(Car c, double v) {
	if (mapcth.find(c) == mapcth.end()) {
		mapcth[c] = pq.push(fibpq_pair(c, v));
	} else {
		pq.update(mapcth[c], fibpq_pair(c, v));
	}
}

Car FibPQ::removeMin() {
	Car c = pq.top().first;
	pq.pop();
	mapcth.erase(c);
	return c;
}

bool FibPQ::empty() {
	return pq.empty();
}