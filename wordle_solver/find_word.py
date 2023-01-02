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

def find_word(all_words,true_word,next_word_selection,mode):
    
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
        
        #------------------------------#
        #--- Step 1: Generate guess ---#
        #------------------------------#
        
        #Option 1: Generate trail word at random
        if next_word_selection=="random":
            trial_word=stp1_1.generate_random_trial_word(all_words_remaining)
        
        #Option 2: Generate trial word by finding word whose letters appear in the most amount of other words 
        elif next_word_selection=="rank":
            trial_word=stp1_2.generate_word_from_most_frequent_remaining_letters(all_words_remaining,
                                                                                 n_words_remaining,
                                                                                 all_possible_letters_remaining)

        #Option 3: Brute force
        elif (next_word_selection=="brute_force_simple" or next_word_selection=="brute_force_extended"):
            trial_word=stp1_3.generate_word_using_brute_force(next_word_selection,all_words_remaining,n_words_remaining,all_possible_letters_remaining,mode)
            
        #Print trial word
        #If mode=="real" (i.e. we are running the wordle solver for real), we need to print out the next
        #word selection so that the user can input this into their app.
        if mode=="real":
            print("\nThe next guess is: ",trial_word)

        #-----------------------------------------------#
        #--- Step 2: Compare guess against true word ---#
        #-----------------------------------------------#
        #This assigns "green", "amber" or "red" for each letter in the trial word compared...
        #...to the true word
        
        #If we are not in "real" mode, this is done automatically
        if mode!="real":
            rag_score=stp2.check_letters_automatically(true_word,trial_word)
        
        #If we are in "real" mode, this is done by the user
        elif mode=="real":
            rag_score=stp2.check_letters_manually()
        
        #-----------------------------------------------------------------#
        #--- Step 3: Generate updated list of remaining possible words ---#
        #-----------------------------------------------------------------#
        all_words_remaining,all_possible_letters_remaining=stp3.get_remaining_words(all_words_remaining,
                                                                                    all_possible_letters_remaining,
                                                                                    rag_score,
                                                                                    trial_word)
        
        #Return number of words in update list if running in "real" mode
        if mode == "real":
            print("Number of possible words remaining: ",len(all_words_remaining))
        
        #-----------------------------------------#
        #--- Step 4: Update tracking variables ---#
        #-----------------------------------------#
        
        #Get number of remaining words
        n_words_remaining=len(all_words_remaining)

        #Add one to i for tracking number of loops
        count+=1
        
    #If the final RAG input was not [Green,Green,Green,Green,Green], we need to add one to the final count. This
    #is because the final guess is not counted unless it is [Green,Green,Green,Green,Green].
    if rag_score!=["Green","Green","Green","Green","Green"]:
        count+=1
        
    #Return word once found
    return all_words_remaining[0],count