### Task 03 | Recursive JSON Path Explorer
### Concepts: Recursion, nested lists/dictionaries
### Problem: Implement find_paths(data, target) that recursively searches nested dictionaries and lists and returns all paths whose value equals target.
### Requirements: Use dot notation for dictionary keys and [index] for list positions. Preserve traversal order; do not treat bool True as numeric 1.
### Sample / expected behavior: Input: {"a":[{"x":5},5],"b":{"y":5}}, target=5 -> ["a[0].x", "a[1]", "b.y"].


def find_paths(data, target):
    paths = []
    
    def recurse(current, current_path):
       
        if type(current) == type(target) and current == target:
            paths.append(current_path)
            
        if isinstance(current, dict):
            for key, value in current.items():
                if current_path == "":
                    new_path = str(key)
                else:
                    new_path = f"{current_path}.{key}"
                recurse(value, new_path)
                
        elif isinstance(current, list):
            for index, item in enumerate(current):
                new_path = f"{current_path}[{index}]"
                recurse(item, new_path)

    recurse(data, "")
    return paths



if __name__ == "__main__":
    sample_data = {
        "a": [{"x": 5}, 5],
        "b": {"y": 5},
        "c": True
    }
    
    target_val = 5
    result = find_paths(sample_data, target_val)
    print("Paths found:", result)
    