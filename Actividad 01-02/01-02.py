import threading
import queue
import random
import time

PRODUCERS = 10
CONSUMERS = 5
ITEMS = 10

aux = list()

queue = queue.Queue(maxsize=10)
condition = threading.Condition()
restantes = threading.Semaphore(ITEMS)

class Producer(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        while True:
            if condition.acquire():
                if queue.full():
                    condition.wait()
                else:
                    item = random.randint(0, 100)
                    restantes.acquire() 
                    queue.put(item)
                    print(f"el productor {self.id} produjo {item}")
                    aux.append(item)
                    condition.notify()
                    condition.release()
                    time.sleep(3)

class Consumer(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        while True:
            if condition.acquire():
                if queue.empty():
                    condition.wait()
                else:
                    item = queue.get()
                    item = aux.pop()
                    print(f"el consumidor {self.id} consumio el item {item}")
                    print("Items en bodega: ", aux) if len(aux)>0 else print("Bodega vacía")
                    restantes.release()
                    condition.notify()
                    condition.release()
                    time.sleep(3)

if __name__ == '__main__':
    producers = []
    custormers = []
    for i in range(PRODUCERS):
        producers.append(Producer(i))
    for i in range(CONSUMERS):
        custormers.append(Consumer(i))
    for p in producers:
        p.start()
    for c in custormers:
        c.start()