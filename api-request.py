import requests

def main():
    print("Using Zillow API")
    url = "http://www.zillow.com/webservice/GetSearchResults.htm?"
    address = "615 E Waverly St, Tucson, AZ 85705"
    payload = "zws-id=X1-ZWz1innmra8v0r_1mzvh"
    headers = {
        'content-type' : " application/x-www-form-urlencoded",
    }

    #response = requests.request("POST", url, data=payload, headers=headers)
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

    return

main()