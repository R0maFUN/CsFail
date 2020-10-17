from fake_useragent import UserAgent
from requests_html import HTMLSession
import csv

def GetKoefs(roundID, roundsAmount = 100, csv_filename = 'roundsData.csv'):
    ua = UserAgent()
    HEADERS = {
        'User-Agent': ua.opera
    }
    session = HTMLSession()
    with open(csv_filename, mode='w') as csv_file:
        fieldnames = ['gameID', 'gameKoef', 'gameBank']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(roundsAmount):
            roundURL = 'https://cs.fail/crash/history/' + str(roundID)
            r = session.get(roundURL, headers=HEADERS)
            r.html.render(sleep=1)
            roundData = r.html.search('content="Game #{gameID} crashed at x{gameKoef} with ${gameBank} bank!"')
            print(f"Game #{roundData['gameID']}, koef = x{roundData['gameKoef']}")
            writer.writerow({key: roundData[key] for key in fieldnames})
            print("[SAVED]")
            roundID -= 1

if __name__ == '__main__':
    GetKoefs(699714, 5)

