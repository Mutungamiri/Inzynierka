from signal import signal, SIGINT
from sys import exit
from pcf8574 import PCF8574
import os
import datetime
import MySQLdb
import time
import RPi.GPIO as GPIO
global c
global db

wyjscia_bus = PCF8574(1, 0x20) #przypisanie adresu wyjsciom
wejscia_bus = PCF8574(1, 0x21) #przypisanie adresu wejsciom
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # przypisanie GPIO4 dla
portu INT
wejscia_bus.port = [True, True, True, True, True, True, True, True] #ustawienie stanow na wejsciach i wyjsciach
wyjscia_bus.port = [False, False, False, False, False, False, False, False]
def printFunction2(channel): #Funkcja wypisujaca stany wejsc
    print("INT triggered-wejscie")
    print(wejscia_bus.port)
GPIO.add_event_detect(4, GPIO.FALLING, callback=printFunction2, bouncetime=100)
# aktywacja przerwan

def insert_to_database(stan, id_czujnika): #funkcja wpisujaca stany czujników do bazy danych
    now = datetime.datetime.now()
    data_czas = now.strftime("%Y-%m-%d %H:%M:%S")
    print(data_czas," - ",stan," - ",id_czujnika)
    sql = "INSERT INTO Pomiary_Czujniki (data_czas, stan_czujnika, ID_czujnika) VALUES (%s, %s, %s)"
    try:
        c.execute(sql,( str(data_czas) , int(stan) , int(id_czujnika)))
        db.commit()
    except:
        db.rollback()

def read_from_database(): #funkcja odczytujaca z bazy danych przeznaczona do weryfikacji poprawnosci wpisywania stanów czujników
    try:
        c.execute("SELECT * FROM Pomiary_Czujniki ORDER BY ID DESC LIMIT 1")
        result = c.fetchall()
        if result is not None:
            print (’Data i czas: ’ , result[0][1], ’|Stan: ’ , result[0][2], ’| ID Czujnika: ’ , result[0][3])
    except:
        print("Blad odczytu")

def handler(signal_received, frame):
    GPIO.cleanup()
    print(’Exiting the process’)
    exit(0)

def system_aktywny(): #funkcja symulujaca działanie uzbrojonego systemu alarmowego
    while True:
        if wejscia_bus.port[7] == False:
            insert_to_database(wejscia_bus.port[7], 8)
            time.sleep(2)
            insert_to_database(wejscia_bus.port[7], 8)
            wyjscia_bus.port[7] = True
        if wejscia_bus.port[6] == False:
            insert_to_database(wejscia_bus.port[6], 7)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[6], 7)
            wyjscia_bus.port[7] = True
        if wejscia_bus.port[5] == False:
            insert_to_database(wejscia_bus.port[5], 6)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[5], 6)
            wyjscia_bus.port[7] = True
        if wejscia_bus.port[4] == False:
            insert_to_database(wejscia_bus.port[4], 5)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[4], 5)
            wyjscia_bus.port[7] = True
        if wejscia_bus.port[3] == False:
            insert_to_database(wejscia_bus.port[3], 4)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[3], 4)
            wyjscia_bus.port[6] = True
        if wejscia_bus.port[2] == False:
            insert_to_database(wejscia_bus.port[2], 3)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[2], 3)
            wyjscia_bus.port[6] = True
        if wejscia_bus.port[1] == False:
            insert_to_database(wejscia_bus.port[1], 2)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[1], 2)
            wyjscia_bus.port[5] = True
        if wejscia_bus.port[0] == False:
            insert_to_database(wejscia_bus.port[0], 1)
            time.sleep(1)
            insert_to_database(wejscia_bus.port[0], 1)
            wyjscia_bus.port[5] = True
        if wyjscia_bus.port[7] == True or wyjscia_bus.port[6] == True or
            wyjscia_bus.port[5] == True:
            print("W celu dezaktywacji przyloz karte")
            deactivate = input()
            if deactivate == ’0000005200’:
            wyjscia_bus.port = [False, False, False, False, False, False, False, False]
            again()

def again(): #funkcja uzbrajajaca system
    karta_rfid = input(’’’Przyloz karte w celu aktywowania systemu’’’)
    if karta_rfid == ’0000005200’:
        system_aktywny()
    else:
        print("Karta nie poprawna")
        again()

if __name__ == ’__main__’:
    signal(SIGINT, handler)
    try:
        db = MySQLdb.connect("localhost","root","test","System_alarmowy")
        #łaczenie sie z baza danych
        c = db.cursor()
    except:
        print("Nie mozna sie polaczyc z Serwerem")
        again()