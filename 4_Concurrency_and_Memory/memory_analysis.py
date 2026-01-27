import sys
import gc
import weakref
import time

"""
Memory Analysis Script

Tasks:
 1) Use sys.getrefcount() to inspect objects.
 2) Create a cyclic reference (two instances pointing to each other).
 3) Show that `del` does not free memory in the presence of a cycle (refcount stays > 0).
 4) Force a collection with gc.collect() and report reclaimed objects.
 5) Fix the cycle using weakref to allow deallocation.

Note: sys.getrefcount(x) returns a value that is typically one higher than
the actual count because the argument passed to getrefcount() creates a
temporary reference. We'll display the raw value and the adjusted value
(`raw-1`) for clarity.
"""


def refcounts(label: str, obj) -> None:
	raw = sys.getrefcount(obj)
	print(f"{label}: getrefcount={raw} (approx actual={raw-1})")


class A:
	pass


class B:
	pass


def demonstrate_cycle_and_gc() -> None:
	print("=== Cycle with strong references ===")
	# Disable automatic cyclic GC temporarily to make the effect observable.
	auto_gc_enabled = gc.isenabled()
	if auto_gc_enabled:
		gc.disable()

	a = A()
	b = B()

	refcounts("a (fresh)", a)
	refcounts("b (fresh)", b)

	# Create cycle: each points to the other
	a.partner = b
	b.partner = a
	print("Created strong reference cycle: a<->b")
	refcounts("a (after linking)", a)
	refcounts("b (after linking)", b)

	# Delete only one external reference; the other still holds a reference
	del a
	print("Deleted name 'a', but 'b.partner' still references the A instance")
	# We can still observe the A object via b.partner
	refcounts("b", b)
	refcounts("b.partner (A)", b.partner)

	# Now delete the remaining external reference
	del b
	print("Deleted name 'b' as well. The cycle objects are now unreachable but still referenced by each other.")

	# Force collection and measure reclaimed unreachable objects
	unreachable = gc.collect()
	print(f"gc.collect() reclaimed objects: {unreachable}")

	# Restore GC state
	if auto_gc_enabled:
		gc.enable()


class WeakA:
	def set_partner(self, other: "WeakB") -> None:
		# Store a weak reference to other
		self.partner = weakref.ref(other)

	def get_partner(self):
		return getattr(self, "partner", lambda: None)()


class WeakB:
	def set_partner(self, other: "WeakA") -> None:
		self.partner = weakref.ref(other)

	def get_partner(self):
		return getattr(self, "partner", lambda: None)()


def demonstrate_weakref_fix() -> None:
	print("\n=== Cycle using weak references (no leak) ===")
	wa = WeakA()
	wb = WeakB()

	refcounts("wa (fresh)", wa)
	refcounts("wb (fresh)", wb)

	# Create a cycle using weak references
	wa.set_partner(wb)
	wb.set_partner(wa)
	print("Created weak reference cycle: wa<->wb (via weakref)")
	refcounts("wa (after linking)", wa)
	refcounts("wb (after linking)", wb)

	# Delete both strong names; weak references do not increase refcount
	del wa
	del wb
	unreachable = gc.collect()
	print(f"gc.collect() after weak cycle: reclaimed objects={unreachable}")


def main() -> int:
	start = time.time()
	demonstrate_cycle_and_gc()
	demonstrate_weakref_fix()
	elapsed = time.time() - start
	print(f"\nDone in {elapsed:.2f}s")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
