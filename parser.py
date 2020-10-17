from fake_useragent import UserAgent
import requests
from lxml import html
from requests_html import HTMLSession
import lxml.html

def GetKoefs(startID, roundsAmount):
    ua = UserAgent()
    HEADERS = {
        'User-Agent': ua.opera
    }
    session = HTMLSession()
    for i in range(roundsAmount):
        startID-=1
        startURL = 'https://cs.fail/crash/history/' + str(startID)
        r = session.get(startURL, headers= HEADERS)
        r.html.render(sleep=1)
        #print(r.html.xpath('//meta[@name="description"]'))
        roundData = r.html.search('content="Game #{gameID} crashed at x{gameKoef} with ${gameBank} bank!"')
        print(f"Game #{roundData['gameID']}, koef = x{roundData['gameKoef']}")

    #response = requests.get(startURL, headers = HEADERS, encoding = 'utf-8')
    #response.request('https://cs.fail/runtime-es2015.1eba213af0b233498d9d.js')
    #response.encoding = 'utf-8'
    #print(response)
    #parsed = html.fromstring(response.text)

    #parsed1 = html.parse(response.text)
    #print(parsed.find_class('main'))
    #print(parsed.xpath('//a[@class="xhistory__link"]'))

if __name__ == '__main__':
    GetKoefs(699714, 15)

