from queue import Queue
import threading
import random
import time

total_clientes = 10
capacidad = 10
meseros_total = chef = int(capacidad * 0.1)
reservaciones = int(capacidad * 0.2)

class restaurant():
    mutex = threading.Lock()
    capacity_condition = threading.Condition()
    waiter_condition = threading.Condition()
    chef_condition = threading.Condition()
    reservation_condition = threading.Condition()

    restaurant_queue = Queue(capacidad)
    orders = Queue()
    food = Queue()
    reservation_queue = Queue(reservaciones)

    def __init__(self):
        super(restaurant, self).__init__()

    def llegada(self, clientes):
        self.reservation_condition.acquire()
        print(f"el cliente {str(clientes.id)} llegó al restaurante")
        time.sleep(1)

        self.mutex.acquire()
        self.entrada(clientes)

        self.reservation_condition.notify()
        self.reservation_condition.release()

    def reservacion(self, clientes):
        self.reservation_condition.acquire()
        if self.reservation_queue.full():
            self.reservation_condition.wait()
            self.mutex.acquire()
            self.entrada(clientes)
            self.reservation_condition.notify()
            self.reservation_condition.release()
            self.reservation_queue.get()

    def entrada(self, clientes):
        self.capacity_condition.acquire()
        if self.restaurant_queue.full():
            print(f"el cliente {str(clientes.id)} está esperando una mesa")
            self.capacity_condition.wait()
        else:
            print(f"el cliente {str(clientes.id)} entró al restaurante")
            time.sleep(2)
            self.restaurant_queue.put(clientes)
            print(f"el cliente {str(clientes.id)} se le a asignado una mesa")

            self.waiter_condition.acquire()
            self.waiter_condition.notify()
            self.waiter_condition.release()

            self.mutex.release()
            self.capacity_condition.release()

    def _serve(self, waiter):
        while True:
            time.sleep(2)
            self.waiter_condition.acquire()
            if self.restaurant_queue.empty():
                print(f"el mesero {str(waiter.id)} está descansando")
                self.waiter_condition.wait()
            else:
                clientes = self.restaurant_queue.get()
                if clientes.served == False:
                    print(
                        f"el mesero {str(waiter.id)} atiende al cliente {str(clientes.id)}")
                    print(
                        f"la orden del cliente {str(clientes.id)} se añadió a la cola")
                    self.orders.put(clientes.id)

                    self.chef_condition.acquire()
                    self.chef_condition.notify()
                    self.chef_condition.release()

                    clientes.served = True
                    self.waiter_condition.release()
                else:
                    self.waiter_condition.release()

    def cocinar(self, chef):
        while True:
            time.sleep(1)
            self.chef_condition.acquire()
            if self.orders.empty():
                print(f"COCINERO {str(chef.id)} está descansando")
                self.chef_condition.wait()
            else:
                order = self.orders.get()
                print(
                    f"COCINERO {str(chef.id)} está cocinando el pedido de el cliente {order}")
                time.sleep(3)
                print(f"el pedido de el cliente {order} está listo")
                self.food.put(order)
                self.chef_condition.release()
    def comiendo(self):
        time.sleep(1)
        if not self.food.empty():
            clientes = self.food.get()
            print(f"el cliente {clientes} está comiendo")
            time.sleep(4)
            print(f"el cliente {clientes} terminó de comer")
            print(f"el cliente {clientes} se fué")
class Client(threading.Thread):
    count = 1
    served = False

    def __init__(self, reservation):
        super(Client, self).__init__()
        self.id = Client.count
        self.reservation = reservation
        Client.count += 1

    def start(self):
        time.sleep(0.2)
        if self.reservation:
            monitor.reservacion(self)
        else:
            monitor.llegada(self)
        monitor.comiendo()


class Waiter(threading.Thread):
    count = 1

    def __init__(self):
        super(Waiter, self).__init__()
        self.id = Waiter.count
        Waiter.count += 1

    def start(self):
        monitor._serve(self)


class Chef(threading.Thread):
    count = 1

    def __init__(self):
        super(Chef, self).__init__()
        self.id = Chef.count
        Chef.count += 1

    def start(self):
        monitor.cocinar(self)

def main():
    clientes = []
    meseros = []
    chefs = []
    
    for i in range(total_clientes):
        reservation_luck = bool(random.choice([0, 0, 1]))
        clientes.append(Client(reservation_luck))
    for i in range(meseros_total):
        meseros.append(Waiter())
    for i in range(chef):
        chefs.append(Chef())
    for cliente in clientes:
        cliente.start()
    for waiter in meseros:
        waiter.start()
    for chef1 in chefs:
        chef1.start()

if __name__ == '__main__':
    monitor = restaurant()
    main()