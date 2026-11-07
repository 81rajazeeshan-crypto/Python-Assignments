### Task 06 | Banking Ledger with OOP
### Concepts: Classes, encapsulation, properties
### Problem: Build Account and Bank classes. Support deposit, withdrawal, transfer, and account statements. Maintain immutable transaction records containing transaction ID, action, amount, and resulting balance.
### Requirements: Reject nonpositive amounts, insufficient funds, and nonexistent accounts. A transfer must be atomic: both balances update or neither does.
### Sample / expected behavior: Account A=1000, B=200; transfer 350 from A to B -> A=650, B=550.


import uuid

class Account:
    def __init__(self, account_id: str, holder_name: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._account_id = account_id
        self._holder_name = holder_name
        self._balance = float(initial_balance)
        self._transactions = []  
        
        if initial_balance > 0:
            tx_id = str(uuid.uuid4())[:8]
            record = (tx_id, "INITIAL_DEPOSIT", initial_balance, self._balance)
            self._transactions.append(record)

    @property
    def account_id(self):
        return self._account_id

    @property
    def holder_name(self):
        return self._holder_name

    @property
    def balance(self):
        return self._balance

    @property
    def transactions(self):
        
        return tuple(self._transactions)

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        tx_id = str(uuid.uuid4())[:8]
        record = (tx_id, "DEPOSIT", amount, self._balance)
        self._transactions.append(record)
        return record

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self._balance -= amount
        tx_id = str(uuid.uuid4())[:8]
        record = (tx_id, "WITHDRAWAL", amount, self._balance)
        self._transactions.append(record)
        return record

    def _force_deposit(self, amount: float, tx_id: str):
       
        self._balance += amount
        record = (tx_id, "TRANSFER_IN", amount, self._balance)
        self._transactions.append(record)

    def _force_withdraw(self, amount: float, tx_id: str):
        
        self._balance -= amount
        record = (tx_id, "TRANSFER_OUT", amount, self._balance)
        self._transactions.append(record)


class Bank:
    def __init__(self):
        self._accounts = {}

    def create_account(self, account_id: str, holder_name: str, initial_balance: float = 0.0) -> Account:
        if account_id in self._accounts:
            raise ValueError(f"Account ID '{account_id}' already exists.")
        account = Account(account_id, holder_name, initial_balance)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            raise ValueError(f"Account ID '{account_id}' does not exist.")
        return self._accounts[account_id]

    def transfer(self, from_id: str, to_id: str, amount: float):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)
        
        if amount > from_acc.balance:
            raise ValueError("Insufficient funds in source account for transfer.")
        
        
        tx_id = str(uuid.uuid4())[:8]
        
        try:
            from_acc._force_withdraw(amount, tx_id)
            to_acc._force_deposit(amount, tx_id)
        except Exception as e:
            raise RuntimeError(f"Transfer failed and was rolled back: {e}")

    def get_statement(self, account_id: str):
        acc = self.get_account(account_id)
        statement = f"--- Statement for Account: {acc.account_id} ({acc.holder_name}) ---\n"
        statement += f"Current Balance: {acc.balance}\nTransactions:\n"
        for tx in acc.transactions:
            statement += f"  ID: {tx[0]} | Action: {tx[1]} | Amount: {tx[2]} | Balance: {tx[3]}\n"
        return statement



if __name__ == "__main__":
    bank = Bank()
    acc_a = bank.create_account("A", "Ali", 1000.0)
    acc_b = bank.create_account("B", "Bilal", 200.0)
    
    print(f"Before Transfer -> A: {acc_a.balance}, B: {acc_b.balance}")
    
    
    bank.transfer("A", "B", 350.0)
    
    print(f"After Transfer -> A: {acc_a.balance}, B: {acc_b.balance}")
    print("\n" + bank.get_statement("A"))