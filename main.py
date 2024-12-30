import threading
import random
import time

class Bank:
    def __init__(self):
        self.balance = 0  # Начальный баланс
        self.lock = threading.Lock()  # Объект блокировки

    def deposit(self):
        for _ in range(100):
            amount = random.randint(50, 500)  # Генерация случайного пополнения
            with self.lock:  # Блокируем доступ к балансу
                self.balance += amount  # Увеличиваем баланс
                print(f"Пополнение: {amount}. Баланс: {self.balance}")

                # Если баланс >= 500, разблокируем
                if self.balance >= 500 and not self.lock.locked():
                    self.lock.release()  # Хотя в данном контексте это не требуется

            time.sleep(0.001)  # Имитация времени выполнения пополнения

    def take(self):
        for _ in range(100):
            amount = random.randint(50, 500)  # Генерация случайного снятия
            print(f"Запрос на {amount}")

            with self.lock:  # Блокируем доступ к балансу
                if amount <= self.balance:
                    self.balance -= amount  # Уменьшаем баланс
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    self.lock.acquire()  # Блокируем поток на 0.01 секунд
                    time.sleep(0.01)

# Создание объекта банка
bk = Bank()

# Создание потоков для методов deposit и take
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запуск потоков
th1.start()
th2.start()

# Ожидание завершения обоих потоков
th1.join()
th2.join()

# Итоговый баланс
print(f'Итоговый баланс: {bk.balance}')
