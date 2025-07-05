class ManagedMoneyAmount:
    def __init__(self, initial_amount):
        self.amount = initial_amount
    def deposit_possible(self, amount):
        return True
    def withdraw_possible(self, amount):
        return True
    def deposit(self, amount):
        if (
            amount < 0
            or not self.deposit_possible(amount)
        ):
            return False
        else:
            self.amount += amount
            return True
    def withdraw(self, amount):
        if (
            amount < 0
            or not self.withdraw_possible(amount)
        ):
            return False
        else:
            self.amount -= amount
            return True
    def show(self):
        print(f"Amount: {self.amount}")

class GeneralAccount(ManagedMoneyAmount):
    def __init__(self, customer_data, account_balance):
        super().__init__(account_balance)
        self.customer_data = customer_data
    def money_transfer(self, destination, amount):
        if (self.withdraw_possible(amount) and destination.deposit_possible(amount)):
            self.withdraw(amount)
            destination.deposit(amount)
            return True
        else:
            return False
    def show(self):
        self.customer_data.show()
        super().show()

class GeneralAccountWithDailyTurnover(GeneralAccount):
    def __init__(self, customer_data, account_balance, max_daily_turnover = 1500):
        super().__init__(customer_data, account_balance)
        self.max_daily_turnover = max_daily_turnover
        self.turnover_today = 0.0
    def transfer_possible(self, amount):
        return (self.turnover_today + amount <= self.max_daily_turnover)
    def withdraw_possible(self, amount):
        return self.transfer_possible(amount)
    def deposit_possible(self, amount):
        return self.transfer_possible(amount)
    def deposit(self, amount):
        if super().deposit(amount):
            self.turnover_today += amount
            return True
        else:
            return False
    def withdraw(self, amount):
        if super().withdraw(amount):
            self.turnover_today += amount
            return True
        else:
            return False
    def show(self):
        super().show()
        print(f"Today already {self.turnover_today : .2f} of {self.max_daily_turnover : .2f} USD turned over")

class CheckingAccountCustomerData:
    def __init__(self, owner, account_number):
        self.owner = owner
        self.account_number = account_number
    def show(self):
        print(f"Owner: {self.owner}")
        print(f"Account number: {self.account_number}")

class CheckingAccountWithDailyTurnover(GeneralAccountWithDailyTurnover):
    def __init__(self, owner, account_number, account_balance, max_daily_turnover=1500):
        customer_data =CheckingAccountCustomerData(owner, account_number)
        super().__init__(customer_data, account_balance, max_daily_turnover)

class ManagedCashAmount(ManagedMoneyAmount):
    def __init__(self, cash_amount):
        if cash_amount < 0:
            cash_amount = 0
        else:
            super().__init__(cash_amount)
    def withdraw_possible(self, amount):
        return (self.amount >= amount)

class Wallet(ManagedCashAmount):
    pass

class Safe(ManagedCashAmount):
    pass

if __name__ == "__main__":
