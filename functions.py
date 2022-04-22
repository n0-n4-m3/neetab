from libraries import *
import requests
from bs4 import BeautifulSoup

def make_problem(priority, who, problem_name, problem_dscr, make_date, dead_date, git):
    otvet = {
    "status": 0,
    "diff": priority, #ЭТО СЛОЖНОСТЬ
    "who": who,
    "git": git,
    "name_of_problem": problem_name,
    "dscr_of_problem": problem_dscr,
    "begin_date": make_date,
    "end_date": dead_date,
    "members": [],
    "progress": {"data": "77.77.77", "message": "Lorem Ipsum...."}
    }
    return otvet

def make_user(user_role, user_name, user_login, user_pas):
    user = {
    "user_role": user_role,
    "user_name": user_name,
    "user_login": user_login,
    "user_pas": user_pas,
    "my_problems": []
    }
    return user

def get_git(url):
    url_compare = "https://github.com"
    commits = url + "/commits"
    r = requests.get(commits)
    soup = BeautifulSoup(r.text,"lxml")
    TimelineItem = soup.find_all("p",class_='mb-1')
    otvet = []
    a = 0
    for i in TimelineItem:
        if a<3:
           #print(url_compare,i.find("a")["href"])
            url_compare = url_compare + i.find("a")["href"]
            r_commit = requests.get(url_compare)
            git_soup = BeautifulSoup(r_commit.text,"lxml")
            otvet.append({"mess":git_soup.find('div', class_="commit-title").text.strip(), "when":git_soup.find('relative-time').text.strip(),"url":url_compare})
            url_compare = "https://github.com"
            a+=1
        else:
            break
    return otvet