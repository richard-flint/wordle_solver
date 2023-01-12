#-------------------------------------#
#--- Import packages and functions ---#
#-------------------------------------#

#Add parent folder to directory so that we can reference files and functions elsewhere in folder structure
import sys 
sys.path.append('..')

#Import functions elsewhere
from helper_functions.step_1_generate_next_trial_word import overall_generate_next_trial_word as stp1_0
from helper_functions.step_3_update_lists import generate_updated_list as stp3

#Run wordle solver for flask app
def run_wordle_solver_flask(mode,next_word_selection,rag_colours,trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining):

    #For anything other than the first run, we first need to generate an updated list of possible words based on the previous trial word and the rag score
    if rag_colours!=None:
    
        #---------------------------------------------------------#
        #--- Generate updated list of remaining possible words ---#
        #---------------------------------------------------------#
        all_words_remaining,all_possible_letters_remaining=stp3.get_remaining_words(all_words_remaining,
                                                                                    all_possible_letters_remaining,
                                                                                    rag_colours,
                                                                                    trial_word)
        #-----------------------------------------#
        #--- Update tracking variables ---#
        #-----------------------------------------#

        #Get number of remaining words
        n_words_remaining=len(all_words_remaining)
        
    #---------------------------#
    #--- Generate next guess ---#
    #---------------------------#
    
    #If first iteration of brute force simple, it's quicker just to use manually generate the first word (which is the same every time)
    if rag_colours==None and next_word_selection=="brute_force_simple":
        next_guess="aerie"
    
    else:
        next_guess=stp1_0.generate_next_trial_word(next_word_selection,
                                                   all_words_remaining,
                                                   n_words_remaining,
                                                   all_possible_letters_remaining,
                                                   mode)
    
    #Return results
    return next_guess,all_words_remaining,n_words_remaining,all_possible_letters_remaining