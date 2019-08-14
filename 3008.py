# This file takes the csv files of Image and Text Schema given by the prof and calculates statistics and creates histograms and bar graphs

import csv
import statistics
import datetime
import numpy as np
import copy
import matplotlib.pyplot as plt

#First both files are simply combined into one csv file

with open('combined.csv', 'w') as comb_file:
    csv_writer = csv.writer(comb_file, delimiter=',')
    with open('imagept21.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            csv_writer.writerow(line)
    with open('text21.csv', 'r') as csv2_file:
        csv_reader2 = csv.reader(csv2_file)
        for line in csv_reader2:
            csv_writer.writerow(line)

    csv_reader3 = csv.reader(comb_file)
    userslogins = {}        # holds all users in a dictionary where you can get specific user data
    loginmap = {}           # the individual users data containing array with times and number of logins and what type of schema it is

# combined file is read line by line and dictionary is made with users individual data

with open('combined.csv', 'r') as comb_file:
    startBefore = False
    csv_reader3 = csv.reader(comb_file)
    loginmap = {}
    username = ""
    for row in csv_reader3:
        if row[1] != username:
            username = row[1]
            loginmap = {"successtimes":[],"failtimes":[],"ImageOrText":row[3]}
        var = "login"
        if row[5] == var:
            timedifference = datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S') - datetimeobj
            timediff = timedifference.total_seconds()
            if row[6] in loginmap:
                loginmap[row[6]] = loginmap.get(row[6]) + 1
            else:
                loginmap[row[6]] = 1
                userslogins[username] = loginmap
            if row[6] == "success" and startBefore:
                loginmap["successtimes"].append(timediff)
                startBefore = False
            else:
                if(startBefore):
                    loginmap["failtimes"].append(timediff)
        if row[5] == "enter" and row[6] == "start":
            datetimeobj = datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S')
            startBefore = True

#below lists are created for the purpose of making histograms and calculating means

successlist = []
failurelist = []
totallist = []
successtimeslist= []
failtimeslist = []

# final csv is the simplified csv required containg userid, paswordscheme, number of logins, succesfull logins, and failed logins, also the average time taken for successful and failed logins. Its created using the aforementioned dictionary with individual users

with open('final.csv', 'w') as final_file:
    csv_writer2 = csv.writer(final_file, delimiter=',')
    csv_writer2.writerow(["username","successful logins", "failed logins" , "total logins", "succesful login times", "failed login times", "schema"])
    for key in userslogins:
        dic = userslogins.get(key)
        if len(dic.get('successtimes')) != 0:
            successAvg = statistics.mean(dic.get('successtimes', [0]))
        else:
            successAvg =0
        if len(dic.get('failtimes')) != 0:
            failureAvg = statistics.mean(dic.get('failtimes', [0]))
        else:
            failureAvg =  0;
        csv_writer2.writerow([key,dic.get('success', 0),dic.get('failure', 0),(dic.get('failure', 0)+dic.get('success', 0)), successAvg, failureAvg, dic.get('ImageOrText')])
        dic['successAvg'] = successAvg
        dic['failAvg'] = failureAvg

# this method gives the stats for the asked for schema
def statmanager(passSchema):
    #clears lists of previous schema data
    successlist.clear()
    totallist.clear()
    failurelist.clear()
    totallist.clear()
    successtimeslist.clear()
    failtimeslist.clear()
    #loops through and creates the list necessary for figures
    for key in userslogins:
        dic = userslogins.get(key)
        if dic.get('ImageOrText')==passSchema:
            successlist.append(dic.get('success', 0))
            failurelist.append(dic.get('failure', 0))
            totallist.append(dic.get('failure', 0) + dic.get('success', 0))
            successtimeslist.append(dic.get('successAvg', 0))
            failtimeslist.append(dic.get('failAvg', 0))

    if passSchema == "testtextrandom":
        print("Text Schema Statistics")
    else:
        print("Images Schema Statistics")


    meanSuccess =statistics.mean(successlist)
    medianSuccess = statistics.median(successlist)
    stdevSuccess = statistics.stdev(successlist)

    meanFail = statistics.mean(failurelist)
    medianFail = statistics.median(failurelist)
    stdevFail = statistics.stdev(failurelist)

    meanTotal = statistics.mean(totallist)
    medianTotal = statistics.median(totallist)
    stdevTotal = statistics.stdev(totallist)

    print ("Number of login per user")
    print ("Successful")

    print("mean number:", meanSuccess)
    print("median:", medianSuccess )
    print("standard deviation:", stdevSuccess)

    print ("Failed")
    print("mean:", meanFail)
    print("median number:", medianFail)
    print("standard deviation :", stdevFail)

    print ("Total")
    print("mean:", meanTotal)
    print("median:", medianTotal)
    print("standard deviation :", stdevTotal)

    meanSuccessTime = statistics.mean(successtimeslist)
    medianSuccessTime = statistics.median(successtimeslist)
    stdevSuccessTime = statistics.stdev(successtimeslist)

    meanFailTime = statistics.mean(failtimeslist)
    medianFailTime = statistics.median(failtimeslist)
    stdevFailTime = statistics.stdev(failtimeslist)

    print ("Login time per user")

    print ("Successful")
    print("mean: ", meanSuccessTime)
    print("median: ",medianSuccessTime)
    print("standard deviation: ", stdevSuccessTime)

    print ("Failed")
    print("mean :", meanFailTime)
    print("median:",medianFailTime)
    print("standard deviation:", stdevFailTime)

    return successlist, failurelist, totallist, successtimeslist, failurelist #returns the schema necessary for making the figures

imageSchema = copy.deepcopy(statmanager('testpasstiles'))
textSchema = copy.deepcopy(statmanager('testtextrandom'))

successNumImage = imageSchema[0]
failNumImage = imageSchema[1]
totalNumImage = imageSchema[2]
successTimesImage =  imageSchema[3]
failTimesImage =  imageSchema[4]

successNumText = textSchema[0]
failNumText = textSchema[1]
totalNumText = textSchema[2]
successTimesText =  textSchema[3]
failTimesText =  textSchema[4]

#code below creates histogram and boxpolot using the above variables
num_bins = 5
plt.hist([successNumImage, successNumText], num_bins, label = ['Image', 'Text'])
plt.xlabel('number of Success')
plt.ylabel('How  many participants')
plt.title('Histogram of Successesful Logins')
plt.legend(loc = 'upper right')
plt.show()

num_bins = 5
plt.hist([failNumImage, failNumText], num_bins, label = ['Image', 'Text'])
plt.xlabel('number of Failures')
plt.ylabel('How  many participants got that number')
plt.title('Histogram of Failed Logins')
plt.legend(loc = 'upper right')
plt.show()

num_bins = 5
plt.hist([totalNumImage, totalNumText], num_bins, label = ['Image', 'Text'])
plt.xlabel('total number')
plt.ylabel('number of participants')
plt.title('Histogram of Total logins')
plt.legend(loc = 'upper right')
plt.show()

num_bins = 9
plt.hist([successTimesImage, successTimesText], num_bins, alpha=0.5, label = ['Image', 'Text'])
plt.xlabel('average time (s)')
plt.ylabel('number of participants')
plt.title('Histogram of Success times')
plt.legend(loc = 'upper right')
plt.show()

num_bins = 9
plt.hist([failTimesImage, failTimesText], num_bins, alpha=0.5, label = ['Image', 'Text'])
plt.xlabel('average time (s)')
plt.ylabel('number of participants')
plt.title('Histogram of Fail times')
plt.legend(loc = 'upper right')
plt.show()

plt.boxplot([successTimesImage, successTimesText])
plt.xticks([1,2],['Images', 'Text'])
plt.title('Average Success Times')
plt.ylabel('average time (s)')
plt.xlabel('schema')
plt.show()

plt.boxplot([failTimesImage, failTimesText])
plt.xticks([1,2],['Images', 'Text'])
plt.title('Average Fail Times')
plt.ylabel('average time (s)')
plt.xlabel('schema')
plt.show()




