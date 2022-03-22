from ast import parse
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from googlesearch import search
import requests
import pandas as pd
import threading
import os
import time



# Globals
lck = threading.Lock()

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

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'zguid=23|%24f554463a-90f4-4ca4-a524-e5f9a4480913; zgsession=1|786d6cfe-4f7e-4ad8-bce6-79218384dcf8; JSESSIONID=52066B08D4B5C1CF021A24CF361C29C6; search=6|1649879766008%7Crb%3DTucson%252C-AZ%26rect%3D32.413417%252C-110.598737%252C31.922138%252C-111.577485%26sort%3Dpriorityscore%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%097481%09%09%09%09%09%09; AWSALB=Ltc3uX5WmVHokmMhLXGZ/0lYOMf4GHvSYJvxXG6tv7wYXD7Nj6J85tL7o6lovKQS8X3xw2/DvMMSS2FHewXN8x8qMk2ZVTe0AzBYB/1Eob2nFc4GcFS4m3ema5Hd; AWSALBCORS=Ltc3uX5WmVHokmMhLXGZ/0lYOMf4GHvSYJvxXG6tv7wYXD7Nj6J85tL7o6lovKQS8X3xw2/DvMMSS2FHewXN8x8qMk2ZVTe0AzBYB/1Eob2nFc4GcFS4m3ema5Hd',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.106 Safari/537.36'
    }

''':authority: www.zillow.com
:method: GET
:path: /search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Tucson%2C%20AZ%22%2C%22mapBounds%22%3A%7B%22west%22%3A-111.577485%2C%22east%22%3A-110.598737%2C%22south%22%3A31.922138%2C%22north%22%3A32.413417%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A7481%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22],%22cat2%22:[%22total%22]}&requestId=2
:scheme: https

user-agent: Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.106 Safari/537.36'''

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

def writeUsableGoogleResults(searchResults, number, direction, street):
    domain1 = "https://www.zillow.com/homedetails/"
    domain2 = "https://www.zillow.com/b/"
    address = ""
    for i in searchResults:
        if(i[:len(domain1)] == domain1 or i[:len(domain2)] == domain2):
            temp = i.split("/")
            parsedStreet = temp[4].split("-")
            index = findIndexofDirection(parsedStreet)
            tucsonIndex = findIndexofTucson(parsedStreet)
            tucsonIndex = len(parsedStreet) - tucsonIndex
            for itr in range(index):
                if((parsedStreet[itr] == number) and (parsedStreet[index] == direction)): # This will need to be fixed
                    if( street.lower() == buildAddress(parsedStreet[index + 1:-tucsonIndex]) ):
                        print(parsedStreet[index + 1:-tucsonIndex])
                        writeToFile(i)
    return 0

def doWork(i):
    i = i.split(",")
    query = i[1][1:-1] + " " + i[2][1:-1] + " " + i[3][1:-1] + " Tucson AZ zillow"
    webpageList=[]
    for result in search(query, tld="co.in", num=5, stop=10, pause=2):
        webpageList.append(str(result))
    writeUsableGoogleResults(webpageList, i[1][1:-1], i[2][1:-1], i[3][1:-1])

    return

def main():
    t = time.time()
    print("Googling address info")
    
    f = open("/home/arielv/zillow-api/SITUS.csv", "r")
    
    #tempList = ["https://www.zillow.com/homedetails/403-405-E-Delano-St-Tucson-AZ-85705/2065674707_zpid/"]
    #writeUsableGoogleResults(tempList, "403", "E", "Delano St")
    

    j = 0
    query = ""
    for i in f:
        if ( j == 10 ):
            print("stopping")
            break
        if ( j != 0 ):
            thread0 = threading.Thread(target=doWork, args=(i,))
            if not thread0.is_alive():
                try:
                    thread0.start()
                except:
                    thread0 = threading.Thread(target=doWork, args=(i,))
                    thread0.start()
            #writeUsableGoogleResults(webpageList, i[1][1:-1], i[2][1:-1], i[3][1:-1])
        j+=1
    #data.close()
    print("done in : ", time.time()-t)
    return


main()