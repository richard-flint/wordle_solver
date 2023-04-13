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

def generate_random_trial_word(ThisWordleRound):
    
    #Generate random number in range
    random_number=random.randint(0,ThisWordleRound.n_words_remaining-1)
    
    #Get trial word
    ThisWordleRound.trial_word=ThisWordleRound.remaining_words[random_number]
    
    #Return word
    return ThisWordleRound