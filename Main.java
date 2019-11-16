import java.util.*;
import com.google.common.collect.Sets;

public class Main {
	public static int start_loc = 0;

	public static class Pair {
		public Car car;
		public int cost;

		public Pair(Car c, int co) {
			car = c;
			cost = co;
		}
	}

	public static class Car {
		public Integer loc;
		public Set<Integer> tas, reached;

		public Car(int loc, Set<Integer> tas, Set<Integer> reached) {
			this.loc = loc;
			this.tas = new HashSet<>(tas);
			this.reached = new HashSet<>(reached);
		}

		public List<Car> neighbors() {
			return null;
		}

		@Override
		public boolean equals(Object o) {
			return loc.equals(((Car) o).loc) && tas.equals(((Car) o).tas);
		}

		@Override
		public int hashCode() {
			return loc.hashCode() + tas.hashCode();
		}

		@Override
		public String toString() {
			return String.format("Car(%s, %s, %s)", loc, tas, reached);
		}
	}

	public static void main(String[] args) {
		long time_start = System.currentTimeMillis();

		final Car donecar = new Car(start_loc, new HashSet<Integer>(), new HashSet<Integer>());

		Set<Integer> a = new HashSet<>();
		a.add(1); a.add(2); a.add(3);

		Set<Set<Integer>> p = Sets.powerSet(a);

		for (Set<Integer> s: p) {
			System.out.println(s);
		}

		long time_end = System.currentTimeMillis();
		System.out.println("done! Time: " + ((time_end - time_start) / 1000.0) + "s");
	}
}