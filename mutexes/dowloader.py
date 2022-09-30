import threading
import pytube

mutex=threading.Lock()

def critico(id):
    global x;
    x = x + id
    print("Hilo =" + str(id) + " =>" + str(x))
    x = 1

def download_videos(id):
    video_urls = [
    'https://youtu.be/FLG4hSChIss',
    'https://youtu.be/bMRosz1JZOA',
    'https://youtu.be/bwen5lsv23A',
    'https://youtu.be/SuKbG1wC_WI',
    'https://youtu.be/mtnBKbQStDM'
    ]
    pytube.YouTube(video_urls[id-1]).streams.first().download()
    print(f'{video_urls[id-1]} was downloaded...')  

class Hilo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        mutex.acquire()
        critico(self.id)
        download_videos(self.id)
        mutex.release()
        
threads_mutex = [Hilo(1), Hilo(2), Hilo(3), Hilo(4), Hilo(5)]
x=1;

for h in threads_mutex:
    h.start()
