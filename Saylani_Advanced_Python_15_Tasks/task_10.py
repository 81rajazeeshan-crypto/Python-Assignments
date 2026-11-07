### Task 10 | CSV Inventory Reconciliation
### Concepts: CSV, file handling, validation
### Problem: Read inventory.csv (sku,name,quantity) and movements.csv (sku,type,units). Apply IN and OUT movements in order, then write updated_inventory.csv and rejected_movements.csv.
### Requirements: Reject unknown SKUs, negative or zero units, invalid movement types, and any OUT causing negative stock. Continue processing after rejected rows.
### Sample / expected behavior: SKU P01 starts at 10; OUT 4, OUT 9, IN 2 -> final 8; second movement rejected.


import csv
import os

def reconcile_inventory(inventory_path, movements_path, updated_inv_path, rejected_mov_path):
    
    inventory = {}
    with open(inventory_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row['sku'].strip()
            name = row['name'].strip()
            try:
                qty = int(row['quantity'].strip())
                inventory[sku] = {"name": name, "quantity": qty}
            except ValueError:
                continue

    rejected_movements = []
    
    
    with open(movements_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row['sku'].strip()
            m_type = row['type'].strip().upper()
            
            try:
                units = int(row['units'].strip())
            except ValueError:
               
                rejected_movements.append({**row, "reason": "Invalid units value"})
                continue
                
            
            if sku not in inventory:
                rejected_movements.append({**row, "reason": "Unknown SKU"})
                continue
                
            if units <= 0:
                rejected_movements.append({**row, "reason": "Units must be positive"})
                continue
                
            if m_type not in ("IN", "OUT"):
                rejected_movements.append({**row, "reason": "Invalid movement type"})
                continue
                
            if m_type == "IN":
                inventory[sku]["quantity"] += units
            elif m_type == "OUT":
                if inventory[sku]["quantity"] < units:
                    rejected_movements.append({**row, "reason": "OUT movement causes negative stock"})
                    continue
                inventory[sku]["quantity"] -= units

    
    with open(updated_inv_path, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['sku', 'name', 'quantity']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sku, data in inventory.items():
            writer.writerow({'sku': sku, 'name': data['name'], 'quantity': data['quantity']})

    
    with open(rejected_mov_path, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['sku', 'type', 'units', 'reason']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rej in rejected_movements:
            writer.writerow(rej)



if __name__ == "__main__":
    inv_file = "inventory.csv"
    mov_file = "movements.csv"
    upd_file = "updated_inventory.csv"
    rej_file = "rejected_movements.csv"
    
    
    with open(inv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sku', 'name', 'quantity'])
        writer.writerow(['P01', 'Laptop', '10'])
        writer.writerow(['P02', 'Mouse', '25'])
        
    
    with open(mov_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sku', 'type', 'units'])
        writer.writerow(['P01', 'OUT', '4'])
        writer.writerow(['P01', 'OUT', '9'])  
        writer.writerow(['P01', 'IN', '2'])
        writer.writerow(['P99', 'IN', '5'])   
        
    reconcile_inventory(inv_file, mov_file, upd_file, rej_file)
    
    print("--- Updated Inventory Content ---")
    with open(upd_file, 'r', encoding='utf-8') as f:
        print(f.read())
        
    print("--- Rejected Movements Content ---")
    with open(rej_file, 'r', encoding='utf-8') as f:
        print(f.read())
        
    
    for path in [inv_file, mov_file, upd_file, rej_file]:
        if os.path.exists(path):
            os.remove(path)