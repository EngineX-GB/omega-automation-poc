import os
import urllib
import requests
import re

from DataDto import DataDto


def extractData(url: str, channelName:str, parentUrl : str, mode : str):
    dataDtoList = []
    source = requests.get(url)
    if "Error Page Not Found" in source.text:
        print ("Page does not exist.[ " + url + " ]. Exiting")
        return []
    results = re.findall("<a href=\"(/view_video.php\\?viewkey\\=[a-zA-Z0-9]+)\"\\stitle\\=(.*)\"\\sclass", source.text,
                         0)
    for result in results:
        title = result[1].replace("\"", "") .replace("\'", "").replace(" ", "_")
        pattern = r'[^0-9a-zA-Z_-]'
        processed= re.sub(pattern, '-', title)
        dataDtoList.append(DataDto(parentUrl + result[0], channelName + "_" +processed, mode))
    return dataDtoList


def writeInputFile(dataDtoList: set):
    f = open("input.txt", 'w', encoding='UTF-8')
    pattern = r'[^0-9a-zA-Z_-]'
    for dto in dataDtoList:
        f.write(dto.getRecord() + "\n")
    f.close()


if __name__ == "__main__":
    totalList = []
    for i in range(1,5):
        linkData = extractData("/videos?page="+str(i), "",
                               "", "MULTI_FILE")
        if len(linkData) == 0:
            break
        else:
            for j in linkData:
                totalList.append(j)
    filteredSet = set(totalList)
    writeInputFile(filteredSet)
