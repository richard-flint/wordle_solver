#Imports
import copy
from backend._2_helper_functions.step_3_update_lists import generate_updated_list as stp3

def get_remaining_words_with_error_handling(all_words_remaining,all_possible_letters_remaining,rag_score,trial_word,mode):
    
    #Initial variables
    error_flag=0
    error_message=""
    
    #-------------------------#
    #--- No error handling ---#
    #-------------------------#
    
    #For anything other than "real_python" or "real_flask" modes, there shouldn't be any errors
    #We exclude the error handling below because it will slow down the script when iterating over large amounts of words
    if mode!="real_python" and mode!="real_flask":
        all_words_remaining,all_possible_letters_remaining=stp3.get_remaining_words(all_words_remaining,
                                                                                    all_possible_letters_remaining,
                                                                                    rag_score,
                                                                                    trial_word)
        
        return all_words_remaining,all_possible_letters_remaining,error_flag,error_message
    
    #----------------------#
    #--- Error handling ---#
    #----------------------#

    #We need additional error handling for "real_python" or "real_flask" mode because users can input incorrect inputs
    elif mode=="real_python" or mode=="real_flask":
        try:
            #Copy variables so to not overwrite
            all_words_remaining_temp=copy.deepcopy(all_words_remaining)
            all_possible_letters_remaining_temp=copy.deepcopy(all_possible_letters_remaining)

            #Try trial word and RAG scope
            all_words_remaining_temp,all_possible_letters_remaining_temp=stp3.get_remaining_words(all_words_remaining_temp,
                                                                                                  all_possible_letters_remaining_temp,
                                                                                                  rag_score,
                                                                                                  trial_word)

            #If the RAG score generates no remaining possible words, there's been an error and we need to ask users to re-input score
            if len(all_words_remaining_temp)==0:
                error_message="ERROR 1: The RAG input produces no possible words. There must be an error. Please re-input a RAG score."
                error_flag=1

            #Otherwise, their user input is OK
            else:
                all_words_remaining=copy.deepcopy(all_words_remaining_temp)
                all_possible_letters_remaining=copy.deepcopy(all_possible_letters_remaining_temp)

                #Return number of words in update list if running in "real_python" mode
                if mode == "real_python":
                    error_message=f"Number of possible words remaining: {len(all_words_remaining)}"

        #If there's an error in generating the list of remaining words, this is likely because the RAG score generates no remaining possible words
        #Again, we will ask the user to re-input the RAG score.
        except:
            error_message=f"ERROR 2: The RAG input produces no possible words. There must be an error. Please re-input a RAG score."
            error_flag=1
            
        #Return values
        return all_words_remaining,all_possible_letters_remaining,error_flag,error_message