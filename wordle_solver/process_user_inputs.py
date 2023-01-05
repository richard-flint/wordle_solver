#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#------------------------------------- Process user inputs ---------------------------------------#
#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#This is a high level function that applies routing logic to the arguments used by the user when
#calling the inital wordle function solver, and then returns the final results to the user. This 
#includes running different sections on code based on whether the user selected to run the wordle
#solver for one word only, or for multiple words (e.g. "100_words" or "all_words").

#-------------------------------------#
#--- Import packages and functions ---#
#-------------------------------------#

from english_words import english_words_set
from english_words import english_words_lower_alpha_set
import numpy as np
import random
import plotly.graph_objects as go
import pandas as pd
import time
from progressbar import progressbar

#Import user defined modules
from find_word import find_word
from helper_functions.other_helper_functions import other_helper_functions as oth

#Define classes for saving results
class WordleResultsOneWord:
    
    #Class attributes
    n_words_solved = 1
    
    #Object-specific attributes
    def __init__(self, actual_word,final_guess,n_guesses,t_solve):
        self.actual_word = actual_word
        self.final_guess = final_guess
        self.n_guesses = n_guesses
        self.t_solve = t_solve
        
class WordleResultsManyWords:
    
    #Object-specific attributes
    def __init__(self, n_guesses_all_words,t_solve_all_words,basic_stats):
        self.n_guesses_all_words = n_guesses_all_words
        self.t_solve_all_words = t_solve_all_words
        self.basic_stats = basic_stats

def run_wordle_solver(mode,next_word_selection,rag_colours):

    #------------------------------#
    #--- Initial pre_processing ---#
    #------------------------------#

    #Get list of all 5 letter words
    all_words,n_words=oth.get_all_five_letter_words(english_words_lower_alpha_set)

    #Initialise dictionary for saving results if doesn't already exist
    if "n_guesses_dict" not in locals():
        n_guesses_dict=dict()
        
    #--------------------------------------------#
    #--- Run for real wordle puzzle (web app) ---#
    #--------------------------------------------#
    
    if mode == "real_web_app":
        
        #Input dummy true word (as we don't know the true word for this mode)
        true_word="unknown"
        
        #Initialise various variables for "find_word" function
        all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
        
         all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=find_word_loop_function(all_words,true_word,next_word_selection,mode,rag_colours,all_words_remaining,n_words_remaining,all_possible_letters_remaining,count)
        
        #Output statistics
        print("\nThe word is: ", guess_word)
        print("Number of guesses: ",n_guesses)
    
    #----------------------------------#
    #--- Run for real wordle puzzle ---#
    #----------------------------------#

    elif mode == "real":
        
        #Input dummy true word (as we don't know the true word for this mode)
        true_word="unknown"
        
        #Find word using wordle solver
        guess_word,n_guesses=find_word(all_words,true_word,next_word_selection,mode,rag_colours)
        
        #Output statistics
        print("\nThe word is: ", guess_word)
        print("Number of guesses: ",n_guesses)
        
    #------------------------#
    #--- Run for one word ---#
    #------------------------#

    elif mode == "one_word":

        #Start timer
        start_time = time.time()

        #Generate true word
        true_word=oth.get_random_true_word(all_words)

        #Get checkpoint time before starting actual solver
        check_time = time.time()

        #Find word using wordle solver
        guess_word,n_guesses=find_word(all_words,true_word,next_word_selection,mode,rag_colours)

        #End timer
        end_time = time.time()

        #Total time calculations
        time_to_solve=end_time-check_time
        total_time_estimate_100_words=(end_time-start_time)*100
        total_time_estimate_all_words=(end_time-start_time)*n_words
        
        #Save results to object
        wordle_results = WordleResultsOneWord(true_word,guess_word,n_guesses,time_to_solve)

        #Print results
        print("The final guess is: ", guess_word)
        print("The actual word is: ",true_word)
        print("Number of guesses: ",n_guesses)
        print("Time taken to solve: ",round(time_to_solve,5),"s")
        print("Estimated time to run on 100 words: ",round(total_time_estimate_100_words,0),"s, or ",round(total_time_estimate_100_words/60,2)," minutes")
        print("Estimated time to run on all words: ",round(total_time_estimate_all_words,0),"s, or ",
              round(total_time_estimate_all_words/60,2)," minutes, or",round(total_time_estimate_all_words/3600,2)," hours")
        
        return wordle_results

    #----------------------------------#
    #--- Run for more than one word ---#
    #----------------------------------#

    #Check whether we are running shorter version (i.e. 100 words) or full version (i.e. all_words)
    elif (mode == "100_words" or mode == "all_words"):

        #*** Find words ***#

        #Initialise list for recording number of guesses
        n_guesses_all_words=[]

        #Define number of words to test
        if mode == "100_words":
            words_to_test=all_words[0:99]
        elif mode == "all_words":
            words_to_test=all_words.copy()
        n_words_to_test=len(words_to_test)
        
        #Start timer
        start_time = time.time()

        #Iterate through words to test
        for ind in progressbar(range(n_words_to_test)):
            
            #Get true word
            true_word=words_to_test[ind]

            #Get final guess for specific word
            guess_word,n_guesses=find_word(all_words,true_word,next_word_selection,mode,rag_colours)

            #Check that guess word is the same as the true word
            if guess_word!=true_word:
                
                #Print error statement if not the same
                print("ERROR! The final guess is not the same as the true word!")
                #Note that this would suggest a fault in the algorithm, since all algorithms
                #should eventually find the correct answer.

            #Save number of guesses
            n_guesses_all_words.append(n_guesses)

            #Record and print interation
            #print("Progress: ",ind,"/",n_words_to_test,end="\r")
            
        #End timer
        end_time = time.time()
        
        #Total time calculations
        time_to_solve=end_time-start_time
        
        #Get descriptive statistics
        n_guesses_all_words_as_series = pd.Series(n_guesses_all_words)
        basic_stats=n_guesses_all_words_as_series.describe()

        #Print basic statistics for number of guesses
        display(basic_stats)
        
        #And plot histogram of number of guesses
        fig = go.Figure(data=[go.Histogram(x=n_guesses_all_words)])
        fig.update_layout(title="Distribution of number of guesses to find words")
        fig.show()
        
        #Save results
        wordle_results = WordleResultsManyWords(n_guesses_all_words,time_to_solve,basic_stats)
        
        #Return saved results
        return wordle_results

    #Catch if user has incorrectly selected the model
    else:
        print('Error! You must select either: "real, "one_word", "100_words" or "all_words"')