from fake_useragent import UserAgent
from requests_html import HTMLSession
import csv
import pandas

def SortCSV(csv_filename = 'roundsData.csv'):
    with open(csv_filename) as csvfile:
        spamreader = csv.DictReader(csvfile)
        sortedlist = sorted(spamreader, key=lambda row: (row['gameID']), reverse=True)
    with open(csv_filename, 'w') as f:
        fieldnames = ['gameID', 'gameKoef', 'gameBank']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)
    pan = pandas.read_csv(csv_filename, index_col='gameID')
    pan.drop_duplicates(keep='first', inplace=True)
    pan.to_csv(csv_filename)


def GetKoefs(roundID, roundsAmount = 100, csv_filename = 'roundsData.csv'):
    ua = UserAgent()
    HEADERS = {
        'User-Agent': ua.opera
    }
    session = HTMLSession()

    csvFirstRoundID = int(pandas.read_csv(csv_filename, nrows=1).gameID[0])
    csvLastRoundID = 0
    with open(csv_filename, 'r') as f:
        last_line = f.readlines()[-2].strip().split(",")
        csvLastRoundID = int(last_line[0])
    print(f"{csvFirstRoundID}  {csvLastRoundID}")

    if int(roundID) <= int(csvFirstRoundID) :
        if int(roundID)-int(roundsAmount)+1 >= int(csvLastRoundID) :
            print("These rounds are already in the database")
            return
        elif roundID >= csvLastRoundID :
            roundsAmount -= roundID - csvLastRoundID + 1
            roundID = int(csvLastRoundID)-1
    elif int(roundID)-int(roundsAmount) <= int(csvFirstRoundID):
        roundsAmount = roundID - csvFirstRoundID
    print(f"roundID = {roundID} , roundsAmount = {roundsAmount}")
    with open(csv_filename, mode='a') as csv_file:
        fieldnames = ['gameID', 'gameKoef', 'gameBank']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()
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
    GetKoefs(699710, 6)
    SortCSV()

