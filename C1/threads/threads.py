from mimetypes import init
from operator import indexOf
from urllib import response
import requests
from pytube import YouTube
import requests
import time
import concurrent.futures
import threading
import psycopg2

video_urls = [
    'https://youtu.be/FLG4hSChIss',
    'https://youtu.be/bMRosz1JZOA',
    'https://youtu.be/bwen5lsv23A',
    'https://youtu.be/SuKbG1wC_WI',
    'https://youtu.be/mtnBKbQStDM'
]

dataUrl = []
        
def service_video():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_video, video_urls)


def get_service_registro(url):
    response = requests.get(url)
    if response.status_code == 200 :
        data = response.json()
        write_db_registro(data)
    else:
        print('Error')

def connect_db_registro():
    con = psycopg2.connect(database="concurrente", user="postgres", password="batalla", host="localhost", port="5432")
    con.autocommit = True
    return con

def write_db_registro(data):   
    connection = connect_db_registro()
    cursor = connection.cursor()

    for dataOut in data:
        title = dataOut['title']
        query = f""" INSERT INTO practica1 (title) VALUES ('{title}') """
        cursor.execute(query)
        
def download_video(video_url):
    yt = YouTube(video_url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    print(f'{video_url} was downloaded...')

def get_services_iterar(dato=0):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
    if response.status_code == 200:
        results = response.json().get('results')
        Nom = results[dato].get('name')
        print(f'{dato+1}. {Nom}')
      
if __name__ == '__main__':
    url_site = ["https://jsonplaceholder.typicode.com/photos"]
    th2 = threading.Thread(target=get_service_registro, args=url_site)
    th2.start()
    for dataUrl in video_urls:
        th3 = threading.Thread(target=download_video, args=[dataUrl])
        th3.start() 
    for x in range(0,50):
        th1 = threading.Thread(target=get_services_iterar, args=[x])
        th1.start()