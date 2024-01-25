from bs4 import BeautifulSoup
import requests
import re

from DataDto import DataDto


def getLinks(channelname, content, parenturl, free):
    links = list()
    soup = BeautifulSoup(content, 'html.parser')
    videos = soup.findAll('li', attrs={'class': 'pcVideoListItem'})

    for v in videos:
        link = v.a['href']
        title = v.a['title']

        if free:
            freeblock = v.findAll('span', attrs={'class', 'phpFreeBlock'})
            if len(freeblock) > 0:
                title = title.replace("\"", "").replace("\'", "").replace(" ", "_")
                pattern = r'[^0-9a-zA-Z_-]'
                processed = re.sub(pattern, '-', title)
                links.append(DataDto(parenturl + link, channelname + "_"  +processed, "MULTI_FILE"))

        else:
            title = title.replace("\"", "").replace("\'", "").replace(" ", "_")
            pattern = r'[^0-9a-zA-Z_-]'
            processed = re.sub(pattern, '-', title)
            links.append(DataDto(parenturl + link, channelname + "_"  +processed, "MULTI_FILE"))

    return links

def writeInputFile(dataDtoList: set):
    f = open("input.txt", 'w', encoding='UTF-8')
    pattern = r'[^0-9a-zA-Z_-]'
    for dto in dataDtoList:
        f.write(dto + "\n")
    f.close()


if __name__ == "__main__":
    records = set()
    channel = ""    # the channel name
    parentUrl = ""  # the parent url
    isFree = True
    url = ""    # the /videos page (which should include the parent url - i.e the absolute url path)
    for i in range(1, 1000):
        pageUrl = url + "?page=" + str(i)
        res = requests.get(pageUrl)
        if "Error Page Not Found" in res.text:
            print("Page does not exist.[ " + pageUrl + " ]. Exiting")
            break
        lines = getLinks(channel, res.content, parentUrl, isFree)
        for line in lines:
            records.add(line.getRecord())

    writeInputFile(records)