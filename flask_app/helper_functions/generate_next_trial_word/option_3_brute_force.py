#------------------------------------#
#--- Step 1 Option 3: Brute force ---#
#------------------------------------#

#*** Algorithm steps ***#

#The premise for this algorithm is that we don't know what the actual word is,
#but we can cycle through each remaining word as though it were the actual word,
#and then test all the other remaining words against each "actual word". The
#final word that we select for the next guess is the trial word that performs
#best on average across all the iterations through different "actual words".

#More specifically, the algorithm works using the following steps:
#--- 1.From the list of remaining words, set one word as the temporary "actual word".
#    Note: we will cycle through every possible word as the temporary "actual word".
#--- 2.From the list of remaining words and for the current "actual word", select a
#    trial word. Note: we will cycle through every possible "trial word" for each
#    temporary "actual word"
#--- 3.For the given "trial word" and "actual word", calculate a score. This is done
#    in two different ways:
#---------3a: "brute force simple"
#         In this approach, we compare the trial word against
#         the temporary actual word, and get the usual RAG score i.e.we use the
#         "check_letters_automatically" function that we otherwise use in step 2 of the main "find_word"
#         algorithm. This generates a RAG score for each letter, which we then map to a 
#         numeric score based on some assumptions for the value of each colour (see "ideas
#         for modifications/extensions" below.) The total score for thee current temporary
#         "trial word" and temporary "actual word" pair is the summation across all RAG scores
#         for each letter.
#---------3a: "brute force extended"
#         In this approach, we assume that our trial word is our test word, and
#         we compare it against the temporary "actual word" to get the list of remaining
#         possible words i.e. if our temporary "actual word" were the "actual word", and
#         we used our temporary "trial word" as our "test word", how many words would
#         be left in our list of remaining possible words? The length of this hypothetical
#         list of remaining possible words is the score assigned for the current temporary
#         "trial word" and temporary "actual word" pair.
#--- 4.We loop this calculation across all possible "trial words" for a given temporary 
#    "actual words", and we record all of the scores in a row of a matrix.
#--- 5.We loop all of these calculations across all possible "actual words" i.e. we assume
#    in term that each possible word is the actual word, and calculate all of the possible
#    possible scores. These scores are recorded in successive rows in a matrix.
#--- 6.We calculate the average score for all trial words across all possible "actual words".
#    This attempts to find the "trial word" that scores highest on average across all possible 
#    actual words.
#--- 7.We select the "trial word" that has the highest average score.

#*** Rationale for this algorithm***#

#We do not know the actual word, but we can cycle through all remaining words as though they
#were the actual words, and test all other words against this word. This allows us to more
#robustly check the performance of each trial word across the set of possible actual words,
#which in turn should lead to the selection of a trial word that best reduces the list of possible
#words for the highest number of possible actual words.

#*** Ideas for modifications/extensions ***#

# - In the "simple" version, the numeric scores for RAG scores i.e. red=1,
#   orange=2 and green=3 is a very basic mapping that assumes a green score
#   is more valuable than an orange score, and an orange score is more valuable
#   than a red score. However, this is not backed by evidence - it is an 
#   assumption in the algorithm. If using this approach, it would be better to
#   find an evidence-based approach for these scores, although this is in 
#   part resolved through the "extended" version of the algorithm, which 
#   removes the need for assigning numeric scores to RAG values.
# - At the moment, we use the "average score across all possible actual values"
#   as our metric for measuring the performance of each trial word, but this
#   may not be the optimum metric e.g. it does not incorporate any measure of 
#   range or variation. There might be two trial words with similar average
#   scores, but one has a much higher variation (e.g. variance). Which one should
#   we select? The word with a higher variance is arguably higher risk, which
#   may sometimes be faster, but may sometimes be slower.

#*** Import libraries ***#
import numpy as np
import sys
import copy
from progressbar import progressbar

#Import function from parallel folders
from helper_functions.generate_rag_score import generate_rag_score as stp2
from helper_functions.update_lists import generate_updated_list as stp3
from helper_functions.other_helper_functions.wordle_classes import WordleRound

#Define function
def generate_word_using_brute_force(WordleGameParameters,ThisWordleRound):
        
    #Define numeric score for RAG scores (note: this is only used in the "simple" version)
    red_score=1
    orange_score=2
    green_score=3
    
    #Create matrix for storing scores
    all_numeric_scores=np.zeros([ThisWordleRound.n_words_remaining,ThisWordleRound.n_words_remaining])
    
    #Loop through all remaining words as possible actual words
    #i.e. we assume in turn that each remaining word is the actual word
    #Note we are using progress bar to track here and provide an ETA, especially
    #for the extended version, since the algorithm is very slow!
    if WordleGameParameters.mode=="one_word":
        
        #Run with progress bar when just doing one word
        for i in progressbar(range(ThisWordleRound.n_words_remaining)):
            
            #Get actual word
            actual_word=ThisWordleRound.remaining_words[i]
            
            #Run brute force calculate on specific actual word
            all_numeric_scores=brute_force_main(WordleGameParameters,ThisWordleRound,green_score,orange_score,red_score,all_numeric_scores,i,actual_word)
        
    else:
        
        #Run without progress bar when doing multiple words, as clashes with progress bar elsewhere
        for i in range(ThisWordleRound.n_words_remaining):
            
            #Get actual word
            actual_word=ThisWordleRound.remaining_words[i]
            
            #Run brute force calculate on specific actual word
            all_numeric_scores=brute_force_main(WordleGameParameters,ThisWordleRound,green_score,orange_score,red_score,all_numeric_scores,i,actual_word)
                
    #Get average score for each trial word (column) across all actual words
    all_trial_words_average_scores=all_numeric_scores.mean(0)
    
    #If we are doing the simple brute force approach, we want the highest scoring trial word
    if WordleGameParameters.method=="brute_force_simple":
    
        #Find location of max scoring value
        location=np.argmax(all_trial_words_average_scores)
    
    #If we are using the extended brute force approach, we want the lowest scoring trial word,
    #since we want the trial word that on average produces the shortest list of possible
    #remaining words
    elif WordleGameParameters.method == "brute_force_extended":
        
        #Find min scoring value
        location=np.argmin(all_trial_words_average_scores)
    
    #Find actual word in this location
    ThisWordleRound.trial_word=ThisWordleRound.remaining_words[location]
    
    #Return selected word
    return ThisWordleRound

#**********************************************#
#*** Run main part of brute force algorithm ***#
#**********************************************#
def brute_force_main(WordleGameParameters,ThisWordleRound,green_score,orange_score,red_score,all_numeric_scores,i,actual_word):
    
    #Save previous trial word and rag score in wordle object to restore at end
    #Note: We need to do this to use the check_letters_automatically function on different trial words
    real_trial_word=ThisWordleRound.previous_trial_word
    real_previous_rag_score=ThisWordleRound.previous_rag_score
        
    #Loop through all words as possible test words
    for j in range(ThisWordleRound.n_words_remaining):

        #Get trial word
        trial_word=ThisWordleRound.remaining_words[j]
        
        #Check if trial word and actual word are the same. If so, skip.
        if actual_word!=trial_word:

            #Initialise numeric score as 0
            numeric_score=0

            #Generate rag score for trial word
            ThisWordleRound.previous_trial_word=trial_word
            ThisWordleRound=stp2.check_letters_automatically(ThisWordleRound,actual_word)

            #*** Brute force simple ***#

            #If we are doing the simple brute force approach
            if WordleGameParameters.method=="brute_force_simple":

                #Assign numeric score for each qualitative rag score
                for score in ThisWordleRound.previous_rag_score:
                    if score=="Red":
                        numeric_score+=red_score
                    elif score=="Orange":
                        numeric_score+=orange_score
                    elif score=="Green":
                        numeric_score+=green_score

            #*** Brute force extended ***#

            #If we are using the extended brute force approach
            elif WordleGameParameters.method == "brute_force_extended":

                #Create a copy of key lists and dictionaries so that we don't change values in global version
                ThisWordleRoundTemp=WordleRound(n_previous_guesses=ThisWordleRound.n_previous_guesses,
                                                previous_trial_word=ThisWordleRound.previous_trial_word,
                                                previous_rag_score=ThisWordleRound.previous_rag_score,
                                                n_words_remaining=ThisWordleRound.n_words_remaining,
                                                remaining_words=ThisWordleRound.remaining_words,
                                                remaining_letters=copy.deepcopy(ThisWordleRound.remaining_letters),
                                                round_number=ThisWordleRound.round_number,
                                                trial_word=ThisWordleRound.trial_word)

                #For the given trial word and actual word, get list of remaining words
                ThisWordleRoundTemp=stp3.get_remaining_words(ThisWordleRoundTemp)

                #Get number of remaining words
                numeric_score=ThisWordleRoundTemp.n_words_remaining

            #Save score to matrix
            all_numeric_scores[i,j]=numeric_score
            
    #Restore true previous trial word and rag score in object
    ThisWordleRound.previous_trial_word=real_trial_word
    ThisWordleRound.previous_rag_score=real_previous_rag_score
    
    #Return values
    return all_numeric_scores