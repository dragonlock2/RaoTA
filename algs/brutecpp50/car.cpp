#include <iostream>
#include "car.h"

node_t Car::startloc;
carid_t Car::startid;
carid_t Car::doneid;

Car::Car(carid_t cid, reach_t rec) : cid(cid), rec(rec) {}

bool Car::operator==(Car other) const {
	return cid == other.cid;
}

//Debug
Car::Car(node_t loc, std::vector<node_t> *tas, std::vector<node_t> *reached) {
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
}

std::ostream& operator<<(std::ostream& strm, const Car& c) {
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
	return strm << "})";
}