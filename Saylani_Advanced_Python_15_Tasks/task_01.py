### Task 01 | Nested Transaction Analyzer
### Concepts: Data structures, sorting, comprehensions
### Problem: Given a list of transaction dictionaries with keys id, customer, category, amount, and status, produce a report containing each customer’s successful spending, top category, and rank by spending. Ignore failed transactions and reject duplicate transaction IDs.
### Requirements: Return a list sorted by spending descending, then customer name ascending. Customers with no successful transactions must appear with total 0. Do not use pandas.

def analyze_transactions(transactions):
    seen_ids = set()
    customer_data = {}
    
    for tx in transactions:
        tx_id = tx.get("id")
        customer = tx.get("customer")
        category = tx.get("category")
        amount = tx.get("amount", 0)
        status = tx.get("status")
        
       
        if customer not in customer_data:
            customer_data[customer] = {
                "total_spending": 0,
                "categories": {}
            }
            
       
        if tx_id in seen_ids:
            continue
        seen_ids.add(tx_id)
        
        
        if status == "success":
            customer_data[customer]["total_spending"] += amount
            
            cats = customer_data[customer]["categories"]
            cats[category] = cats.get(category, 0) + amount

   
    report = []
    for customer, data in customer_data.items():
        total = data["total_spending"]
        cats = data["categories"]
        
        
        top_cat = None
        if cats:
            top_cat = max(cats.items(), key=lambda x: (x[1], x[0]))[0]
            
        report.append({
            "customer": customer,
            "total_spending": total,
            "top_category": top_cat
        })
        
    
    report.sort(key=lambda x: (-x["total_spending"], x["customer"]))
    
    
    for index, item in enumerate(report, start=1):
        item["rank"] = index
        
    return report


if __name__ == "__main__":
    sample_transactions = [
        {"id": 1, "customer": "Ali", "category": "Food", "amount": 500, "status": "success"},
        {"id": 2, "customer": "Ali", "category": "Travel", "amount": 200, "status": "failed"},
        {"id": 3, "customer": "Sara", "category": "Food", "amount": 700, "status": "success"},
        {"id": 1, "customer": "Duplicate", "category": "Tech", "amount": 100, "status": "success"}, # Duplicate ID test
        {"id": 4, "customer": "Bilal", "category": "Clothes", "amount": 0, "status": "success"} # 0 spending customer
    ]
    
    results = analyze_transactions(sample_transactions)
    for res in results:
        print(res)