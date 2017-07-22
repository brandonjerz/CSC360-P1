#Big Group In The Back
#Brandon Jerz
#CSC 360
#Project1 Machile Learning with sentiment Analysis


import test
import sys
running = True 
while(running):
      debateNumber = 1
      debateURL = ""
      candidateName = ""
      query = ""
      x = ""
      y = ""
      answered = True
      incorrect = True

      participantList = []
      moderatorList = []
      wordList = []
      wordCount = 0


      print("Hello, please select one of the following debates by number:")
      print("1. Republican Candidate Debate ")
      print("2. Democratic Candidate Debate ")
      print("3. Vice Presidential Debate ")
      print("4. Presidential Debate Nevada ")
      print("5. Presidential Debate Missouri")

      while(incorrect):
            while True: 
                  try:
                        debateNumber = int(raw_input("Please enter a number 1-5: "))
                        print("Processing.....")
                        break
                  except ValueError:
                        print("Error: Please only use integers")                 
            if debateNumber == 1:
                  incorrect = False
                  debateURL = "http://www.presidency.ucsb.edu/ws/index.php?pid=111711"     
            elif debateNumber == 2:
                  incorrect = False
                  debateURL = "http://www.presidency.ucsb.edu/ws/index.php?pid=111178"
            elif debateNumber == 3:
                  incorrect = False
                  debateURL = "http://www.presidency.ucsb.edu/ws/index.php?pid=119012"
            elif debateNumber == 4:
                  incorrect = False
                  debateURL = "http://www.presidency.ucsb.edu/ws/index.php?pid=119039"
            elif debateNumber == 5:
                  incorrect = False
                  debateURL = "http://www.presidency.ucsb.edu/ws/index.php?pid=119038"
            else:
                  print("Incorrect Entry, Enter a Number 1-5")
            
      sentences = test.tokenize_url(debateURL)
      participantList = test.getParticipants(debateURL)
      moderatorList = test.getModerators(debateURL)
      tokens = test.cleanHTML(debateURL)
      participantWords = test.getCount(tokens,participantList,moderatorList)
      wordCount = len(participantWords)     
      cData = test.getCandidateSentiment(sentences,participantList,moderatorList)     
      print "You've chosen debate number: %d" %(debateNumber)
      print("Please choose one of the following inquirys")
      print("1.  Who are the debate participants?")
      print("2.  Who are the debate monitors?")
      print("3.  How many words were spoken by the candidates as a group")
      print("4.  How many words were spoken by each of the candidates?")
      print("5.  What did X say about Y?")
      print("6.  What were each candidates 10 most said words (4 letters or more)")
      print("7.  Which candidate used the most negative language")
      print("8.  Which candidate used the most neutral language")
      print("9.  Which candidate used the most positive language")
      print("10. Which candidate had the highest compund score (average of all 3)")
      print("11. All sentiment analysis")
      incorrect = True
      while(incorrect):
            while True:
                  try:
                        choiceNumber = int(raw_input("Please enter a number 1-11: "))
                        break
                  except ValueError:
                        print("\nPlease only use integers") 


            if choiceNumber == 1:
                  #INSERT CODE THAT NAMES EACH PARTICIPANT
                  incorrect = False
                  for p in participantList:
                    print p
                    
            if choiceNumber == 2:
                  #INSERT CODE THAT NAMES EACH MODERATOR
                  incorrect = False
                  for m in moderatorList:
                    print m
            if choiceNumber == 3:
                  #INSERT CODE THAT COUNTS THE NUMBER OF WORDS SPOKEN BY ALL
                  #CANDIDATES TOGETHER
                  incorrect = False
                  print "There were %d words said by the Candidates" % (wordCount)

            if choiceNumber == 4:
                  #INSERT CODE THAT SHOWS NUMBER OF WORDS
                  #SPOKEN BY EACH OF THE CANDIDATES GIVE COUNT AND
                  #PERCENTAGE
                  incorrect = False
                  test.getCandidateCount(wordCount,tokens,participantList,moderatorList)
            if choiceNumber == 5:
                  incorrect = False
                  x = raw_input("Enter an X: ")
                  y = raw_input("Enter a Y: ")
                  test.getConcordance(x.upper(),y,tokens,participantList,moderatorList)
            if choiceNumber == 6:
                  incorrect = False
                  test.getCandidateTop10Words(tokens,participantList,moderatorList)
            if choiceNumber == 7:
                  incorrect = False
                  person = ""
                  greatest = -12
                  for p in participantList:
                  		if(cData["CRUZ"]["neg"] > greatest):
                  				greatest = cData[p]["neg"]
                  				person = p
                  print("%s had the greatest negative score with a score of %f therefore he/she had the most negative language"%(person,greatest))
            if choiceNumber == 8:
                  incorrect = False
                  person = ""
                  greatest = -12
                  for p in participantList:
                  		if(cData[p]["neu"] > greatest):
                  				greatest = cData[p]["neu"]
                  				person = p
                  print("%s had the greatest neutral score with a score of %f therefore he/she had the most neutral language"%(person,greatest))
            if choiceNumber == 9:
                  incorrect = False
                  person = ""
                  greatest = -12
                  for p in participantList:
                  		if(cData[p]["neu"] > greatest):
                  				greatest = cData[p]["pos"]
                  				person = p
                  print("%s had the greatest positive score with a score of %f therefore he/she had the most positive language"%(person,greatest))
            if choiceNumber == 10:
                  incorrect = False
                  person = ""
                  greatest = -12
                  for p in participantList:
                  		if(cData[p]["neu"] > greatest):
                  				greatest = cData[p]["compound"]
                  				person = p
                  print("%s had the greatest compound score with a score of %f therefore he/she had the most compound language"%(person,greatest))
                  
                  
            if choiceNumber == 11:
            		incorrect = False
            		for p in participantList:
            			print("")
            			print("Data for %s")%p
            			print("-----------")
            			print("Total Negative Score: %f")%cData[p]["neg"]
            			print("Total Neutral Score: %f")%cData[p]["neu"]
            			print("Total Positive Score: %f")%cData[p]["pos"]
            			print("Total Average Compound Score: %f")%cData[p]["compound"]
            			print("-----------")
            			print("")
            			
            			
      finalDecision = int(raw_input("Enter 0 to exit or 1 to select a new debate: "))
      if finalDecision == 0:
            #EXIT PROGRAM
            incorrect = False
            print("Goodbye!")
            running = False
