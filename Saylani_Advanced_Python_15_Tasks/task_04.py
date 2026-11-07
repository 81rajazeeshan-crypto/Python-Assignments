### Task 04 | Dependency Execution Planner
### Concepts: Graphs, sets, algorithms
### Problem: Given tasks and prerequisite pairs (A,B) meaning A must finish before B, return a valid execution order.
### Requirements: Detect cycles and raise ValueError with a clear message. For multiple available tasks, select alphabetically first. Reject unknown task names.
### Sample / expected behavior: Tasks=["build","test","deploy"]; dependencies=[("build","test"),("test","deploy")] -> ["build","test","deploy"].


import heapq

def find_execution_order(tasks, dependencies):
    task_set = set(tasks)
    in_degree = {task: 0 for task in tasks}
    adj_list = {task: [] for task in tasks}
    
    
    for u, v in dependencies:
        if u not in task_set or v not in task_set:
            raise ValueError(f"Unknown task name found in dependencies: ({u}, {v})")
        adj_list[u].append(v)
        in_degree[v] += 1
        
    
    available_tasks = [task for task in tasks if in_degree[task] == 0]
    heapq.heapify(available_tasks)
    
    execution_order = []
    
    while available_tasks:
        current = heapq.heappop(available_tasks)
        execution_order.append(current)
        
        for neighbor in adj_list[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(available_tasks, neighbor)
                
    
    if len(execution_order) != len(tasks):
        raise ValueError("Cycle detected in task dependencies! Cannot determine valid execution order.")
        
    return execution_order



if __name__ == "__main__":
    tasks_list = ["build", "test", "deploy"]
    deps = [("build", "test"), ("test", "deploy")]
    
    try:
        order = find_execution_order(tasks_list, deps)
        print("Execution Order:", order)  
    except ValueError as e:
        print("Error:", e)
        
   
    cyclic_deps = [("build", "test"), ("test", "build")]
    try:
        find_execution_order(["build", "test"], cyclic_deps)
    except ValueError as e:
        print("Cycle Error Handled Successfully:", e)