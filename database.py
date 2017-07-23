import web_scrawler

def main():
    url = 'http://www.amiami.com/top/page/c/bishoujo.html'
    maxPages = 200
    products = web_scrawler.spider(url, maxPages)
    mydb = {}
    for p in products:
        product, series = p
        if series in mydb:
            mydb[series] += 1
        else:
            mydb[series] = 0
            mydb[series] += 1
    for s in mydb.keys():
        print(str(s) + " : " + str(mydb[series]) + " products on the site")

main()