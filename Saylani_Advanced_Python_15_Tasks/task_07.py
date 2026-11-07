### Task 07 | Employee Payroll Engine
### Concepts: Inheritance, polymorphism, abstract classes
### Problem: Define abstract Employee with calculate_pay(). Implement SalariedEmployee, HourlyEmployee, and CommissionEmployee with different pay formulas. Generate a unified payroll summary.
### Requirements: Hourly overtime above 40 hours pays 1.5x. Commission employees receive base + sales*rate. Prevent direct instantiation of Employee.
### Sample / expected behavior: Hourly rate=20, hours=45 -> 950; Commission base=500, sales=4000, rate=.10 -> 900.


from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, emp_id: str, name: str):
        self._emp_id = emp_id
        self._name = name

    @property
    def emp_id(self):
        return self._emp_id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def calculate_pay(self) -> float:
        pass


class SalariedEmployee(Employee):
    def __init__(self, emp_id: str, name: str, monthly_salary: float):
        super().__init__(emp_id, name)
        if monthly_salary < 0:
            raise ValueError("Salary cannot be negative.")
        self._monthly_salary = float(monthly_salary)

    def calculate_pay(self) -> float:
        return self._monthly_salary


class HourlyEmployee(Employee):
    def __init__(self, emp_id: str, name: str, hourly_rate: float, hours_worked: float):
        super().__init__(emp_id, name)
        if hourly_rate < 0 or hours_worked < 0:
            raise ValueError("Rate and hours cannot be negative.")
        self._hourly_rate = float(hourly_rate)
        self._hours_worked = float(hours_worked)

    def calculate_pay(self) -> float:
        if self._hours_worked <= 40:
            return self._hours_worked * self._hourly_rate
        else:
            regular_pay = 40 * self._hourly_rate
            overtime_hours = self._hours_worked - 40
            overtime_pay = overtime_hours * self._hourly_rate * 1.5
            return regular_pay + overtime_pay


class CommissionEmployee(Employee):
    def __init__(self, emp_id: str, name: str, base_salary: float, sales_amount: float, commission_rate: float):
        super().__init__(emp_id, name)
        if base_salary < 0 or sales_amount < 0 or commission_rate < 0:
            raise ValueError("Base salary, sales, and rate cannot be negative.")
        self._base_salary = float(base_salary)
        self._sales_amount = float(sales_amount)
        self._commission_rate = float(commission_rate)

    def calculate_pay(self) -> float:
        return self._base_salary + (self._sales_amount * self._commission_rate)


def generate_payroll_summary(employees):
    summary = "--- Unified Payroll Summary ---\n"
    total_payroll = 0.0
    for emp in employees:
        pay = emp.calculate_pay()
        total_payroll += pay
        summary += f"ID: {emp.emp_id} | Name: {emp.name} | Type: {type(emp).__name__} | Pay: {pay:.2f}\n"
    summary += f"---------------------------------\nTotal Company Payroll: {total_payroll:.2f}"
    return summary



if __name__ == "__main__":
    staff = [
        SalariedEmployee("E001", "Ahmed", 5000.0),
        HourlyEmployee("E002", "Zain", 20.0, 45.0),       
        CommissionEmployee("E003", "Sara", 500.0, 4000.0, 0.10) 
    ]
    
    print(generate_payroll_summary(staff))
    
    
    try:
        invalid_emp = Employee("E999", "Ghost")
    except TypeError as e:
        print("\nAbstract Instantiation Prevention Verified Successfully.")