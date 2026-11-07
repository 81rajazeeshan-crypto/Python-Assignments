### Task 08 | Cache Decorator with Expiration
### Concepts: Decorators, closures, functools, time
### Problem: Implement @ttl_cache(seconds) that caches results for repeated positional and keyword arguments and recomputes after expiration. Track cache hits and misses.
### Requirements: Preserve function metadata with functools.wraps. Handle equivalent keyword argument order; document behavior for unhashable inputs. Use time.monotonic().
### Sample / expected behavior: A call with x=2,y=3 followed by y=3,x=2 before expiry should return a cache hit.


import time
import functools

def ttl_cache(seconds: float = 60):
    def decorator(func):
        cache = {}
        hits = 0
        misses = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            
            
            sorted_kwargs = tuple(sorted(kwargs.items()))
            cache_key = (args, sorted_kwargs)
            
            current_time = time.monotonic()
            
            
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < seconds:
                    hits += 1
                    return result
                else:
                    
                    del cache[cache_key]
            
            
            misses += 1
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            return result

        
        def get_stats():
            return {"hits": hits, "misses": misses}

        def clear_cache():
            nonlocal hits, misses
            cache.clear()
            hits = 0
            misses = 0

        wrapper.get_stats = get_stats
        wrapper.clear_cache = clear_cache
        return wrapper
    return decorator



if __name__ == "__main__":
    @ttl_cache(seconds=2)
    def expensive_computation(x, y):
        print(f"Computing for x={x}, y={y}...")
        return x * y

    print("--- First Call (Miss) ---")
    print(expensive_computation(x=2, y=3))

    print("--- Second Call with same kwarg order (Hit) ---")
    print(expensive_computation(x=2, y=3))

    print("--- Third Call with reversed kwarg order (Hit expected) ---")
    print(expensive_computation(y=3, x=2))

    print("\nCache Stats:", expensive_computation.get_stats())

    print("\nWaiting for TTL expiration...")
    time.sleep(2.1)

    print("--- Call after expiration (Miss expected) ---")
    print(expensive_computation(x=2, y=3))
    print("Final Cache Stats:", expensive_computation.get_stats())