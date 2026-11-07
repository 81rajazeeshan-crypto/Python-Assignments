### Task 12 | Custom Iterable Range Toolkit
### Concepts: Iterators, generators, dunder methods
### Problem: Create a ReversibleRange(start,stop,step) class supporting iteration, reversed iteration, len(), and membership tests without constructing a list.
### Requirements: Match Python range stop-exclusive semantics for positive and negative nonzero steps. Implement __iter__, __reversed__, __len__, and __contains__.
### Sample / expected behavior: ReversibleRange(2,11,3) -> [2,5,8]; reversed -> [8,5,2]; 5 in object -> True.


class ReversibleRange:
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            self._start = 0
            self._stop = start
            self._step = 1
        else:
            self._start = start
            self._stop = stop
            self._step = step
            
        if self._step == 0:
            raise ValueError("range() arg 3 must not be zero")
            
        
        if self._step > 0:
            if self._start >= self._stop:
                self._length = 0
            else:
                self._length = (self._stop - self._start + self._step - 1) // self._step
        else:
            if self._start <= self._stop:
                self._length = 0
            else:
                self._length = (self._start - self._stop - self._step - 1) // (-self._step)

    def __len__(self):
        return self._length

    def __iter__(self):
        current = self._start
        for _ in range(self._length):
            yield current
            current += self._step

    def __reversed__(self):
        if self._length == 0:
            return
        
        last_val = self._start + (self._length - 1) * self._step
        current = last_val
        for _ in range(self._length):
            yield current
            current -= self._step

    def __contains__(self, value):
        if self._length == 0:
            return False
            
        if self._step > 0:
            if not (self._start <= value < self._stop):
                return False
        else:
            if not (self._stop < value <= self._start):
                return False
                
        
        return (value - self._start) % self._step == 0



if __name__ == "__main__":
    r = ReversibleRange(2, 11, 3)
    print("Forward Iteration:", list(r))         
    print("Reversed Iteration:", list(reversed(r))) 
    print("Length of range:", len(r))             
    print("Is 5 in range?", 5 in r)               
    print("Is 6 in range?", 6 in r)              