#Big Group In The Back
#Brandon Jerz
#CSC 360
#Project1 Machile Learning with sentiment Analysis

import os
import bs4
from bs4 import BeautifulSoup
import re,pprint,nltk,bs4
from urllib import urlopen
from nltk.tokenize import PunktSentenceTokenizer
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#Republican Candidate Debate: http://www.presidency.ucsb.edu/ws/index.php?pid=111711
#Democratic Candidate Debate: http://www.presidency.ucsb.edu/ws/index.php?pid=111178
#Vice Presidential Debate: http://www.presidency.ucsb.edu/ws/index.php?pid=119012
#Presidential Debate Nevada: http://www.presidency.ucsb.edu/ws/index.php?pid=119039
#Presidential Debate Missouri: http://www.presidency.ucsb.edu/ws/index.php?pid=119038



def cleanHTML(url):
	raw = urlopen(url).read()
	startIndex = raw.find("PARTICIPANTS")
	endIndex = raw.find("Citation:")
	raw = raw[startIndex:endIndex]
	soup = BeautifulSoup(raw,"lxml").getText()
	soup = soup.replace("?", " ")
	soup = soup.replace(".", " ")
	soup = soup.replace("!", " ")
	soup = soup.replace(":", " ")
	soup = soup.replace("-", " ")
	soup = soup.replace("'", "")
	soup = soup.replace("\"", " ")
	soup = soup.replace(","," ")
	soup = soup.replace(" - ", "")
	tokens = nltk.word_tokenize(soup)
	#print tokens
	switch = 0
	tokenlist = []
	for tok in tokens:
		tokenlist.append(tok)
	return tokenlist



def tokenize_url(url):
        raw = urlopen(url).read()
        startIndex = raw.find("PARTICIPANTS")
        endIndex = raw.find("Citation:")
        raw = raw[startIndex:endIndex]
        soup = BeautifulSoup(raw,"lxml").getText()
        soup = soup.replace("!", "! ")
	soup = soup.replace(":", " ")
	soup = soup.replace(".", ". ")
	soup = soup.replace("-", " ")
	soup = soup.replace("'", "")
	soup = soup.replace("\"", " ")
	soup = soup.replace(",",", ")
	soup = soup.replace(" - ", "")
	soup = soup.replace("?", "? ")
	soup = soup.replace(".  ", ". ")
	soup = soup.replace("?  ", "? ")
	soup = soup.replace("Mr. ","Mr.")
	soup = soup.replace("Mr.Trump","")
        tokenizer = PunktSentenceTokenizer(soup)
        tokenized = tokenizer.tokenize(soup)
        return tokenized


def getCandidateSentiment(sentences, candidates, moderators):
        sid = SentimentIntensityAnalyzer()
        send = False
        sentList = []
        sentValue = 0
        candidateData = {}
        for person in candidates:
            neg = 0
            neu = 0
            pos = 0
            compound = 0
            sentList = []
            sentValue = 0
            for t in sentences:
                    if checkForPerson(t,person):
                        send = True
                    elif checkForPerson2(t,moderators):
                            if checkForPerson2(t,candidates):
                                if send == True:
                                    sentList.append(t)
                            else:
                                    send = False
             
            for sentence in sentList:
                    ss = sid.polarity_scores(sentence)
                    neg = neg + ss["neg"]
                    neu = neu + ss["neu"]
                    pos = pos + ss["pos"]
                    compound = compound + ss["compound"]
            avgNeg = ss["neg"]/len(sentList)
            avgNeu = ss["neu"]/len(sentList)
            avgPos = ss["pos"]/len(sentList)
            avgCompound = ss["compound"]/len(sentList)

            candidateData[person] = {"neg" : neg,
                                       "neu" : neu,
                                       "pos" : pos,
                                       "compound" : compound,
                                       "avgNeg" : avgNeg,
                                       "avgNeu" : avgNeu,
                                       "avgPos" : avgPos,
                                       "avgCompound" : avgCompound
                                      }
        return candidateData

def checkForPerson(sentence,person):
    words = nltk.word_tokenize(sentence)
    for word in words:
        if person == word:
                return True
    return False
    

def checkForPerson2(sentence,people):
    words = nltk.word_tokenize(sentence)
    for p in people:

            for word in words:
                    if word == p:
                            #print(p)
                            #print(word)
                            return False
    return True

def getCount(tokens, candidates, moderators):
        send = False
        wordList = []
        for person in candidates:
            for t in tokens:
                if person in t:
                    send = True
                elif t not in moderators:
                    if t not in candidates:
                        if send == True:
                            wordList.append(t)
                else:
                    send = False
        return wordList

#Counts the number of words spoken by each candidate
def getCandidateCount(wordCount, tokens, candidates, moderators):
        send = False
        wordList = []
        for person in candidates:
                wordList = []
                for t in tokens:
                        if person in t:
                                send = True
                        elif t not in moderators:
                                if t not in candidates:
                                        if send == True:
                                            wordList.append(t)
                        else:
                                send = False
                wordPercent = float(len(wordList))/float(wordCount) * 100
                print "%s said %d words which is %f percentage of total words "%(person,len(wordList),wordPercent)

                


#Prints out each candidates top 10 words greater than 4 letters
def getCandidateTop10Words(tokens, candidates, moderators):
        send = False
        wordList = []
        for person in candidates:
                wordList = []
                wordCounter = {}
                for t in tokens:
                        if person in t:
                                send = True
                        elif t not in moderators:
                                if t not in candidates:
                                        if send == True:
                                            wordList.append(t)
                        else:
                                send = False
                for word in wordList:
                        if word in wordCounter:
                                if len(word)>4:
                                        wordCounter[word] += 1
                        else:
                                if len(word)>4:
                                        wordCounter[word] = 1
                        popularwords = sorted(wordCounter, key = wordCounter.get, reverse = True)
                        top10 = popularwords[:10]
                        
                print "%s Top 10 words are  "%(person)
                print "----------------"
                for x in top10:
                        print x
                print"-----------------"




#Gets Concordance
def getConcordance(x,y,tokens, candidates, moderators):
        send = False
        wordList = []
        for t in tokens:
        	if x in t:
                        send = True
                elif t not in moderators:
                        if t not in candidates:
                                if send == True:
                                        wordList.append(t)
                else:
                        send = False
        candidateText = nltk.Text(wordList)
        candidateText.concordance(y)


#Get Participants from URL
def getParticipants(url):
	raw = urlopen(url).read()
	startIndex = raw.find("PARTICIPANTS")
	endIndex = raw.find("citation")
	raw = raw[startIndex:endIndex]
	soup = BeautifulSoup(raw,"lxml")
	CandidateList = []
	#soup = soup.getText()
	ptags = soup.findAll("p")
	#tokens = nltk.word_tokenize(soup)
	switch = 0
	for tag in ptags:
		if "PARTICIPANTS" in tag.getText():
			participantTag = tag.getText()
			participantTag = participantTag.replace("PARTICIPANTS:","")
			#participantTag = participantTag.replace(") ","); ")
			participantTag = participantTag.replace(");","|")
			participantTag = participantTag.replace(")","|")
			participantTag = participantTag.replace(";","|")
			participantTag = participantTag.replace("'","")
			
			participantTag = participantTag.strip()
			titlelist = ["Businessman","Senator","Governor","Mayor","Former", "Secretary of State"," and"]
			
			for x in titlelist:
				participantTag = participantTag.replace(x,"")
			pArray = participantTag.split("|")
			if pArray[-1] =="":
				del pArray[-1]
			for thing in pArray:
					thing = thing.strip()
					nameArray = thing.split(" ")
					CandidateList.append(nameArray[1].upper())
	return CandidateList		    
	
#Get Moderators from URL
def getModerators(url):
	raw = urlopen(url).read()
	startIndex = raw.find("PARTICIPANTS")
	endIndex = raw.find("citation")
	raw = raw[startIndex:endIndex]
	soup = BeautifulSoup(raw,"lxml")
	ModeratorList = []
	#soup = soup.getText()
	ptags = soup.findAll("p")
	#tokens = nltk.word_tokenize(soup)
	
	for tag in ptags:
		if "MODERATOR" in tag.getText():
			moderatorTag = tag.getText()
			moderatorTag = moderatorTag.replace("MODERATOR:","")
			moderatorTag = moderatorTag.replace(");","|")
			moderatorTag = moderatorTag.replace(")","|")
			moderatorTag = moderatorTag.replace(";","|")
			moderatorTag = moderatorTag.strip()
			titlelist = ["Senator","Governor","Mayor"," and "]
			
			for x in titlelist:
				moderatorTag = moderatorTag.replace(x,"")
			
			mArray = moderatorTag.split("|")
			if mArray[-1] =="":
				del mArray[-1]
			for thing in mArray:
					thing = thing.strip()
					nameArray = thing.split(" ")
					ModeratorList.append(nameArray[1].upper())
	return ModeratorList



	
			

	

'''
def getIndividualCount(name):
	raw = urlopen(url).read()
	startIndex = raw.find("PARTICIPANTS")
	endIndex = raw.find("citation")
	raw = raw[startIndex:endIndex]
	soup = BeautifulSoup(raw,"lxml")
'''
	 
