import budget
outgoings = budget.BudgetManager(2500)
outgoings.add_budget("Alimenti", 500)
outgoings.print_summary()