#---------------------------------------------------#
#--- Step 1 Option 1: Generate random trial word ---#
#---------------------------------------------------#

#*** Algorithm steps ***#
#This function generates a random next guess from the list of possible words.

#*** Rationale for this algorithm***#
#This is perhaps the simplest method for selecting the next word, and is useful
#as an initial basic implementation and benchmark for other more sophisticated
#algorithms.


#Import libraries
import random

def generate_random_trial_word(all_words_remaining):
    
    #Get number of words
    n_words=len(all_words_remaining)
    
    #Generate random number in range
    random_number=random.randint(0,n_words-1)
    
    #Get trial word
    trial_word=all_words_remaining[random_number]
    
    #Return word
    return trial_word