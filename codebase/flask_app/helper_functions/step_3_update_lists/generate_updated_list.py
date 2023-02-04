#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#----------- Functions for "Step 3: Generate updated list of remaining possible words" -----------#
#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#This collection of functions generates an updated list of possible words based on the comparison
#between the trial word and actual word carried out in Step 2. The functions use the output of 
#Step 2 (i.e. a list of 5 words that correspond to RAG ratings e.g. either "green","orange" or
#"red"), and based on this information, systematically removes words from the list of remaining
#possible words

#*** Algorithm steps ***#

#These function generates the next guess through the following algorithm:
#--- 1.Cycle through the RAG rating for each letter.
#--- 2.If RAG score is "Green", reduce the list of possible letters for
#    that column down to 1 letter i.e. the corresponding letter in the
#    trial word.
#--- 3.If RAG score is "Orange", find all other columns where the corresponding
#    letter in the trial word could possibly appear in the actual word. This
#    information is stored in a dictionary called "orange_letters", which is then
#    used in subsequent functions to systematically remove words from the list of remaining
#    possible words. This is by far the most complicated section of this algorithm,
#    since a lot of information is contained in an "Orange" score, but is it is 
#    more complex to extract and apply all of this information.
#--- 3.If RAG score is "Red", remove this letter from all lists of possible letters.
#--- 4.Based on the updated list of possible letters for each column, remove words
#    from the list of possible words that are no longer possible solutions

#*** Rationale for this algorithm***#

#The RAG scores contain a lot of information about the position of possible letters,
#which can then be used to systematically reduce down the number of possible words, which
#in turn means the next guess is from an increasingly small list of words. The allows the
#algorithm to reduce the list of possible words in an effective manner until only one
#possible word is left - the actual word.

#*** Ideas for modifications/extensions ***#
# - We currently use the list of possible letters to further reduce down the orange letters
#   dictionary, and we use both the list of possible letters and the orange letters dictionary
#   to reduce the list of possible words, but we dont use the orange letters list to reduce
#   down the list of possible letters. This could be used to further eliminate words from the
#   list of possible words e.g. if there is perfect orange letter pair, whereby one letter
#   can only occur in two positions, and a second (different) letter can only occur in two positions,
#   and both sets of positions are the same, then we know that in those two positions, the list
#   of possible letters is only 2 in length i.e. the two letters with matching possible positions.
#   This is similar to common moves in sudoku, and can be further extended e.g. to three positions that have
#   perfectly overlapping possible positions across three pairs of possible positions.

#Imports
import copy

#---------------------------#
#--- Get remaining words ---#
#---------------------------#
#This function takes 1) the list of possible letters in each word, and 2) the dictionary of orange
#letters and their positions, and creates an updated list of possible words

def get_remaining_words(all_words_remaining,all_possible_letters_remaining,rag_score,trial_word):
    
    #Get possible letters for each column
    all_possible_letters_remaining,min_max_occurences=get_possible_letters(all_possible_letters_remaining,rag_score,trial_word)
    
    #Create copy of all_words list so we can delete words
    #without affecting loop that includes all_words_remaining
    all_words_remaining_updated=all_words_remaining.copy()
    
    #Cycle through all words in list of remaining possible words
    for word in all_words_remaining:
        
        #Initialise delete word flag with inital value of FALSE, which by default does not remove a word
        delete_word_flag=False
        
        #*** Check each letter in each word is in list of possible letters for corresponding column ***#
        
        #Cycle through all 5 letters in each word
        for i in range(5):
            
            #Get test letter
            test_letter=word[i]
            
            #Get column name for "all_possible_letters_remaining" dictionary
            column_name=list(all_possible_letters_remaining.keys())[i]
            
            #Get list of possible letters for given column
            possible_letters_one_column=all_possible_letters_remaining[column_name]
            
            #Check if test letter is in list of possible letters for column
            check = test_letter in possible_letters_one_column
            
            #If test letter is not in list of possible letters, set delete word 
            #(note: strictly speaking, we just set the flag here, and the word is deleted lower down.
            #       we use the same approach lower down too.)
            if check == False:
                delete_word_flag=True
                
        #*** Check word fulfills max min occurences criteria ***#
        
        #For each letter in the max min occurences dictionary
        for specific_letter in min_max_occurences.keys():
            
            #Count number of  occurences of specific letter in word
            n_occurences=word.count(specific_letter)
            
            #Check if n_occurences is between maximum and minimum value
            min_possible_occurences=min_max_occurences[specific_letter][0]
            max_possible_occurences=min_max_occurences[specific_letter][1]
            if (n_occurences<min_possible_occurences) or (n_occurences>max_possible_occurences):
                
                #If not, set delete word flag
                delete_word_flag=True
                
        #*** Delete word ***#
                
        #If delete word flag is now set to true, delete word from list         
        if delete_word_flag==True:
            all_words_remaining_updated.remove(word)
    
    #**************#
    #*** Return ***#
    #**************#
    
    #Return remaining lists after looping through all words
    return all_words_remaining_updated,all_possible_letters_remaining

#----------------------------#
#--- Get possible letters ---#
#----------------------------#
#This function generates two things based on the RAG score for the selected trial word :
# 1) an updated dictionary of possible letters for each column ("all_possible_letters")
# 2) an updated dictionary of letters and their possible positions in the true word ("orange_letters")

def get_possible_letters(all_possible_letters_remaining,rag_score,trial_word):
    
    #Initialise dictionary for storing "orange" letters
    orange_letters=[]
    
    #Initialise dictionary for storing minimum and maximum possible occurences of certain "orange" letters
    min_max_occurences=dict()
    
    #*******************#        
    #*** Check green ***#
    #*******************#
    
    #Initialise i for counting
    i=0
    
    #Loop through columns 1 to 5
    for column in all_possible_letters_remaining.keys():
        
        #Get specific letter and specific rag_score in trial word
        specific_letter=trial_word[i]
        specific_score=rag_score[i]
        
        #If column score is green
        if specific_score=="Green":
            
            #Set the column in "all_possible_letters_remaining" to one letter i.e. the specific letter
            all_possible_letters_remaining[column]=specific_letter
            
        #Increment i
        i+=1
    
    #*****************#
    #*** Check red ***#
    #*****************#
    
    #Initialise i for counting
    i=0
    
    #Loop through columns 1 to 5
    for column in all_possible_letters_remaining.keys():
        
        #Get specific letter and specific rag_score in trial word
        specific_letter=trial_word[i]
        specific_score=rag_score[i]
        
        #If column score is red
        if specific_score=="Red":
            
            #Count how many times specific letter appears in word
            n_occurences=trial_word.count(specific_letter)
            
            #If it appears only once, then we can be sure that it is not in the true word
            if n_occurences==1:
                
                #And so we can remove it from all_possible_letters_remaining
                #Note we use "col" here to avoid overwriting the "column" variable in the wider loop
                for col in all_possible_letters_remaining.keys():
                    if specific_letter in all_possible_letters_remaining[col]:
                        all_possible_letters_remaining[col].remove(specific_letter)
                    
            #If letter appears more than once, we need to check if it's orange elsewhere
            elif n_occurences>1:
                
                #Initialise variables
                other_rag_scores=[]
                
                #Get RAG scores for other occurences
                trial_word_as_list=[*trial_word]           #Copy trial word into list
                trial_word_as_list[i]=""                   #Remove letter from current position
                
                #Loop through other letters
                for ind in range(len(trial_word_as_list)):
                    if trial_word_as_list[ind]==specific_letter:
                        other_rag_scores.append(rag_score[ind])
                        
                #If none of the other rag scores are orange, we can remove the letter from everywhere
                #Note we use "col" here to avoid overwriting the "column" variable in the wider loop
                if "Orange" not in other_rag_scores:
                    for col in all_possible_letters_remaining.keys():
                        if specific_letter in all_possible_letters_remaining[col]:
                            if len(all_possible_letters_remaining[col])>1:         #If len=1, then it means it's a green, so don't remove
                                all_possible_letters_remaining[col].remove(specific_letter)
                            
                #If one or more of the other rag scores are orange, then we can only remove it from its current position
                elif "Orange" in other_rag_scores:
                    if specific_letter in all_possible_letters_remaining[column]:
                        all_possible_letters_remaining[column].remove(specific_letter)
            
        #Increment i
        i+=1
        
    #********************#
    #*** Check orange ***#
    #********************#
    
    #Initialise i for counting
    i=0
    
    #Loop through columns 1 to 5
    for column in all_possible_letters_remaining.keys():
        
        #Get specific letter and specific rag_score in trial word
        specific_letter=trial_word[i]
        specific_score=rag_score[i]
        
        #If column score is orange
        if specific_score=="Orange":
            
            #Remove letter from current position
            if specific_letter in all_possible_letters_remaining[column]:
                all_possible_letters_remaining[column].remove(specific_letter)
                
            #The number of red, oranges and greens also gives information on the min and max number of
            #possible occurences of a letter in a word. We calculate this in the next section.
            
            #We only need to do this once for each letter
            if specific_letter not in orange_letters:
            
                #Record that letter is orange (including duplication)
                orange_letters.append(specific_letter)

                #Generate copy of trial word
                trial_word_as_list=[*trial_word]           #Copy trial word into list
                trial_word_as_list[i]=""                   #Remove letter from current position

                #Loop through trial word, and get rag score for same specific letter
                other_rag_scores=[]
                for ind in range(len(trial_word_as_list)):
                    if trial_word_as_list[ind]==specific_letter:
                        other_rag_scores.append(rag_score[ind])

                #Count number of greens, reds and oranges in other rag scores
                n_greens=other_rag_scores.count("Green")
                n_oranges=other_rag_scores.count("Orange")
                n_reds=other_rag_scores.count("Red")

                #Get minimum and maximum occurences of letter in word
                #Note, this information is useful as it can help remove additional words from the available list

                #The minimum possible number of occurences is given by 1 (for the fact that there's at least one
                #occruance for the orange in the current position) + the number of orange elsewhere for the 
                #same letter + the number of greens elsewhere for the same letter
                min_occurences=1+n_oranges+n_greens

                #The maximum number of occurences depends whether there is the same letter with a red score
                if n_reds!=0:
                    #If yes, then we know the max number of occurences is equal to the min number of occurences
                    max_occurences=min_occurences
                else:
                    #If not, we don't know what the top end is, so set to 5
                    max_occurences=5

                #Save min and max occurences data
                min_max_occurences[specific_letter]=[min_occurences,max_occurences]
            
            #But we still want to record duplicates for lower down
            else:
                
                #Record that letter is orange (including duplication)
                orange_letters.append(specific_letter)

        #Iterate up
        i+=1
        
    #********************************************************************#
    #*** Check if any orange letters have only one available position ***#
    #********************************************************************#
    #After the above analysis, some orange letters may only have one available position
    #If so, we want to collapse those positions down to one letter
    
    #Create list to keep track of orange letters that have been processed
    orange_letters_done=[]
        
    #Loop across all orange letters 
    for specific_letter in orange_letters:
        
        #Check specific letter hasnt been processed yet
        if specific_letter not in orange_letters_done:
            
            #Record that we are processing this letter
            orange_letters_done.append(specific_letter)
        
            #Count number of times the letter appears as orange
            n_orange=orange_letters.count(specific_letter)

            #Find number of occurences of letter in columns of remaining possible letters...
            n_occurences=0
            position=[]
            rag_score_temp=[]
            i=0

            #...by serching through all columns
            for col in all_possible_letters_remaining.keys():

                #...and checking if letter is in column and column is not "Green"
                if (specific_letter in all_possible_letters_remaining[col]) and (rag_score[i]!="Green"):
                    n_occurences+=1    #...save occurence
                    position.append(i) #...and save position

                #Increment position count
                i+=1

            #If the number of occurences (i.e. number of possible columns where the letter could be) is equal to
            #the number of oranges in the RAG score, then we know each of the possible positions must be this letter
            if n_occurences==n_orange:

                i=0
                for col in all_possible_letters_remaining.keys():
                    if i in position:
                        all_possible_letters_remaining[col]=specific_letter
                    i+=1
    
    #*********************#
    #*** Return values ***#
    #*********************#
    
    #Return list of remaining letters
    return all_possible_letters_remaining, min_max_occurences