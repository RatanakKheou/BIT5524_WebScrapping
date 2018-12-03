from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import csv


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    Error outputFile/ Wrong input # WARNING:
    """
    print("Incorrect INPUT")


def monthToNum(shortMonth):
    return{
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9,
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
    }[shortMonth]

def outputFile(linkInput, nameOutput):
    """
    Scrapping and Output the file by weeks in monthToNum
        - 'linkInput' will take a the link to scrap from and execute the valid link
        - 'nameOutput' the file name for the output along with Date

    """
    raw_html = simple_get(linkInput)
    html = BeautifulSoup(raw_html, 'html.parser')

    category = html.find_all("span", { "class":"eventcategory"})
    dates = html.find_all("td", {"align":"center", "valign":"top", "width":"14%"})
    itemInDate = html.find_all("td", {"bgcolor":"#f5f5eb", "class":"past", "valign":"top", "width":"14%"})

    tempDate = []
    tempDay = []

    i = 0
    for x in dates:
        splitTemp = x.get_text().split("\n")
        xTemp = splitTemp[2].split(" ")
        xxx = '{}/{}/2018'.format(monthToNum(xTemp[0]),xTemp[1])
        datetime_object = datetime.strptime(xxx, '%m/%d/%Y')
        tempDate.append(xxx)
        tempDay.append(splitTemp[1])
        i = i + 1

    events = []
    categoryID = []
    Dates = []
    Days = []
    j = 0
    for x in itemInDate:
        for y in x.find_all('b'):
            events.append(y.get_text())
            Dates.append(tempDate[j])
            Days.append(tempDay[j])
        j = j + 1

    for temp in category:
        categoryID.append(temp.get_text())

    toFile = pd.DataFrame(np.column_stack([events, categoryID, Dates, Days]), columns = ['Events', 'CategoryID', 'Date', 'Days'])
    fileName = '{}{}.csv'.format("C:\\Users\\krata\\Documents\\BIT 5524\\Scrapping\\", nameOutput)
    toFile.to_csv(fileName, index = False)
    print("Executed")

def scrapVTBegin(startDate, numDays):
    """
    Executing the Scrapping From startDate to number of day
        -'startDate' will take input '8/25/2018' format, OR 0 for default option
        -'numDays' number of day from the start date to scrap from, larger than 1
    """
    #Defualt links
    link1 = "https://www.calendar.vt.edu/main.php?view=week&timebegin="
    link2 = "+00%3A00%3A00&sponsorid=all&categoryid=0&keyword="
    #Default Date
    if startDate == 0:
        startDate = datetime.strptime('08/25/2018', '%m/%d/%Y')
    for nd in range(0, int(numDays/7)):
        startDate = startDate + timedelta(days=7)
        temp = startDate.strftime('%Y-%m-%d')
        link = '{}{}{}'.format(link1, temp, link2)
        fileNames = '{}_{}'.format("events", temp)
        print(temp)
        outputFile(link, fileNames)

def main():
    numDays = 98
    startDate = datetime.strptime('08/25/2018', '%m/%d/%Y')
    csvNames = []
    for nd in range(0, int(numDays/7)):
        startDate = startDate + timedelta(days=7)
        temp = startDate.strftime('%Y-%m-%d')
        fileNames = 'C:\\Users\\krata\\Documents\\BIT 5524\\Scrapping\\{}_{}.csv'.format("events", temp)
        csvNames.append(fileNames)

    append_list = []
    i = 0
    for np in csvNames[0:-1]:
        df = pd.read_csv(csvNames[i],index_col=None, header=0)
        append_list.append(df)
        i = i + 1
    frame = pd.concat(append_list, axis = 0)
    frame.to_csv("C:\\Users\\krata\\Documents\\BIT 5524\\Scrapping\\combinedFile.csv", index = False)
    print('Executed Succesfully')

if __name__ == '__main__':
    #  Execute the Scrap Using the scrapVTBegin() function
    #
    # DISCLAIMER: Only scrap till the most recent data and crash when no more new DataFrame
    #               is founded
    #
    #scrapVTBegin(0, 100)
     main()
