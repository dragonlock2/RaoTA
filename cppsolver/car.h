#ifndef CAR_H
#define CAR_H

#include <vector>
#include <set>

using namespace std;

class Car {
	public:
		int loc;
		set<int> tas;
		set<int> reached;

		Car(int l, set<int> t, set<int> r);
};

#endif