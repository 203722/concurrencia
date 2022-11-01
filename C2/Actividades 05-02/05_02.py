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
    capacidad_I = threading.Condition()
    mesero_E = threading.Condition()
    chef_A = threading.Condition()
    condicion_R = threading.Condition()

    rest = Queue(capacidad)
    ordenes = Queue()
    comida = Queue()
    cola_R = Queue(reservaciones)

    def __init__(self):
        super(restaurant, self).__init__()

    def llegada(self, clientes):
        self.condicion_R.acquire()
        print(f"el cliente {str(clientes.id)} llegó al restaurante")
        time.sleep(1)

        self.mutex.acquire()
        self.entrada(clientes)

        self.condicion_R.notify()
        self.condicion_R.release()

    def reservacion(self, clientes):
        self.condicion_R.acquire()
        if self.cola_R.full():
            self.condicion_R.wait()
            self.mutex.acquire()
            self.entrada(clientes)
            self.condicion_R.notify()
            self.condicion_R.release()
            self.cola_R.get()

    def entrada(self, clientes):
        self.capacidad_I.acquire()
        if self.rest.full():
            print(f"el cliente {str(clientes.id)} está esperando una mesa")
            self.capacidad_I.wait()
        else:
            print(f"el cliente {str(clientes.id)} entró al restaurante")
            time.sleep(2)
            self.rest.put(clientes)
            print(f"el cliente {str(clientes.id)} se le a asignado una mesa")

            self.mesero_E.acquire()
            self.mesero_E.notify()
            self.mesero_E.release()

            self.mutex.release()
            self.capacidad_I.release()

    def _serve(self, mesero_X):
        while True:
            time.sleep(2)
            self.mesero_E.acquire()
            if self.rest.empty():
                print(f"el mesero {str(mesero_X.id)} está descansando")
                self.mesero_E.wait()
            else:
                clientes = self.rest.get()
                if clientes.served == False:
                    print(
                        f"el mesero {str(mesero_X.id)} atiende al cliente {str(clientes.id)}")
                    print(
                        f"la orden del cliente {str(clientes.id)} se añadió a la cola")
                    self.ordenes.put(clientes.id)

                    self.chef_A.acquire()
                    self.chef_A.notify()
                    self.chef_A.release()

                    clientes.served = True
                    self.mesero_E.release()
                else:
                    self.mesero_E.release()

    def cocinar(self, chef):
        while True:
            time.sleep(1)
            self.chef_A.acquire()
            if self.ordenes.empty():
                print(f"COCINERO {str(chef.id)} está descansando")
                self.chef_A.wait()
            else:
                order = self.ordenes.get()
                print(
                    f"COCINERO {str(chef.id)} está cocinando el pedido de el cliente {order}")
                time.sleep(3)
                print(f"el pedido de el cliente {order} está listo")
                self.comida.put(order)
                self.chef_A.release()
    def comiendo(self):
        time.sleep(1)
        if not self.comida.empty():
            clientes = self.comida.get()
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