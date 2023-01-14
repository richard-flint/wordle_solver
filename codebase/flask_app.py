#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#------------------------------------- Flask App ---------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#

#--- Run locally ---#
#To run on a local machine, navigate to the relevant folder in the terminal and use the command: python flask_app.py
#To navigate, use "cd .\OneDrive\Documents\GitHub\wordle_solver\codebase\"

#Next steps:
# - Create a version of the wordle solver that can integrate with this app.

#---------------#
#--- Imports ---#
#---------------#

from flask import Flask, request, render_template, jsonify, redirect
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
reset=1

#------------------------#
#--- Page 0: Homepage ---#
#------------------------#

@app.route("/", methods=["GET", "POST"])
def wordle_homepage():
    
    #Ensure relevant variables are global
    global all_words,n_words
    global all_words_remaining,n_words_remaining,all_possible_letters_remaining,count
    global next_word_selection,rag_colours,tile_colours,remove_trial_word,error_message,reset
    global trial_word,previous_trial_word
    
    #If starting or re-starting
    #if request.method==None or request.method == "GET":
    if reset==1:
    
        #Initialise global variables
        all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
        next_word_selection=""
        rag_colours=""
        trial_word=""
        tile_colours=""
        remove_trial_word="No"
        error_message = "" #Initialise error string for printing error if needed
        
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
            
            #Get first trial word
            mode="real_flask"
            next_word_selection=method
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)
            
            #Go to rag score page
            print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            return redirect("/find_word")
            
    #Return homepage
    reset=0
    return render_template('home_page_with_formatting.html', error_message=error_message)

#--------------------------------------#
#--- Page 3: Input RAG scores pages ---#
#--------------------------------------#

@app.route("/find_word", methods=["GET", "POST"])
def wordle_solver():
    
    #Ensure relevant variables are global
    global all_words,n_words
    global all_words_remaining,n_words_remaining,all_possible_letters_remaining,count
    global next_word_selection,rag_colours,tile_colours,remove_trial_word,error_message
    global trial_word,previous_trial_word
    
    #Initialise variables
    error_message = "" #Initialise error string for printing error if needed
    accepted_colours=["Green","Orange","Red"] #Initialise list for checking input
    possible_words="Too many words to currently list."
    
    #If trial word not accepted, we need to bin it and get the next best word
    if remove_trial_word=="Yes":
        
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
        remove_trial_word="No"
    
    #-------------------------------------------------#
    #--- Process user input if we have rag colours ---#
    #-------------------------------------------------#
    elif remove_trial_word=="No" and rag_colours!="":
        
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
    
    return render_template('rag_input_page.html', error_message=error_message,possible_words=possible_words,trial_word=trial_word,n_words_remaining=n_words_remaining)





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

#Check if we need to remove word
@app.route('/remove_trial_word_update', methods=['POST'])
def update_remove_trial_word_flag():
    global remove_trial_word
    remove_trial_word = request.get_json()['value']
    return jsonify({'success': True})

#Check if we need to reset wordle solver
@app.route('/update_reset_wordle_solver_flag', methods=['POST'])
def update_reset_flag():
    global reset
    reset=1
    return jsonify({'success': True})

if __name__ == '__main__':
  app.run()