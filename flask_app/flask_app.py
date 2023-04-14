#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#------------------------------------- Flask App ---------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#

#--- Run locally ---#
#To run on a local machine, navigate to the relevant folder in the terminal and use the command: python flask_app.py
#To navigate, use "cd .\OneDrive\Documents\GitHub\wordle_solver\codebase\flask_app"

#---------------#
#--- Imports ---#
#---------------#

from flask import Flask, request, render_template, jsonify, redirect, url_for
import copy

from helper_functions.find_word import find_word_flask
from helper_functions.other_helper_functions import other_helper_functions as oth
from helper_functions.initialise_variables import initialise_variables as stp0
from helper_functions.other_helper_functions.wordle_classes import WordleGame
from helper_functions.other_helper_functions.wordle_classes import WordleRound

#-----------------------#
#--- Start flask app ---#
#-----------------------#

app = Flask(__name__)
app.config["DEBUG"] = True

#-----------------------------------#
#--- Initialise global variables ---#
#-----------------------------------#
#For speed of development, we'll use global variables, but would potentially be better to use a backend database

#Get list of all 5 letter words
all_words,n_words=oth.import_wordle_word_list()

#Create dictionary for storing all rounds
AllWordleRounds={}

#------------------------#
#--- Page 0: Homepage ---#
#------------------------#

@app.route("/", methods=["GET", "POST"])
@app.route("/home/<reset>", methods=["GET", "POST"])
def wordle_homepage(reset="yes"):  #Default value is "yes" if no value provided
    
    #Define global variables
    global WordleGameParameters, ThisWordleRound, AllWordleRounds
    global rank_start_word,bfs_start_word
    
    #------------------------------#
    #--- Check if (re-)starting ---#
    #------------------------------#
    
    #If we just starting or ressting...
    if reset=="yes":
    
        #...just set error message
        error_message=""
        
        #And clear AllWordleRounds variable
        AllWordleRounds={}
        
        #...and display homepage at bottom of function
        
    #--------------------#
    #--- Check method ---#
    #--------------------#
    
    #Otherwise, if not restarting, check user input
    elif reset=="no":
    
        #Initialise variables for checking method
        method = None
        accepted_methods=["random","rank","brute_force_simple"] #Initialise list for checking input
        error_message=""

        #Get input for method variable
        method = request.form["methodinput"].lower()
        
        #If method is ChatGPT, output specific error message
        if method=="chatgpt":
            
            #Provide specific error message
            #error_message = "The ChatGPT method is not currently available on the web app because of the cost of using the API. However, you can try this method yourself by cloning the GitHub repository and using your own API key." 
            
            error_message = "" #Blank actually also still looks better for now

            #...and display homepage at bottom of function
            
        #Otherwise, check that method variable is from accepted list
        elif method not in accepted_methods:

            #If not, create output message...
            error_message = "" #Blank actually looks better for now

            #...and display homepage at bottom of function

        #------------------#
        #--- Start game ---#
        #------------------#
        
        #If method is in accepted list
        elif method in accepted_methods:
            
            #Create instance of WordleGameParameters
            mode="real_flask"
            WordleGameParameters=WordleGame(all_words,n_words,method,mode)
            
            #----------------------------#
            #--- Get first trial word ---#
            #----------------------------#

            #Initialise variables
            all_possible_letters_remaining,rank_start_word,bfs_start_word=stp0.initialise_variables(all_words)
            
            #Initialise WordleRound object for first round
            ThisWordleRound=WordleRound(n_previous_guesses=0,
                                        previous_trial_word="N/A",
                                        previous_rag_score="N/A",
                                        n_words_remaining=WordleGameParameters.n_words,
                                        remaining_words=WordleGameParameters.all_words,
                                        remaining_letters=all_possible_letters_remaining,
                                        round_number=1,
                                        trial_word="TBD",
                                        error=0,
                                        error_message="")

            #Get first trial word
            if WordleGameParameters.method=="rank":
                ThisWordleRound.trial_word=rank_start_word
            elif WordleGameParameters.method=="brute_force_simple":
                ThisWordleRound.trial_word=bfs_start_word
            else:
                ThisWordleRound,error_flag=find_word_flask(WordleGameParameters,ThisWordleRound)
                
            #Store wordle round
            AllWordleRounds["ThisWordleRound1"]=ThisWordleRound

            #Redirect to rag score page
            return redirect("/find_word/no", code=301)
        
    #-----------------#
    #--- Otherwise ---#
    #-----------------#
    
    #And if all else fails...
    else:
        
        #...just set error message
        error_message=""
    
    #----------------------#
    #--- Output webpage ---#
    #----------------------#
    return render_template('home_page_with_formatting.html', error_message=error_message)
        
#--------------------------------------#
#--- Page 2: Input RAG scores pages ---#
#--------------------------------------#

@app.route("/find_word/<remove_trial_word>", methods=["GET", "POST"])
def wordle_solver(remove_trial_word="no"):
    
    #Ensure relevant variables are global
    global WordleGameParameters,ThisWordleRound,AllWordleRounds
    global rank_start_word,bfs_start_word
    
    #Initialise variables
    error_message = "" #Initialise error string for printing error if needed
    accepted_colours=["Green","Orange","Red"] #Initialise list for checking input
    possible_words="All words currently available."
    error_flag=0
    
    #--------------------------------------------#
    #--- Create updated object if first guess ---#
    #--------------------------------------------#
    #After the first guess, we have no RAG score, so it is different
    if ThisWordleRound.round_number==1:
        
        #Create new object for next wordle round
        ThisWordleRound=WordleRound(n_previous_guesses=ThisWordleRound.n_previous_guesses+1,
                                    previous_trial_word=ThisWordleRound.trial_word,
                                    previous_rag_score="TBD",
                                    n_words_remaining=ThisWordleRound.n_words_remaining, #Copy in temporarily, to be updated in next round
                                    remaining_words=ThisWordleRound.remaining_words, #Copy in temporarily, to be updated in next round
                                    remaining_letters=ThisWordleRound.remaining_letters, #Copy in temporarily, to be updated in next round
                                    round_number=ThisWordleRound.round_number+1,
                                    trial_word=ThisWordleRound.trial_word, #Copy in temporarily, to be updated in next round
                                    error=0,
                                    error_message="")
        
        
    
    #-----------------------------------------#
    #--- Remove trial word if not accepted ---#
    #-----------------------------------------#
    
    #Check if trial word is accepted. If not we need to bin it and get the next best word
    elif remove_trial_word=="yes" and ThisWordleRound.n_words_remaining>1:
        
        #Check if we're round one. If we are, then we don't allow word removal
        #Note: This would be theoretcally possible, but would be slow for slower algorithms.
        if ThisWordleRound.round_number==2:
            error_message="This starting word is definitely allowed! Please input the RAG score for this word and generate the next trial word."

        else:
            #Remove trial word from list
            ThisWordleRound.remaining_words.remove(ThisWordleRound.previous_trial_word)
            ThisWordleRound.n_words_remaining=ThisWordleRound.n_words_remaining-1

            #Get previous trial word and rag score
            name="ThisWordleRound"+str(ThisWordleRound.round_number-1)
            ThisWordleRound.previous_trial_word=AllWordleRounds[name].previous_trial_word
            ThisWordleRound.previous_rag_score=AllWordleRounds[name].previous_rag_score

            #Get next trial word
            ThisWordleRound,error_flag=find_word_flask(WordleGameParameters,ThisWordleRound)

            #Create new object for next
            ThisWordleRound=WordleRound(n_previous_guesses=ThisWordleRound.n_previous_guesses, #We dont update the n. guesses as we have only dropped a word
                                            previous_trial_word=ThisWordleRound.trial_word,
                                            previous_rag_score="TBD",
                                            n_words_remaining=ThisWordleRound.n_words_remaining, #Copy in temporarily, to be updated in next round
                                            remaining_words=ThisWordleRound.remaining_words, #Copy in temporarily, to be updated in next round
                                            remaining_letters=ThisWordleRound.remaining_letters, #Copy in temporarily, to be updated in next round
                                            round_number=ThisWordleRound.round_number, #We dont update the round number as we have only dropped a word
                                            trial_word=ThisWordleRound.trial_word, #Copy in temporarily, to be updated in next round
                                            error=0,
                                            error_message="")


            #Get remaining possible words as string
            possible_words=get_possible_words_as_string(ThisWordleRound)
    
    #--------------------------#
    #--- Process user input ---#
    #--------------------------#
    elif remove_trial_word=="no" and ThisWordleRound.n_words_remaining>1 and ThisWordleRound.n_previous_guesses>0:
        
        #---------------------------#
        #--- Get next trial word ---#
        #---------------------------#

        #Save RAG colours into wordle round object
        global rag_colours
        ThisWordleRound.previous_rag_score=rag_colours

        #Get next trial word
        ThisWordleRound,error_flag=find_word_flask(WordleGameParameters,ThisWordleRound)

        #If we have an error
        if error_flag==1:
            
            #Print error message, and make no update to wordle object
            #Note: wordle object remains unchanged by "find_word_flask" object if there is an error
            error_message="This input produces no remaining possible words. Please try again."
        
        #Else if we dont have an error flag, save output and create updated object for next round
        elif error_flag==0:
            
            #Save wordle round
            name="ThisWordleRound"+str(ThisWordleRound.round_number)
            AllWordleRounds[name]=ThisWordleRound
            
            #Generate next worde round
            ThisWordleRound=WordleRound(n_previous_guesses=ThisWordleRound.n_previous_guesses+1,
                                        previous_trial_word=ThisWordleRound.trial_word,
                                        previous_rag_score="TBD",
                                        n_words_remaining=ThisWordleRound.n_words_remaining, #Copy in temporarily, to be updated in next round
                                        remaining_words=ThisWordleRound.remaining_words, #Copy in temporarily, to be updated in next round
                                        remaining_letters=ThisWordleRound.remaining_letters, #Copy in temporarily, to be updated in next round
                                        round_number=ThisWordleRound.round_number+1,
                                        trial_word=ThisWordleRound.trial_word, #Copy in temporarily, to be updated in next round
                                        error=0,
                                        error_message="")

        #Get remaining possible words as string
        possible_words=get_possible_words_as_string(ThisWordleRound)
            
    #Else, if we just have one word remaining
    elif ThisWordleRound.n_words_remaining==1:
        
        #Set error message for trying to find more words
        error_message="There are no more words left...you have found the word! To re-start, press 'Reset wordle solver'"
            
    #----------------------#
    #--- Output webpage ---#
    #----------------------#
    
    #Ensure rag colours are reset before outputting webpage
    rag_colours=["Red","Red","Red","Red","Red"]
    
    #Display webpage
    return render_template('rag_input_page.html',
                           error_message=error_message,
                           possible_words=possible_words,
                           trial_word=ThisWordleRound.trial_word,
                           n_words_remaining=ThisWordleRound.n_words_remaining)

def get_possible_words_as_string(ThisWordleRound):
    possible_words=ThisWordleRound.remaining_words[0]
    for word in ThisWordleRound.remaining_words[1:]:
            possible_words=possible_words+", "+word
    return possible_words


def tile_colour_mapping(colour: str):
    if colour=='lightgrey' or colour=="":
        colour='Red'
    else:
        colour=colour.capitalize()
    return colour

@app.route("/store_colors", methods=["POST"])
def store_colors():
    data = request.get_json()
    global rag_colours
    rag_colours=[tile_colour_mapping(data['tile1']),
                 tile_colour_mapping(data['tile2']),
                 tile_colour_mapping(data['tile3']),
                 tile_colour_mapping(data['tile4']),
                 tile_colour_mapping(data['tile5'])]
    return jsonify({"message": "Colors stored successfully!"})

if __name__ == '__main__':
  app.run()