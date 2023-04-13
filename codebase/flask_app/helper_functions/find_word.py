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
from helper_functions.step_1_generate_next_trial_word import overall_generate_next_trial_word as stp1_0
from helper_functions.step_2_generate_rag_score import generate_rag_score as stp2
from helper_functions.step_3_update_lists import error_handling as stp3
from helper_functions.other_helper_functions.wordle_classes import WordleRound

#Import other modules
import copy

def find_word_python(WordleGameParameters,true_word):
    
    #----------------------------#
    #--- Initialise variables ---#
    #----------------------------#
    
    #Initialise various variables for "find_word" function
    all_possible_letters_remaining,rank_start_word,bfs_start_word=stp0.initialise_variables(WordleGameParameters.all_words)
    
    #Initial WordleRound object for first round
    ThisWordleRound=WordleRound(n_previous_guesses=0,
                                previous_trial_word="N/A",
                                previous_rag_score="N/A",
                                n_words_remaining=WordleGameParameters.n_words,
                                remaining_words=WordleGameParameters.all_words,
                                remaining_letters=all_possible_letters_remaining,
                                round_number=1,
                                trial_word="TBD")
    
    #---------------------------------#
    #--- Generate first trial word ---#
    #---------------------------------#
    #No previous guess or rag score for generating first trial word, so easier to treat separately
    
    #If first iteration of brute force simple, it's quicker just to use manually generate the first word (which is the same every time)
    if WordleGameParameters.method=="brute_force_simple" and bfs_start_word!="":
        ThisWordleRound.trial_word=bfs_start_word

    #If first iteration of rank, it's quicker just to use manually generate the first word (which is the same every time)
    elif WordleGameParameters.method=="rank" and rank_start_word!="":
        ThisWordleRound.trial_word=rank_start_word

    #Otherwise, generate next word as normal
    else:
        ThisWordleRound=stp1_0.generate_next_trial_word(WordleGameParameters,ThisWordleRound)
        
    #Save details from first round round
    AllWordleRounds={"round_1":ThisWordleRound}
    
    #-------------------------#
    #--- Loop until solved ---#
    #-------------------------#
    
    #Loop until we get an all-"Green" RAG score
    while ThisWordleRound.previous_rag_score!=["Green","Green","Green","Green","Green"]:
        
        #Note: Each round builds up to generating the next guess
        
        #--------------------------------------------------#
        #--- Step 1: Create wordle class for this round ---#
        #--------------------------------------------------#
        ThisWordleRound=WordleRound(n_previous_guesses=ThisWordleRound.n_previous_guesses+1,
                                    previous_trial_word=ThisWordleRound.trial_word,
                                    previous_rag_score="TBD",
                                    n_words_remaining=ThisWordleRound.n_words_remaining, #Copy in temporarily, to be updated below
                                    remaining_words=ThisWordleRound.remaining_words, #Copy in temporarily, to be updated below
                                    remaining_letters=ThisWordleRound.remaining_letters, #Copy in temporarily, to be updated below
                                    round_number=ThisWordleRound.round_number+1,
                                    trial_word="TBD")
        
        #--------------------------------------------------------#
        #--- Step 2: Compare previous guess against true word ---#
        #--------------------------------------------------------#
        #This assigns "green", "amber" or "red" for each letter in the trial word compared to the true word
        ThisWordleRound=stp2.check_letters_automatically(ThisWordleRound,true_word)
        
        
        #---------------------------------#
        #--- Step 3: Check if finished ---#
        #---------------------------------#
        #If we have an all-"Green" rag score, we can fill in the remaining detail for this round
        #The loop will then exit
        if ThisWordleRound.previous_rag_score==["Green","Green","Green","Green","Green"]:
            ThisWordleRound.n_words_remaining=1
            ThisWordleRound.remaining_words
            ThisWordleRound.remaining_letters
            ThisWordleRound.trial_word="N/A"
            
            #Save details from this round
            round_name="round_"+str(ThisWordleRound.round_number)
            AllWordleRounds[round_name]=ThisWordleRound
            
        #Only continue if we dont have an all-"Green" rag score
        elif ThisWordleRound.previous_rag_score!=["Green","Green","Green","Green","Green"]:

            #-----------------------------------------------------------------#
            #--- Step 4: Generate updated list of remaining possible words ---#
            #-----------------------------------------------------------------#

            ThisWordleRound=stp3.get_remaining_words(ThisWordleRound)

            #-----------------------------------#
            #--- Step 5: Generate next guess ---#
            #-----------------------------------#
            
            #Generate next guess
            ThisWordleRound=stp1_0.generate_next_trial_word(WordleGameParameters,ThisWordleRound)

            #Save details from this round
            round_name="round_"+str(ThisWordleRound.round_number)
            AllWordleRounds[round_name]=ThisWordleRound

    #Return data once word is found
    return ThisWordleRound.previous_trial_word,ThisWordleRound.n_previous_guesses

#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#
#------------------------------------- Find word (flask app) ---------------------------------------#
#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#

#Run wordle solver for flask app
def find_word_flask(WordleGameParameters,ThisWordleRound):
    
    #Initialise error flag
    error_flag=0
    
    #------------------------------------#
    #--- Step 0: Check if first round ---#
    #------------------------------------#
    
    #If first iteration of brute force simple, it's quicker just to use manually generate the first word (which is the same every time)
    if WordleGameParameters.method=="brute_force_simple" and ThisWordleRound.round_number==1:
        ThisWordleRound.trial_word=bfs_start_word

    #If first iteration of rank, it's quicker just to use manually generate the first word (which is the same every time)
    elif WordleGameParameters.method=="rank" and ThisWordleRound.round_number==1:
        ThisWordleRound.trial_word=rank_start_word
        
    #If first iteration of rank, it's quicker just to use manually generate the first word (which is the same every time)
    elif WordleGameParameters.method=="random" and ThisWordleRound.round_number==1:
        ThisWordleRound=stp1_0.generate_next_trial_word(WordleGameParameters,ThisWordleRound)
    
    #Otherwise, generate next word as normal
    else:
        
        #-----------------------------------------------#
        #--- Step 1: Save lists in case we get error ---#
        #-----------------------------------------------#
        remaining_letters_temp=ThisWordleRound.remaining_letters
        remaining_words_temp=ThisWordleRound.remaining_words
        n_remaining_words_temp=ThisWordleRound.n_words_remaining
        
        #-----------------------------------------------------------------#
        #--- Step 2: Generate updated list of remaining possible words ---#
        #-----------------------------------------------------------------#

        ThisWordleRound,error_flag=stp3.get_remaining_words_with_error_handling(WordleGameParameters,ThisWordleRound)
        
        #-----------------------------------#
        #--- Step 3: Generate next guess ---#
        #-----------------------------------#
        
        #If no error, then generate next guess
        if error_flag==0:
            ThisWordleRound=stp1_0.generate_next_trial_word(WordleGameParameters,ThisWordleRound)
    
    #Return results
    return ThisWordleRound,error_flag