import requests
from bs4 import BeautifulSoup
import json

exportPath = "output/"
websiteUrl = "https://www.courdecassation.fr/"

def scrapDecision(url):
    print("Get : " + url)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        decisionContent = [section for section in soup.find_all("p", class_="decision-accordeon--contenu")]

        data = {}
        for content in decisionContent:
            lines = [line.strip() for line in "".join(content.strings).splitlines()]
            data[content.get("id")] = [line for line in lines if line != '']
        
        name = url.split("/")[-1]
        exportTojson(exportPath + name + ".json", data)

    else:
        print("Erreur lors de la requête: code de statut", response.status_code)

def scrapPage(url):
    print("Get : " + url)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        decisionLinks = [paragraph.find("a").get("href") for paragraph in soup.find_all("p", class_="lien-voir")]

        for link in decisionLinks:
            scrapDecision(websiteUrl + link)


        nextPageButton = soup.find("li", class_="pager__item--next")
        if nextPageButton == None:
            print("Scrap every page")
            return
        
        nextPageLink = nextPageButton.find("a").get("href")

        scrapPage(websiteUrl + nextPageLink)

    else:
        print("Erreur lors de la requête: code de statut", response.status_code)


def exportTojson(path, data): 
    print("Export : " + path)
    jsonStr = json.dumps(data, indent=4)

    with open(path, "w") as text_file:
        text_file.write(jsonStr)

def main():
    scrapPage("https://www.courdecassation.fr/recherche-judilibre?search_api_fulltext=Code+de+l%27entr%C3%A9e+et+du+s%C3%A9jour+des+%C3%A9trangers+et+du+droit+d%27asile&date_du=&date_au=&judilibre_juridiction=cc&op=Rechercher+sur+judilibre")

if __name__ == "__main__":
    main()