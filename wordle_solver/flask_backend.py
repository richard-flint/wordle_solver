#-------------------------------------#
#--- Import packages and functions ---#
#-------------------------------------#

#from english_words import english_words_set
#from english_words import english_words_lower_alpha_set
#import numpy as np
#import random
#import plotly.graph_objects as go
#import pandas as pd
#import time
#from progressbar import progressbar

#Import user defined modules
#from find_word import find_word
#from helper_functions.other_helper_functions import other_helper_functions as oth
from helper_functions.step_1_generate_next_trial_word import overall_generate_next_trial_word as stp1_0
from helper_functions.step_3_update_lists import generate_updated_list as stp3

#Import user defined functions
#from helper_functions.step_0_initialise_variables import initialise_variables as stp0
#from helper_functions.step_1_generate_next_trial_word import option_1_random_guess as stp1_1
#from helper_functions.step_1_generate_next_trial_word import option_2_most_frequent_letter as stp1_2
#from helper_functions.step_1_generate_next_trial_word import option_3_brute_force as stp1_3
#from helper_functions.step_2_generate_rag_score import generate_rag_score as stp2


def run_wordle_solver_flask(mode,next_word_selection,rag_colours,trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining):

    #For anything other than the first run
    if rag_colours!=None:
    
        #-----------------------------------------------------------------#
        #--- Step 3: Generate updated list of remaining possible words ---#
        #-----------------------------------------------------------------#
        all_words_remaining,all_possible_letters_remaining=stp3.get_remaining_words(all_words_remaining,
                                                                                    all_possible_letters_remaining,
                                                                                    rag_colours,
                                                                                    trial_word)
        #-----------------------------------------#
        #--- Step 4: Update tracking variables ---#
        #-----------------------------------------#

        #Get number of remaining words
        n_words_remaining=len(all_words_remaining)
        
    #------------------------------#
    #--- Step 1: Generate guess ---#
    #------------------------------#
        
    next_guess=stp1_0.generate_next_trial_word(next_word_selection,
                                               all_words_remaining,
                                               n_words_remaining,
                                               all_possible_letters_remaining,
                                               mode)
    
    #Return results
    return next_guess,all_words_remaining,n_words_remaining,all_possible_letters_remaining