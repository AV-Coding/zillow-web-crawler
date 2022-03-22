from ast import parse
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from googlesearch import search
from queue import Queue
import requests
import pandas as pd
import threading
import os
import time



# Globals
lck = threading.Lock()
#sema = threading.Semaphore(value=100)
#threads = list()
jobs = Queue()

abbreviations = {}
abbreviations["rd"]=1
abbreviations["st"]=1
abbreviations["ave"]=1
abbreviations["pl"]=1
abbreviations["bl"]=1
abbreviations["blvd"]=1
abbreviations["dr"]=1
abbreviations["ln"]=1
abbreviations["av"]=1
abbreviations["way"]=1
abbreviations["wy"]=1
abbreviations["cir"]=1
abbreviations["ci"]=1
abbreviations["ct"]=1
abbreviations["loop"]=1
abbreviations["lp"]=1
abbreviations["ln"]=1

directions = {}
directions["n"] = 1
directions["e"] = 1
directions["s"] = 1
directions["w"] = 1

def writeToFile(text):
    global lck
    lck.acquire()
    with open("/home/arielv/zillow-api/data.log", 'a') as f:
        f.write(text + '\n')
    lck.release()

def findIndexofTucson(parsedStreet):
    j = 0
    for j in range(len(parsedStreet)):
        if( parsedStreet[j].lower() == "tucson" ):
            return j
    return -1

def findIndexofDirection(parsedStreet):
    j = 0
    for j in range(len(parsedStreet)):
        if(parsedStreet[j].lower() in directions.keys()):
            return j
    return -1

def buildAddress(parsedAddress):
    address = ""
    for x in parsedAddress:
        if(x.lower() == "unit" or x.lower() == "apt" or x.lower() == "suite" or x.isnumeric() or x[1:].isnumeric()):
            break
        else:
            if(x.lower() == "blvd"):
                x = "bl"
            elif(x.lower() == "ave"):
                x = "av"
            elif(x.lower() == "way"):
                x = "wy"
            elif(x.lower() == "cir"):
                x = "ci"
            elif(x.lower() == "loop"):
                x = "lp"
            address += str(x).lower() + " "
    return address[:-1]

def writeUsableGoogleResults(query):
        link = "https://www.google.com/search?q=" + query
        writeToFile(link)
        return 0

def doWork(q):
    while not q.empty():
        #sema.acquire()
        i = q.get().split(",")
        #i.replace(" ", "+")
        number = i[1][1:-1].replace(" ", "+")
        direction = i[2][1:-1].replace(" ", "+")
        street = i[3][1:-1].replace(" ", "+")
        #query = i[1][1:-1] + "+" + i[2][1:-1] + "+" + i[3][1:-1] + "+Tucson+AZ+zillow"
        query = number + "+" + direction + "+" + street + "+Tucson+AZ+zillow"
        #query = i + "+Tucson+AZ+zillow"
        writeUsableGoogleResults(query)
        #time.sleep(1)
        #sema.release()
    return

def main():
    t = time.time()
    print("Googling address info")
    
    f = open("/home/arielv/zillow-api/SITUS.csv", "r")
    line = 0
    for j in f:
        if (line < 414165):
            jobs.put(j)
            line+=1
        else:
            break
    
    for i in range(1000):
        worker = threading.Thread(target=doWork, args=(jobs,))
        worker.start()
        print(threading.active_count())
    
    jobs.join()
'''    j = 0
    query = ""
    threads = [threading.Thread(name="worker/task", target=doWork, args=(i,)) for i in f]
    for thread in threads:
        thread.start()
        print(threading.active_count())
    for thread in threads:
        thread.join()
        print(threading.active_count())
    print("done in : ", time.time()-t)
    return
        if ( j == 100000 ):
            print("stopping")
            break
        if ( j != 0 ):
            thread0 = threading.Thread(target=doWork, args=(i,))
            threads.append(thread0)
            thread0.start()
            print(threading.active_count())
        j+=1
    print("done in : ", time.time()-t)
    return

            if not thread0.is_alive():
                try:
                    thread0.start()
                except:
                    thread0 = threading.Thread(target=doWork, args=(i,))
                    thread0.start()
        
    #data.close()
    print("done in : ", time.time()-t)
    return'''


main()