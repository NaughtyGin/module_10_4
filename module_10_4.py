import threading
from threading import Thread
from queue import Queue
from time import sleep
from random import randint


class Table:

    def __init__(self, number: int, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        sleep(randint(3, 10))

    def __str__(self):
        return self.name


class Cafe:

    def __init__(self, *tables):
        self.tables = tables
        self.queue = Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            for table in tables:
                if table.guest is None:
                    table.guest = guest
                    th = threading.Thread(target=Guest.run, args=(guests, ), name=table.guest)
                    th.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or True in [table.guest is not None for table in tables]:
            threads_now = [th for th in threading.enumerate() if th.name in guests_names]
            sleep(0.3)  # задержка для синхронизации потоков первых гостей и гостей из очереди
            for th in threads_now:
                if not threading.Thread.is_alive(th):
                    free_table = [table.number for table in tables if str(table.guest) == str(th.name)]
                    for table in tables:
                        if table.number == free_table[0]:
                            print(f'{table.guest} покушал(-а) и ушёл(ушла)')
                            print(f'Стол номер {table.number} свободен')
                            table.guest = None
                            if not self.queue.empty():
                                table.guest = self.queue.get()
                                th = threading.Thread(target=Guest.run, args=(self.queue, ), daemon=True,
                                                      name=table.guest)
                                th.start()
                                print(f'{table.guest} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
        print('Все гости покушали и ушли, очереди нет')


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Victoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
