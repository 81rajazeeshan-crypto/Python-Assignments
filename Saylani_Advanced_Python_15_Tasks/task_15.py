### Task 15 | Integrated Order Fulfillment System
### Concepts: OOP, composition, files, exceptions, algorithms
### Problem: Design Product, Cart, Order, and Inventory classes. Read a product catalog from JSON, build carts, apply percentage discounts, compute totals, and place orders with stock updates. Persist orders to JSON.
### Requirements: Reject invalid quantities and out-of-stock purchases. Validate all items before changing inventory; roll back if order persistence fails. Generate unique order IDs. Include at least three unit tests using unittest.
### Sample / expected behavior: Catalog: P1 price=100 stock=5; cart P1 x2 with 10% discount -> total 180, stock becomes 3 after successful order.


class NestedTransactionManager:
    def __init__(self):
        
        self._store = {}
        
        self._tx_stack = []

    def begin(self):
       
        self._tx_stack.append(dict(self._store))

    def commit(self):
        if not self._tx_stack:
            raise RuntimeError("Cannot commit: No active transaction.")
        
        self._tx_stack.pop()

    def rollback(self):
        if not self._tx_stack:
            raise RuntimeError("Cannot rollback: No active transaction.")
        
        previous_state = self._tx_stack.pop()
        self._store = previous_state

    def set(self, key, value):
        self._store[key] = value

    def get(self, key, default=None):
        return self._store.get(key, default)

    def delete(self, key):
        if key in self._store:
            del self._store[key]



if __name__ == "__main__":
    tm = NestedTransactionManager()
    
    tm.set("a", 10)
    tm.set("b", 20)
    print("Initial State:", tm.get("a"), tm.get("b"))  

   
    tm.begin()
    tm.set("a", 100)
    print("Inside Outer Tx (a):", tm.get("a"))  
    
    
    tm.begin()
    tm.set("a", 999)
    tm.set("c", 30)
    print("Inside Inner Tx (a, c):", tm.get("a"), tm.get("c")) 
    
    
    tm.rollback()
    print("After Inner Rollback (a should be 100, c should be None):", tm.get("a"), tm.get("c"))  # Expected: 100, None
    
    
    tm.commit()
    print("After Outer Commit (a):", tm.get("a"))  