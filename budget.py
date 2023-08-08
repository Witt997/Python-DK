class BudgetManager:
    def __init__(self, amount):
        self.available = amount
        self.budget = {}
        self.expenditure = {}

    def add_budget(self, name, amount):
        if name in self.budget:
            raise ValueError("Budget esistente")
        if amount > self.available:
            raise ValueError("Fondi insufficienti")
        self.budget[name] = amount
        self.expenditure[name] = []
        self.available -= amount
        return self.available
    
    def change_budget(self, name, new_amount):
        if name not in self.budget:
            raise ValueError("Il budget non esiste")
        old_amount = self.budget[name]
        if new_amount > old_amount + self.available:
            raise ValueError("Fondi insufficienti")
        self.budget[name] = new_amount
        self.available -= new_amount - old_amount
        return self.available

    def spend(self, name, amount):
        if name not in self.expenditure:
            raise ValueError("Budget non previsto")
        self.expenditure[name].append(amount)
        budgeted = self.budget[name]
        spent = sum(self.expenditure[name])
        return budgeted - spent

    def print_summary(self):
        print("Budget           Previsto      Speso   Residuo")
        print("--------------- ---------- ---------- ----------")
        total_budgeted = 0
        total_spent = 0
        total_remaining = 0
        for name in self.budget:
            budgeted = self.budget[name]
            spent = sum(self.expenditure[name])
            remaining = budgeted - spent
            print(f'{name:15s} {budgeted:10.2f} {spent:10.2f}' f'{remaining:10.2f}')
            total_budgeted += budgeted
            total_spent += spent
            total_remaining += remaining
        print("--------------- ---------- ---------- ----------")
        print(f'{ "Totale":15s} {total_budgeted:10.2f} {total_spent:10.2f}' 
              f'{total_budgeted - total_spent:10.2f}')
