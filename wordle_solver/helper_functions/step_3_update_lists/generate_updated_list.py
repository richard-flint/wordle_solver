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
    all_possible_letters_remaining,orange_letters=get_possible_letters(all_possible_letters_remaining,rag_score,trial_word)
    
    #Create copy of all_words list so we can delete words
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
        
        #*** Check word fulfills criteria associated with orange letters ***#
        
        #For each letter in the orange letter list
        for specific_orange_letter in orange_letters.keys():
            
            #Check if orange letter is in word. If not, then delete word
            if specific_orange_letter not in word:
                delete_word_flag=True
            
            #Check if orange letter is in at least one of the correct columns...
            
            #...by first getting the list of possible columns for a specific orange letter
            possible_columns=orange_letters[specific_orange_letter]
            actual_columns=[]
            
            #...and find the columns for all occuranges of that letter in the test word
            for i in range(5):
                if word[i]==specific_orange_letter:
                    actual_columns.append(i)
            
            #...and check that these occurances match the possible positions of orange letters
            for i in range(len(actual_columns)):
                
                #If the actual position is not one of the possible positions, delete word
                if actual_columns[i] not in possible_columns:
                    delete_word_flag=True

        #If delete word flat is now set to true, delete word from list         
        if delete_word_flag==True:
            all_words_remaining_updated.remove(word)
        
    #Return remaining lists after looping through all words
    return all_words_remaining_updated,all_possible_letters_remaining

#----------------------------#
#--- Get possible letters ---#
#----------------------------#
#This function generates two things based on the RAG score for the selected trial word :
# 1) an updated dictionary of possible letters for each column ("all_possible_letters")
# 2) an updated dictionary of letters and their possible positions in the true word ("orange_letters")

def get_possible_letters(all_possible_letters,score,trial_word):
    
    #Initialise i
    i=0
    
    #Initialise dictionary for storing "orange" letters
    orange_letters=dict()
    
    #Get list of column numbers that are either red or orange (this is for the "if orange" condition)
    red_or_orange_columns=[]
    for j in range(5):
        if (score[j] == "Red" or score[j] == "Orange"):
            red_or_orange_columns.append(j)
    
    #Loop through columns 1 to 5
    for column in all_possible_letters.keys():
        
        #Get specific letter and specific score in trial word
        specific_letter=trial_word[i]
        specific_score=score[i]
        
        #If column score is green
        if specific_score=="Green":
            
            #Set the column in "all_possible_letters" to one letter i.e. the specific letter
            all_possible_letters[column]=specific_letter
            
        #If column score is orange
        elif specific_score=="Orange":
            
            #Remove letter from list of possible letters for that position, since an orange score indicates
            #that the specific letter is not correct for that specific position
            all_possible_letters[column].remove(specific_letter)
            
            #Check if this letter has previously appeared as an "orange" (i.e. in an earlier letter in the
            #trial word)
            #Note: we are working through the test word sequentially, and the same letter may appear two
            #or more times as an orange letter. If this is the case, the analysis of the first orange letter
            #is sufficient, so we skip the second (or higher) occurances
            if specific_letter not in orange_letters.keys():
                
                #If the letter has not previously appeared in trial word as orange, then find the list
                #of possible positions in true word, and record this in the "orange_letters" dictionary
                orange_letters=add_letter_to_orange_letters(trial_word,
                                                            specific_letter,
                                                            orange_letters,
                                                            red_or_orange_columns,
                                                            i,
                                                            score)
            
        #If red, remove letter from all columns in "all_possible_letters"
        elif specific_score=="Red":
            for column2 in all_possible_letters.keys():
                if specific_letter in all_possible_letters[column2]:
                    all_possible_letters[column2].remove(specific_letter)
        
        #Iterate up
        i+=1
        
    #--- Cross check orange letters list with possible letters list ---#
    #We now have a list of possible letters for each column, and a dictionary of orange letters with
    #columns where these letters may appear in the true word. However, some of columns that are listed for
    #specific letters in the "orange letters" dictionary may have already been ruled out by previous rounds
    #in the solver, and so we cross-check the two lists to remove any positions in the orange_letters list
    #that have already been ruled out. We could also use the orange letters dictionary to further reduce
    #the possible letters list, but this has not been implemented yet.
    all_possible_letters,orange_letters=cross_check_orange_letters(all_possible_letters,orange_letters)
                
    #Return list of remaining letters
    return all_possible_letters, orange_letters

#------------------------------------#
#--- Add letter to orange letters ---#
#------------------------------------#
#The "orange_letters" dictionary is a dictionary where the keys are specific letters that are identified
#as "orange" for the given trial word, and the values are a list of numbers that correspond to the columns
#where the letter could possibly be. This function finds the values for a specific key, and adds it to the
#dictionary.

def add_letter_to_orange_letters(trial_word,specific_letter,orange_letters,red_or_orange_columns,i,score):
    
    #For the specific orange letter, record that it is a possible option for all columns that are either
    #red or orange, but not for columns that are green, since those columns are already decided
    orange_letters[specific_letter]=red_or_orange_columns.copy()

    #Remove the current column from the list, as we know that the specific letter is not correct
    #for the current column (otherwise it would be green...!)
    orange_letters[specific_letter].remove(i)

    #Check if the specific orange letter appears more than once in the trial word
    if trial_word.count(specific_letter)>1:

        #If the specific letter does appear more than once, find the colours and locations
        #of the specific orange letter elsewhere in the word
        locations_of_repeated_letters=[]
        colours_of_repeat_letters=[]

        #Iterate through all letters in trial word
        for k in range(5):

            #Get letter in trial word
            letter_in_trial_word=trial_word[k]

            #Check if letter in trial word is same as specific orange letter, and that the column is not same as
            #current column for the specific orange letter
            if (letter_in_trial_word==specific_letter and i!=k):
                locations_of_repeated_letters.append(k)
                colours_of_repeat_letters.append(score[k])

        #If there is one or more repeated letter that is "Green"
        if "Green" in colours_of_repeat_letters:
            #Remove letter from orange letters dictionary, since the "Orange" in the current column is covered
            #by the "Green" in the repeated column
            orange_letters.pop(specific_letter) 

        #If there is one or more repeated letters that is "Orange" or "Red"
        elif ("Orange" in colours_of_repeat_letters or "Red" in colours_of_repeat_letters):

            #Loop through repeated letters, and remove any locations from "orange_letters" list
            #where the repeated letters are either "Orange" or "Red". Note: technically we should
            #not need to do this for "Red", since the same letter should not appear as "Orange" and
            #"Red" in the same set of scores, but included here for completeness/additional security.
            count=0
            for colour in colours_of_repeat_letters:
                if (colour == "Orange" or colour == "Red"):

                    #Get column number to remove from "orange_letters" list
                    column_to_remove=locations_of_repeated_letters[count]

                    #Remove column number from "orange_letters" list
                    orange_letters[specific_letter].remove(column_to_remove)

                #Add one to count
                count+=1
                
    #Return orange letters dictionary
    return orange_letters

#----------------------------------#
#--- Cross check orange letters ---#
#----------------------------------#
#We now have a list of possible letters for each column, and a dictionary of orange letters with
#columns where these letters may appear in the true word. However, some of columns for the orange letters
#may have already been ruled out by previous rounds in the solver, and so we cross-check the two lists
#to remove any positions in the orange_letters list that have already been ruled out.

def cross_check_orange_letters(all_possible_letters,orange_letters):

    #Check if any of the orange letters have been removed from "all_possible_letters"
    for letter in orange_letters.keys():
        
        #Get columns associate with specific letter
        columns=orange_letters[letter]
        
        #Loop across all columns to check
        for column_number in columns:
            
            #Get column name for "all_possible_letters" column
            column_name="column_"+str(column_number)
            
            #Check if orange letter is in possible letters for column
            if letter not in all_possible_letters[column_name]:
                
                #If orange letter is not in possible letters for column, then delete from orange letters
                orange_letters[letter].remove(column_number)
                
    #If any of the orange letters now only have one possible column, then set 
    #that column in "all_possible_letters"
    for letter in orange_letters.keys():
        if len(orange_letters[letter])==1:
            column_number=orange_letters[letter][0]
            column_name="column_"+str(column_number)
            all_possible_letters[column_name]=letter
            
    #Return updated
    return all_possible_letters,orange_letters