import threading
mutex = threading.Lock()

def critico(id):
    global x;
    x = x + id
    print("Hilo =" + str(id) + " =>" + str(x))
    x = 1

class Hilo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        print("a")

    def run(self):
        print("b")
        mutex.acquire()
        critico(self.id)
        mutex.release()
        print("b")
        
hilos = [Hilo(1), Hilo(2), Hilo(3)]
x=1;

for h in hilos:
    h.start()
