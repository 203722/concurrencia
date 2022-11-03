from queue import Queue                        #Marcos alejandro shilon gallegos - 203459
import threading                               #Jose Adrian Batalla Cruz - 203722
import time
import random

CAPACIDAD = 15
CLIENTES = 20
RESERVACIONES = round(CAPACIDAD*0.2)
MESEROS = COCINEROS = round(CAPACIDAD * 0.1)

class Restaurante():
  mutex = threading.Lock()
  clientes = threading.Condition()
  mesero = threading.Condition()
  cocinero = threading.Condition()
  clientes_reservacion = threading.Condition()
  adentro = Queue(CAPACIDAD)
  ordenes = Queue()
  comidas = Queue()
  reservaciones = Queue(RESERVACIONES)

  def __init__(self):
    super(Restaurante, self).__init__()

  def en_cola(self, cliente):
    self.clientes_reservacion.acquire()
    print(f"Cliente {cliente.id} está en la cola")
    time.sleep(1)
    self.mutex.acquire()
    self.entrar(cliente)
    self.clientes_reservacion.notify()
    self.clientes_reservacion.release()

  def reservacion(self, cliente):
    self.clientes_reservacion.acquire()
    if self.reservaciones.full():
            self.clientes_reservacion.wait()
    else:
            self.reservaciones.put(cliente)
            print(f"Cliente {str(cliente.id)} ingresó a la cola, con reservación")
            time.sleep(5)
            print(f"Cliente {str(cliente.id)} llegó al restaurante, con reservación")
            time.sleep(1)

            self.mutex.acquire()
            self.entrar(cliente)
            self.reservaciones.get()

            self.clientes_reservacion.notify()
            self.clientes_reservacion.release()

  def entrar(self, cliente):
    self.clientes.acquire()
    if self.adentro.full():
      print(f"el restaurante está lleno, cliente {cliente.id} esperando")
      self.clientes.wait()
    else:
      print(f"Cliente {cliente.id} entro al rstaurante")
      time.sleep(1)
      self.adentro.put(cliente)
      print(f"El recepcionista asigna una mesa a el cliente {cliente.id}")
      self.mesero.acquire()
      self.mesero.notify()
      self.mesero.release()
      self.mutex.release()
      self.clientes.release()

  def ordenar(self, mesero):
    while True:
      time.sleep(1)
      self.mesero.acquire()
      if self.adentro.empty():
        print(f"Mesero {mesero.id} está descansando")
        self.mesero.wait()
      else:
        cliente = self.adentro.get()
        if cliente.atendido == False:
          print(f"Mesero {mesero.id} tomando orden a cliente {cliente.id}")
          time.sleep(1)
          print(f"El pedido del cliente {cliente.id} se añadió a la lista")
          self.ordenes.put(cliente.id)
          self.cocinero.acquire()
          self.cocinero.notify()
          self.cocinero.release()
          cliente.atendido = True
          self.mesero.release()
        else:
          self.mesero.release()

  def cocinar(self, cocinero):
      while True:
            time.sleep(1)
            self.cocinero.acquire()
            if self.ordenes.empty():
                print(f"COCINERO {str(cocinero.id)} está descansando")
                self.cocinero.wait()
            else:
                order = self.ordenes.get()
                print(f"COCINERO {str(cocinero.id)} está cocinando el pedido de Cliente {order}")
                time.sleep(3)
                print(f"el pedido de Cliente {order} está listo")
                self.comidas.put(order)
                self.cocinero.release()

  def comer(self):
    time.sleep(1)
    if not self.comidas.empty():
            cliente = self.comidas.get()
            print(f"Cliente {cliente} está comiendo")
            time.sleep(4)
            print(f"Cliente {cliente} terminó de comer")
            print(f"Cliente {cliente} se fué del restaurante")

class Cliente(threading.Thread):
  conta = 1
  atendido = False

  def __init__(self, reservacion):
    super(Cliente, self).__init__()
    self.id = Cliente.conta
    self.reservacion = reservacion
    Cliente.conta += 1
    
  def run(self):
    time.sleep(1)
    if self.reservacion:
      restaurante.reservacion(self)
    else:
      restaurante.en_cola(self)
    restaurante.comer()

class Mesero(threading.Thread):
  conta = 1

  def __init__(self):
    super(Mesero, self).__init__()
    self.id = Mesero.conta
    Mesero.conta += 1

  def run(self):
    restaurante.ordenar(self)

class Cocinero(threading.Thread):
  conta = 1

  def __init__(self):
    super(Cocinero, self).__init__()
    self.id = Cocinero.conta
    Cocinero.conta += 1

  def run(self):
    restaurante.cocinar(self)

def main():
  Hilos = []
  for i in range(CLIENTES):
    con_reservacion = bool(random.choice([0, 0, 1]))
    Hilos.append(Cliente(con_reservacion))
  for i in range(MESEROS):
    Hilos.append(Mesero())
  for i in range(COCINEROS):
    Hilos.append(Cocinero())
  for aux in Hilos:
    aux.start()

if __name__ == '__main__':
    restaurante = Restaurante()
    main()