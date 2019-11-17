#include <iostream>
#include <vector>
#include <set>
#include "car.h"

using namespace std;

Car::Car(int l, set<int> t, set<int> r) : loc(l), tas(t), reached(r) {}