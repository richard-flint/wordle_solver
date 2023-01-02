#---------------------#
#--- Check letters ---#
#---------------------#
#This function compares a trial word against the actual word, and returns a
#RAG rating for each letter using the following (standard Wordle) definitions:
#--- "Green"  = trial letter is the same as true letter
#--- "Orange" = trial letter appears at least once in true word, but not in the
#               current position in the trial word
#--- "Red"    = trial letter does not appear in true word

#The function returns a list of words that correspond to five 
#RAG ratings, one for each letter

def check_letters(true_word,trial_word):
    
    #Initialise score list
    true_word_letters=[]
    trial_word_letters=[]
    all_scores=[]
    
    #Get lists of letters
    for i in range(5):
        true_word_letters.append(true_word[i])
        trial_word_letters.append(trial_word[i])
        
    #Get rag score for each letter in trial word
    for i in range(5):
        if trial_word_letters[i]==true_word_letters[i]:
            all_scores.append("Green")
        elif trial_word_letters[i] in true_word_letters:
            all_scores.append("Orange")
        else:
            all_scores.append("Red")
            
    #Return final value
    return all_scores