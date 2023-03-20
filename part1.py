import requests
from bs4 import BeautifulSoup
import csv

baseUrl = "https://www.amazon.in"
url = baseUrl + "/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

def getProducts(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def writeProduct(soup):
    prodList = soup.find_all(
        'div', class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16")

    print(prodList)

    for item in prodList:
        url = item.find('a', class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")['href']
        name = item.find('span', class_="a-size-medium a-color-base a-text-normal").text
        price = item.find('span', class_="a-price-whole").text
        try:
            rating = item.find('span', class_="a-size-base").text
        except:
            rating = "N/A"
        try:
            noOfRating = item.find('span', class_="a-size-base s-underline-text").text
        except:
            noOfRating = "N/A"
        product = [url, name, price, rating, noOfRating]
        writer.writerow(product)


def getNextUrl(soup):
    try:
        next = soup.find('a', class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")['href']
        url = baseUrl + str(next)
        return url
    except:
        return
   
with open('products.csv', 'w', encoding='utf8', newline='') as f:
    header = ['Url', 'Name', 'Price', 'Rating', 'No of Reviews']
    writer = csv.writer(f)
    writer.writerow(header)
    while True:
        print(url)
        soup = getProducts(url)
        writeProduct(soup)
        url = getNextUrl(soup)
        if(not url):
            print("Reached the end!")
            break
