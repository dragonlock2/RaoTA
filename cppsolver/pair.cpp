#include <iostream>
#include "pair.h"

Pair::Pair(Car c, double v) : car(c), val(v) {}

bool Pair::operator<(Pair p) const {
	return val > p.val; // too lazy to make actual pq, may need to do comparison more properly
}

std::ostream& operator<<(std::ostream &strm, const Pair& p) {
	return strm << "Pair(" << p.car << ", " << p.val << ")";
}