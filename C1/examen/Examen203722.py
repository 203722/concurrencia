import threading
import random
import time

cant = 8

palillos = []
comer = []
personas = []

def agarrar(id_persona):
    izq = palillos[id_persona]
    der = palillos[(id_persona-1) % cant]
    izq.acquire()
    
    if der.acquire():
        return True
    else:
        izq.release()
        return False
    
def soltar(id_persona, tiempo):
    palillos[id_persona].release()
    palillos[(id_persona-1) % cant].release()
    print(f"Persona numero {id_persona+1} terminó de comer en {round(tiempo)} segundos.")
    
def eating(id_persona):
    if agarrar(id_persona):
        print(f"Persona numero {id_persona+1} esta comiendo")
        comer.append(id_persona+1)
        
        dif = set(personas).difference(set(comer))
        dif1 = set(comer).difference(set(personas))
        mostrar = list(dif.union(dif1))

        print(f"Personas esperando un palillo: {mostrar}")
        
        tiempo_comer = random.uniform(1,5)
        time.sleep(tiempo_comer)
        
        soltar(id_persona, tiempo_comer)
            
if __name__ == '__main__':
    hilos = []
    
    for _ in range(cant):
        palillos.append(threading.Lock())
    
    for i in range(cant):
        personas.append(i+1)
        nuevo_hilo = threading.Thread(target=eating, args=(i,))
        hilos.append(nuevo_hilo)
    
    for hilo in hilos:
        hilo.start()
