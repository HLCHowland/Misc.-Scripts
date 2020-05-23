import requests, re
from time import sleep
from bs4 import BeautifulSoup
from termcolor import colored
from random import randint, choice

printing = False


def get_valid_url():
    print("\nWhat is the id number or url of the quizlet course?")
    qset = input()
    url_regex = re.compile(r"^(https://quizlet.com/)?(?P<id>\d{4,15})(/[\w-]{1,1000})?/?$")
    id_regex = re.compile(r"^\d{4,15}$")
    match = url_regex.search(qset)
    if match:
        if printing: print("match:", match.group(0), "\n\n")
        url = "https://quizlet.com/" + match.group("id")

        if printing: print("returning ", url, "\t In get_valid_input()")
        return url

    else:
        if printing: print("match: ", match)
        print("That is not a valid id or url. Please enter the string of numbers following \"quizlet.com\" in the url")
        sleep(0.3)
        print("For example: \"4071437\"")
        sleep(0.2)
        get_valid_url()


def scrape_data(url):
    """
    returns list of many dicts: each contains a term and a definition value
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # msg_404 = "There is no set with the ID you specified"
    msg_404 = "Page Unavailable"
    bodyContent = soup.select("div.SetPage-terms")
    if msg_404 in str(soup.body):
        # check for 404
        print("sorry m8, that isn't a valid quizlet course")

    else:
        if printing: print("YaY!!! real web page. Scraping data....")
        # YAY real page! Now let's do the work of extracting the terms and definitions
        data = []  # data will be a list containing many dicts with term and definition keys
        content = soup.select("div.SetPage-terms")[0]
        pairs = content.select("div.SetPageTerm-content")
        for pair in pairs:
            term = pair.select("span.TermText")[0].get_text()
            defn = pair.select("span.TermText")[1].get_text()
            data.append({
                "term": term,
                "definition": defn
            })
            if printing:
                print(colored("term: ", "blue"), term)
                print(colored("definition: ", "green"), defn)
    if printing: print("\nDONE SCRAPING DATA\n\n")
    return data


def prompt_user(data):
    pair = choice(data)
    if printing: print("pair is ", pair)
    t = pair["term"]
    d = pair["definition"]
    print(d)
    ans = input()
    if ans.lower() == t.lower():
        print(colored("Correct!", "green"))
    else:
        print(colored("Incorrect.", "red"), " The answer was ", t)


def main():
    url = get_valid_url()
    if printing: print("Getting data from\t", url)
    data = scrape_data(url)
    run = True
    while run:
        prompt_user(data)
        print("press q to quit or enter to continue")
        if input() == "q": run = False


main()
