import requests
from bs4 import BeautifulSoup

def main():
    print("Googling address info")
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    
    # to search
    query = "615 E Waverly St Tucson Az zillow"
    
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        print(j)
    

    return

main()