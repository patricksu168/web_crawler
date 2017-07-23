import requests
import sys
import re
from bs4 import BeautifulSoup


def spider(url, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    products = []
    firstPage = 0
    while numberVisited < int(maxPages) and pagesToVisit != []:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            html_content = requests.get(url)
            html_text = html_content.text
            soup = BeautifulSoup(html_text, "html.parser")
            if firstPage == 0:
                for product in soup.findAll('ul', {'class': 'product_ul'}):
                    if numberVisited < int(maxPages):
                        product_name = product.find('li', {'class': 'product_name'})
                        product_page = product_name.find('a').get('href')
                        numberVisited, name, series, pagesToVisit = get_single_item(product_page, maxPages, numberVisited,
                                                                            pagesToVisit)
                        products.append((name, series))
                firstPage += 1
            else:

                numberVisited, name, series, pagesToVisit = get_single_item(url, maxPages, numberVisited,
                                                                            pagesToVisit)
                products.append((name, series))
            print(" **Success!**")
            #print(len(products))
        except:
            print(" **Failed!**")
    return products

def get_single_item(url, maxPages, numberVisited, pagesToVisit):
    if (numberVisited < int(maxPages)):
        print(numberVisited, "Visiting:", url)
        html_content = requests.get(url)
        html_text = html_content.text
        # print(html_text)
        soup = BeautifulSoup(html_text, "html.parser")
        product_name = soup.find('h2', {'class': 'heading_10'})
        product_name = re.sub("\<br\/.*", "", str(product_name))
        product_name = re.sub("\<h2.*\"\>", "", product_name)
        #print(product_name)
        product_spec = soup.find('dl', {'class': 'spec_data'})
        product_series = product_spec.find('dt', string='Series Title')
        if str(product_series) != "None":
            series = product_series.findNext('dd').find('a')
            if str(series) != "None":
                series_name = series.string
            else:
                series_name = "Original"
        else:
            series_name = "Original"
        #print(series_name)
        recommend = soup.find('ul', {'class': 'recommend'})
        if str(recommend) != "None":
            for links in recommend.findAll('a'):
                new_link = links.get('href')
                pagesToVisit.append(new_link)
                #print("new links is: " + new_link)
            #print(len(pagesToVisit))
        numberVisited += 1
        return numberVisited, product_name, series_name, pagesToVisit

