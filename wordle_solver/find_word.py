#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#------------------------------------- Find word ---------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#This is a high level algorithm for finding the "true word" in a wordle puzzle
#It breaks the problem down into four main steps, each of which calls one or more additional
#user defined functions.

#Import user defined functions
from helper_functions.step_0_initialise_variables import initialise_variables as stp0
from helper_functions.step_1_generate_next_trial_word import option_1_random_guess as stp1_1
from helper_functions.step_1_generate_next_trial_word import option_2_most_frequent_letter as stp1_2
from helper_functions.step_1_generate_next_trial_word import option_3_brute_force as stp1_3
from helper_functions.step_2_generate_rag_score import generate_rag_score as stp2
from helper_functions.step_3_update_lists import generate_updated_list as stp3

def find_word(all_words,true_word,next_word_selection,mode,rag_colours):
    
    #------------------------------------#
    #--- Step 0: Initialise variables ---#
    #------------------------------------#
    
    #Initialise various variables for "find_word" function
    all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
    
    #*******************************************************************************************************#
    #Explaining key variables:
    #--- "all_words_remaining" = list of all reamining possible words. Note: This list is reduced over time
    #                            until there is just one word remaining
    #--- "all_possible_letters_remaining" = a dictionary with five keys ("column_0" to "column_4") which
    #                                       correspond to the 5 columns or spaces in a 5-letter wordle
    #                                       word. Each key in the dictionary is initialised with all 26
    #                                       letters of the alphabet, but this is reduced over time as
    #                                       specific letters are ruled out for each column.
    #*******************************************************************************************************#
    
    #Loop until there is only one possible remaining word
    while n_words_remaining>1:
        
        #Run one interation
        all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=find_word_loop_function(all_words,true_word,next_word_selection,mode,rag_colours,all_words_remaining,n_words_remaining,all_possible_letters_remaining,count)
        
    #If the final RAG input was not [Green,Green,Green,Green,Green], we need to add one to the final count. This
    #is because the final guess is not counted unless it is [Green,Green,Green,Green,Green].
    if rag_score!=["Green","Green","Green","Green","Green"]:
        count+=1
        
    #Return word once found
    return all_words_remaining[0],count