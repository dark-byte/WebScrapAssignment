import csv
import requests
from bs4 import BeautifulSoup

baseUrl = "https://www.amazon.in"

record = []

def getData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    description = ""
    manufacturer = ""
    asin = ""
    prodDescription = ""

    try:
        descList= soup.find('div', id="feature-bullets").find_all('span')
        for desc in descList:
            description += desc.text
    except:
        description = ''


    try:
        prodDetails = soup.find('div', id="detailBullets_feature_div").find_all('span')
        manufacturer = prodDetails[8].text
        asin = prodDetails[11].text

    except:
        try:
            additionInfo = soup.find('table', id="productDetails_detailBullets_sections1").find_all('tr')
            for i in additionInfo:
                if (i.find('th').text == " ASIN "):
                   asin = i.find('td').text.strip()

            techDetails = soup.find('table', id="productDetails_techSpec_section_1").find_all('tr')
            for i in techDetails:
                if (i.find('th').text == ' Manufacturer '):
                    manufacturer = i.find('td').text.strip().replace('\u200e', '')
        except:
            asin = ""
            manufacturer = ""

    try:
        feautureDiv = soup.find('div', id="aplus_feature_div").find_all('p')
        for i in feautureDiv:
            prodDescription += i.text.strip()
    except:
        prodDescription = "  "

    return [description, manufacturer, asin, prodDescription]
    

with open("products.csv", 'r', encoding="utf8") as f:
    products = csv.reader(f)

    for product in products:
        if(product[0] == "Url"):
            continue
        print(baseUrl+product[0])
        data = getData(baseUrl+product[0])
        entry = product + data
        record.append(entry)


with open('products2.csv', 'w', encoding='utf8') as f:
    writer = csv.writer(f)
    header = ["Url", "Name", "Price", "Rating", "No of Reviews", "Description", "Manufacturer", "ASIN", "Product Description"]
    writer.writerow(header)
    writer.writerows(record)

print("Recorded entered successfully!")