#ifndef CAR_H
#define CAR_H

#include <vector>

#define LOC_BITS 6
#define LOC_OFFSET 58 //=64-6

typedef uint64_t carid_t; //max 58 locations, index 0-57
typedef uint64_t reach_t;
typedef uint8_t node_t;

class Car {
	public:
		static node_t startloc;
		static carid_t startid;
		static carid_t doneid;

		carid_t cid;
		reach_t rec;

		Car(carid_t cid, reach_t rec);

		bool operator==(Car other) const;

		void neighbors(); //TODO

		//Debug
		Car(node_t loc, std::vector<node_t> *tas, std::vector<node_t> *reached);
		friend std::ostream& operator<<(std::ostream &strm, const Car &c);
};

namespace std {
	template <>
	struct hash<Car> {
	    size_t operator()(const Car& c) const {
	    	//TODO improve this
	    	return c.cid;
	    }
	};
}

#endif