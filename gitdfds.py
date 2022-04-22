import requests
from bs4 import BeautifulSoup

url = 'https://github.com/n0-n4-m3/journal'
def get_git(url):
    url_compare = "https://github.com"
    commits = url + "/commits"
    r = requests.get(commits)
    soup = BeautifulSoup(r.text,"lxml")
    TimelineItem = soup.find_all("p",class_='mb-1')
    otvet = {}
    a = 0
    for i in TimelineItem:
        if a<10:
           #print(url_compare,i.find("a")["href"])
            url_compare = url_compare + i.find("a")["href"]
            r_commit = requests.get(url_compare)
            git_soup = BeautifulSoup(r_commit.text,"lxml")
            otvet[url_compare]={"mess":git_soup.find('div', class_="commit-title").text.strip(), "when":git_soup.find('relative-time').text.strip()}
            url_compare = "https://github.com"
            a+=1
        else:
            break
    print(otvet)
    return otvet


if __name__ == "__main__":
    get_git(url)