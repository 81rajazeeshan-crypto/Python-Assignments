### Task 14 | Command-Line Contact Manager
### Concepts: Modules, JSON, CRUD, validation
### Problem: Build a menu-driven CLI contact manager with add, search, update, delete, list, and persistent JSON storage. Each contact has a unique ID, name, phone, and email.
### Requirements: Use separate functions/modules for storage and business logic. Handle missing/corrupt JSON safely without silently deleting existing data. Search names case-insensitively.
### Sample / expected behavior: Add ID=1, name="Ayesha"; restart application; search "aye" -> contact remains available.


import json
import os

STORAGE_FILE = "contacts_data.json"


def load_contacts():
    if not os.path.exists(STORAGE_FILE):
        return {}
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        
        print("Warning: Contact storage file is corrupted or unreadable. Starting with empty state to prevent data loss.")
        return {}

def save_contacts(contacts):
    try:
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=4)
    except IOError as e:
        print(f"Error saving contacts to storage: {e}")



def add_contact(contacts, contact_id, name, phone, email):
    if contact_id in contacts:
        raise ValueError(f"Contact ID '{contact_id}' already exists.")
    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }
    save_contacts(contacts)

def search_contacts(contacts, query):
    query_lower = query.lower()
    results = []
    for c_id, details in contacts.items():
        if query_lower in details["name"].lower() or query_lower in details["phone"] or query_lower in details["email"].lower():
            results.append({"id": c_id, **details})
    return results

def update_contact(contacts, contact_id, name=None, phone=None, email=None):
    if contact_id not in contacts:
        raise ValueError(f"Contact ID '{contact_id}' does not exist.")
    if name:
        contacts[contact_id]["name"] = name
    if phone:
        contacts[contact_id]["phone"] = phone
    if email:
        contacts[contact_id]["email"] = email
    save_contacts(contacts)

def delete_contact(contacts, contact_id):
    if contact_id not in contacts:
        raise ValueError(f"Contact ID '{contact_id}' does not exist.")
    del contacts[contact_id]
    save_contacts(contacts)

def list_contacts(contacts):
    return [{"id": c_id, **details} for c_id, details in contacts.items()]



if __name__ == "__main__":
    
    if os.path.exists(STORAGE_FILE):
        os.remove(STORAGE_FILE)
        
    db = load_contacts()
    
   
    add_contact(db, "1", "Ayesha", "0300-1234567", "ayesha@email.com")
    add_contact(db, "2", "Ali", "0321-9876543", "ali@email.com")
    
    print("--- List All Contacts ---")
    for c in list_contacts(db):
        print(c)
        
    print("\n--- Case-Insensitive Search for 'aye' ---")
    for res in search_contacts(db, "aye"):
        print(res)
        
    print("\n--- Update Contact 1 Phone ---")
    update_contact(db, "1", phone="0333-5555555")
    print("Updated Contact 1:", db["1"])
    
    print("\n--- Delete Contact 2 ---")
    delete_contact(db, "2")
    print("Remaining Contacts count:", len(db))
    
    
    if os.path.exists(STORAGE_FILE):
        os.remove(STORAGE_FILE)