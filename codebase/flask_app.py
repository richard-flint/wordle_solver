#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#------------------------------------- Flask App ---------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#

#--- Run locally ---#
#To run on a local machine, navigate to the relevant folder in the terminal and use the command: python flask_app.py
#To navigate, use "cd .\OneDrive\Documents\GitHub\wordle_solver\codebase\"

#---------------#
#--- Imports ---#
#---------------#

from flask import Flask, request, render_template, jsonify, redirect, url_for
from english_words import english_words_set
from english_words import english_words_lower_alpha_set
import copy

from backend._2_helper_functions.find_word import find_word_flask
from backend._2_helper_functions.other_helper_functions import other_helper_functions as oth
from backend._2_helper_functions.step_0_initialise_variables import initialise_variables as stp0

#-----------------------#
#--- Start flask app ---#
#-----------------------#

app = Flask(__name__)
app.config["DEBUG"] = True

#-----------------------------------#
#--- Initialise global variables ---#
#-----------------------------------#
#We use global variables

#Get list of all 5 letter words
all_words,n_words=oth.get_all_five_letter_words(english_words_lower_alpha_set)

#------------------------#
#--- Page 0: Homepage ---#
#------------------------#

@app.route("/", methods=["GET", "POST"])
@app.route("/home/<reset>", methods=["GET", "POST"])
def wordle_homepage(reset="yes"):
    
    #If starting or re-starting
    #if request.method==None or request.method == "GET":
    if reset=="yes":
        
        error_message=""
        
    #----------------------------------#
    #--- Page 1: Process user input ---#
    #----------------------------------#

    elif request.method == "POST":
        
        #Initialise method variable e.g. random, rank, brute_force_simple etc.
        accepted_methods=["random","rank","brute_force_simple"] #Initialise list for checking input
        method = None
        
        #Get input for method variable
        method = request.form["methodinput"].lower()

        #Check that method variable is from accepted list
        if method not in accepted_methods:
            error_message = "Method not accepted. Try again."
            
        #Else, complete calculation
        elif method in accepted_methods:
            
            #Ensure relevant variables are global
            global all_words,n_words
            global all_words_remaining,n_words_remaining,all_possible_letters_remaining,count
            global next_word_selection,rag_colours,tile_colours,remove_trial_word
            global trial_word,previous_trial_word
            
            #Initialise global variables
            all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
            next_word_selection=""
            rag_colours=""
            tile_colours=""
            remove_trial_word="no"
            trial_word=""
            previous_trial_word=""
            
            #Initialise local variables
            mode="real_flask"
            next_word_selection=method
            
            #Get trial wor
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)
            
            #Go to rag score page
            return redirect("/find_word/no", code=301)
            
    #Return homepage
    return render_template('home_page_with_formatting.html', error_message=error_message)

#--------------------------------------#
#--- Page 3: Input RAG scores pages ---#
#--------------------------------------#

@app.route("/find_word/<remove_trial_word>", methods=["GET", "POST"])
def wordle_solver(remove_trial_word="no"):
    
    #Ensure relevant variables are global
    global all_words,n_words
    global all_words_remaining,n_words_remaining,all_possible_letters_remaining,count
    global next_word_selection,rag_colours,tile_colours
    global trial_word,previous_trial_word
    
    #Initialise variables
    error_message = "" #Initialise error string for printing error if needed
    accepted_colours=["Green","Orange","Red"] #Initialise list for checking input
    possible_words="All words currently available."
    
    #If trial word not accepted, we need to bin it and get the next best word
    if remove_trial_word=="yes":
        
        #Remove word
        all_words_remaining.remove(trial_word)
        n_words_remaining=n_words_remaining-1
        
        #Get next trial word
        mode="real_flask"
        trial_word=previous_trial_word
        trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                        next_word_selection,
                                                                                                        rag_colours,
                                                                                                        trial_word,
                                                                                                        all_words_remaining,
                                                                                                        n_words_remaining,
                                                                                                        all_possible_letters_remaining,
                                                                                                        remove_trial_word)
        
        #Output error message if error
        if error_flag==1:
            error_message=error_message
            
        #Get possible words as string
        possible_words=""
        for word in all_words_remaining:
            possible_words=word+", "+possible_words
        
        #Reset trial word flag
        remove_trial_word="no"
    
    #-------------------------------------------------#
    #--- Process user input if we have rag colours ---#
    #-------------------------------------------------#
    elif remove_trial_word=="no" and rag_colours!="":
        
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
            
            #Save previous trial word before generating new trial word
            previous_trial_word=trial_word
            
            #Get first trial word
            mode="real_flask"
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)
            
            #Output error message if error
            if error_flag==1:
                errors=error_message
                
            #Get possible words as string
            possible_words=""
            for word in all_words_remaining:
                possible_words=word+", "+possible_words
            
    #----------------------#
    #--- Output webpage ---#
    #----------------------#
    #If still no rag colours, initialise to red all
    if rag_colours=="":
        rag_colours=["Red","Red","Red","Red","Red"]
    return render_template('rag_input_page.html',
                           error_message=error_message,
                           possible_words=possible_words,
                           trial_word=trial_word,
                           n_words_remaining=n_words_remaining)





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