import threading
import random
import time
class Lock:
    def __init__(self):
        self.lock = threading.Lock()
    def acquire(self):
        self.lock.acquire()
    def release(self):
        self.lock.release()
class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = Lock()
    def deposit(self):
        self.lock.acquire()
        try:
            amount = random.randint(50, 500)
            self.balance += amount
            print(f" Пополнение: {amount}. Баланс: {self.balance} ")
            if self.balance >= 500 and self.lock.acquire():
                self.lock.release()
            time.sleep(0.001)
        finally:
            self.lock.release()
    def take(self):
        amount = random.randint(50, 500)
        print(f" Запрос на {amount} ")
        if amount <= self.balance:
            self.lock.acquire()
            try:
                self.balance -= amount
                print(f" Снятие: {amount}. Баланс: {self.balance} ")
            finally:
                self.lock.release()
        else:
            print(" Запрос отклонён, недостаточно средств ")
            self.lock.acquire()
bk = Bank()
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))
th1.start()
th2.start()
th1.join()
th2.join()
print(f'Итоговый баланс: {bk.balance}')
