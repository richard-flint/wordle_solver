#Imports
import copy
from helper_functions.update_lists import generate_updated_list as stp3

def get_remaining_words_with_error_handling(WordleGameParameters,ThisWordleRound):
    
    #Initial variables
    error_flag=0
    error_message=""
    
    #-------------------------#
    #--- No error handling ---#
    #-------------------------#
    
    #For anything other than "real_flask" mode, there shouldn't be any errors
    #We exclude the error handling below because it will slow down the script when iterating over large amounts of words
    if WordleGameParameters.mode!="real_flask":
        ThisWordleRound=stp3.get_remaining_words(ThisWordleRound)
        
        return ThisWordleRound,error_flag
    
    #----------------------#
    #--- Error handling ---#
    #----------------------#

    #We need additional error handling for "real_flask" mode because users can input incorrect inputs
    elif WordleGameParameters.mode=="real_flask":
        
        #Copy variables so to not overwrite
        remaining_words_temp=ThisWordleRound.remaining_words
        remaining_letters_temp=copy.deepcopy(ThisWordleRound.remaining_letters)
        n_remaining_words_temp=ThisWordleRound.n_words_remaining
        
        try:

            #Try trial word and RAG scope
            ThisWordleRound=stp3.get_remaining_words(ThisWordleRound)

            #If the RAG score generates no remaining possible words, there's been an error and we need to ask users to re-input score
            if ThisWordleRound.n_words_remaining==0:
                
                #Set error flag
                error_flag=1
                
                #Restore previous lists
                ThisWordleRound.remaining_words=remaining_words_temp
                ThisWordleRound.remaining_letters=copy.deepcopy(remaining_letters_temp)
                ThisWordleRound.n_words_remaining=n_remaining_words_temp

        #If there's an error in generating the list of remaining words, this is likely because the RAG score generates no remaining possible words
        #Again, we will ask the user to re-input the RAG score.
        except:
            #Set error flag
            error_flag=1

            #Restore previous lists
            ThisWordleRound.remaining_words=remaining_words_temp
            ThisWordleRound.remaining_letters=copy.deepcopy(remaining_letters_temp)
            ThisWordleRound.n_words_remaining=n_remaining_words_temp
            
        #Return values
        return ThisWordleRound,error_flag