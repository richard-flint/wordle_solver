#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#------------------------------------- Find word ---------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#This is a high level algorithm for finding the "true word" in a wordle puzzle
#It breaks the problem down into four main steps, each of which calls one or more additional
#user defined functions.

#Import user defined functions
from backend._2_helper_functions.step_0_initialise_variables import initialise_variables as stp0
from backend._2_helper_functions.step_1_generate_next_trial_word import overall_generate_next_trial_word as stp1_0
from backend._2_helper_functions.step_2_generate_rag_score import generate_rag_score as stp2
from backend._2_helper_functions.step_3_update_lists import error_handling as stp3

#Import other modules
import copy

def find_word_python(all_words,true_word,next_word_selection,mode,rag_colours):
    
    #----------------------------#
    #--- Initialise variables ---#
    #----------------------------#
    
    #Initialise various variables for "find_word" function
    all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
    n_words=len(all_words)
    error_flag=0 #Initialise error flag
    
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
        
        #If first iteration of brute force simple, it's quicker just to use manually generate the first word (which is the same every time)
        if n_words_remaining==n_words and next_word_selection=="brute_force_simple":
            trial_word="aerie"
        
        #If there is an error flag, we don't want to re-generate a new random word
        elif error_flag==1:
            
            #Reset error flag
            error_flag=0
        
        #Otherwise, generate next word as normal
        else:
            trial_word=stp1_0.generate_next_trial_word(next_word_selection,
                                                       all_words_remaining,
                                                       n_words_remaining,
                                                       all_possible_letters_remaining,
                                                       mode)

        #Check trial word
        #If mode=="real_python" (i.e. we are running the wordle solver for real...
        #...within a python interface), we need check the word selection is actually
        #... accepted by the app, and then also print out the next word selection so
        #...that the user can input this into their app.
        if mode=="real_python":
            
            print("\nThe next guess is: ",trial_word)
            trial_word_check_flag=0
            while trial_word_check_flag==0:
                
                #Check with users that trial word is accepted by the actual wordle app
                input_string=f"Is this word accepted by the wordle app? [OPTIONS: Yes, No]"
                trial_word_check=input(input_string).lower()[0] #Take just the first letter and make lowercase 
                                                                #to account for different user inputs
                
                #If trial word is not accepted, we need to bin and get the next ebst trial word
                if trial_word_check=="n":
                    all_words_remaining.remove(trial_word)
                    n_words_remaining=n_words_remaining-1
                    trial_word=stp1_0.generate_next_trial_word(next_word_selection,
                                                               all_words_remaining,
                                                               n_words_remaining,
                                                               all_possible_letters_remaining,
                                                               mode)
                
                #If trial word is accepted, we move on
                elif trial_word_check=="y":
                    trial_word_check_flag=1
                
                else:
                    print("\nInput error. Re-enter input.")
            

        #-----------------------------------------------#
        #--- Step 2: Compare guess against true word ---#
        #-----------------------------------------------#
        #This assigns "green", "amber" or "red" for each letter in the trial word compared...
        #...to the true word

        #If we are in "real_python" mode, this is done by the user
        if mode=="real_python":
            rag_colours=stp2.check_letters_manually()

        #If we are not in "real_python" mode, this is done automatically
        elif mode!="real_python":
            rag_colours=stp2.check_letters_automatically(true_word,trial_word)

        #-----------------------------------------------------------------#
        #--- Step 3: Generate updated list of remaining possible words ---#
        #-----------------------------------------------------------------#
        
        all_words_remaining,all_possible_letters_remaining,error_flag,error_message=stp3.get_remaining_words_with_error_handling(all_words_remaining,
                                                                                                                                all_possible_letters_remaining,
                                                                                                                                rag_colours,
                                                                                                                                trial_word,
                                                                                                                                mode)
        if mode=="real_python":
            print(error_message)

        #-----------------------------------------#
        #--- Step 4: Update tracking variables ---#
        #-----------------------------------------#
        
        if error_flag!=1:
            
            #Get number of remaining words
            n_words_remaining=len(all_words_remaining)
        
            #Add one to i for tracking number of loops
            count+=1

    #If the final RAG input was not [Green,Green,Green,Green,Green], we need to add one to the final count. This
    #is because the final guess is not counted unless it is [Green,Green,Green,Green,Green].
    if rag_colours!=["Green","Green","Green","Green","Green"]:
        count+=1

    #Return word once found
    return all_words_remaining[0],count

#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#
#------------------------------------- Find word (flask app) ---------------------------------------#
#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#

#Run wordle solver for flask app
def find_word_flask(mode,next_word_selection,rag_colours,trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,remove_trial_word):
    
    #Initialise variables
    error_flag=0
    error_message=""
    
    #For anything other than the first run, we first need to generate an updated list of possible words based on the previous trial word and the rag score
    if rag_colours!=None and remove_trial_word=="No":
    
        #-----------------------------------------------------------------#
        #--- Step 1: Generate updated list of remaining possible words ---#
        #-----------------------------------------------------------------#
        all_words_remaining,all_possible_letters_remaining,error_flag,error_message=stp3.get_remaining_words_with_error_handling(all_words_remaining,
                                                                                                                            all_possible_letters_remaining,
                                                                                                                            rag_colours,
                                                                                                                            trial_word,
                                                                                                                            mode)

        #-----------------------------------------#
        #--- Step 2: Update tracking variables ---#
        #-----------------------------------------#

        #Get number of remaining words
        if error_flag==0:
            n_words_remaining=len(all_words_remaining)
        
    #-----------------------------------#
    #--- Step 3: Generate next guess ---#
    #-----------------------------------#
    
    #Only generate next guess if no error
    if error_flag==0:
    
        #If first iteration of brute force simple, it's quicker just to use manually generate the first word (which is the same every time)
        if rag_colours==None and next_word_selection=="brute_force_simple":
            trial_word="aerie"

        #For everything else, both first guesses nad next guess, we generate the next guess
        else:
            trial_word=stp1_0.generate_next_trial_word(next_word_selection,
                                                       all_words_remaining,
                                                       n_words_remaining,
                                                       all_possible_letters_remaining,
                                                       mode)
    
    #Return results
    return trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message