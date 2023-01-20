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
from english_words import english_words_set
from english_words import english_words_lower_alpha_set
import copy

from helper_functions.find_word import find_word_flask
from helper_functions.other_helper_functions import other_helper_functions as oth
from helper_functions.step_0_initialise_variables import initialise_variables as stp0

#-----------------------#
#--- Start flask app ---#
#-----------------------#

app = Flask(__name__)
app.config["DEBUG"] = True

#-----------------------------------#
#--- Initialise global variables ---#
#-----------------------------------#
#For speed of development, we'll use global variables, but would potentially be better to use a backend SQL database

#Get list of all 5 letter words
all_words,n_words=oth.get_all_five_letter_words(english_words_lower_alpha_set)

#------------------------#
#--- Page 0: Homepage ---#
#------------------------#

@app.route("/", methods=["GET", "POST"])
@app.route("/home/<reset>", methods=["GET", "POST"])
def wordle_homepage(reset="yes"):  
    
    #------------------------------#
    #--- Check if (re-)starting ---#
    #------------------------------#
    
    #If we just starting or ressting...
    if reset=="yes":
    
        #...just set error message
        error_message=""
        
        #...and display homepage at bottom of function
        
    #--------------------#
    #--- Check method ---#
    #-------------------#
    
    #Otherwise, if not restarting, check user input
    elif reset=="no":
    
        #Initialise variables for checking method
        method = None
        accepted_methods=["random","rank","brute_force_simple"] #Initialise list for checking input
        error_message=""

        #Get input for method variable
        method = request.form["methodinput"].lower()

        #Check that method variable is from accepted list
        if method not in accepted_methods:

            #If not, create output message...
            error_message = "" #Blank actually looks better for now

            #...and display homepage at bottom of function

        #If method is in accepted list
        elif method in accepted_methods:
            
            #----------------------------#
            #--- Get first trial word ---#
            #----------------------------#

            #Ensure relevant variables are global
            global all_words,n_words
            global all_words_remaining,n_words_remaining,all_possible_letters_remaining,count
            global next_word_selection
            global rag_colours,previous_rag_colours
            global trial_word,previous_trial_word

            #Initialise global variables
            all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
            next_word_selection=""
            remove_trial_word="no"
            rag_colours=""
            previous_rag_colours=""
            trial_word=""
            previous_trial_word=""

            #Initialise local variables
            mode="real_flask"
            next_word_selection=method

            #Get trial word
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)

            #Redirect to rag score page
            return redirect("/find_word/no", code=301)
        
    #----------------------#
    #--- Otherwise ---#
    #----------------------#
    
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
    global all_words,n_words
    global all_words_remaining,n_words_remaining,all_possible_letters_remaining,count
    global next_word_selection
    global rag_colours,previous_rag_colours
    global trial_word,previous_trial_word
    
    #Initialise variables
    error_message = "" #Initialise error string for printing error if needed
    accepted_colours=["Green","Orange","Red"] #Initialise list for checking input
    possible_words="All words currently available."
    
    #-----------------------------------------#
    #--- Remove trial word if not accepted ---#
    #-----------------------------------------#
    
    #Check if trial word is accepted. If not we need to bin it and get the next best word
    if remove_trial_word=="yes" and n_words_remaining>1:
        
        #Check if trial word is first word for brute force
        if trial_word=="aerie": #"aerie" is currently the first word in the brute force method
        
            #Do not remove word, and add error message
            error_message="'aerie' is definitely accepted by the Wordle app! Try inputting it again."
            
        #Otherwise, continue to remove word    
        else:

            #Remove trial word from list
            all_words_remaining.remove(trial_word)
            n_words_remaining=n_words_remaining-1

            #Get next trial word
            mode="real_flask"
            trial_word=previous_trial_word
            rag_colours=previous_rag_colours
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)
            
            #Get remaining possible words as string
            possible_words=get_possible_words_as_string(all_words_remaining)
    
    #-------------------------------------------------#
    #--- Process user input if we have rag colours ---#
    #-------------------------------------------------#
    elif remove_trial_word=="no" and rag_colours!="" and n_words_remaining>1:
        
        #Check that variables are accepted
        input_flag=0
        for colour in rag_colours:
            if colour not in accepted_colours:
                input_flag=1
        
        #If one or more variables are not accepted, output error
        if input_flag==1:
            error_message = "At least one input is not accepted. Try again.\n"
        
        #Else, get next word and update global variables
        elif input_flag==0:
            
            #---------------------------#
            #--- Get next trial word ---#
            #---------------------------#
            
            #Temporary save previous trial word and rag score before generating new trial word
            previous_trial_word_temp=trial_word
            previous_rag_colours_temp=rag_colours
            
            #Get next trial word
            mode="real_flask"
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)
            
            #If we have an error
            if error_flag==1:
                
                #We don't reset the previous trial word and rag score
                previous_trial_word_temp=None
                previous_rag_colours_temp=None
                
            #Else if there's no error, we can safely move on
            elif error_flag==0:
                previous_trial_word=previous_trial_word_temp
                previous_rag_colours=previous_rag_colours_temp
                
            #Get remaining possible words as string
            possible_words=get_possible_words_as_string(all_words_remaining)
            
    #Else, if we just have one word remaining
    elif n_words_remaining==1:
        
        #Set error message for trying to find more words
        error_message="There are no more words left...you have found the word! To re-start, press 'Reset wordle solver'"
        possible_words=trial_word
            
    #----------------------#
    #--- Output webpage ---#
    #----------------------#
    
    #Ensure rag colours are reset before outputting webpage
    rag_colours=["Red","Red","Red","Red","Red"]
    
    #Display webpage
    return render_template('rag_input_page.html',
                           error_message=error_message,
                           possible_words=possible_words,
                           trial_word=trial_word,
                           n_words_remaining=n_words_remaining)

def get_possible_words_as_string(all_words_remaining):
    possible_words=all_words_remaining[0]
    for word in all_words_remaining[1:]:
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
    print("it me, richard, just storing some colours")
    return jsonify({"message": "Colors stored successfully!"})

if __name__ == '__main__':
  app.run()