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

from flask import Flask, request, render_template, jsonify
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

#Initialise various variables for "find_word" function
all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
next_word_selection=""
rag_colours=""
tile_colours="no tile colours recorded yet!"

#------------------------#
#--- Page 0: Homepage ---#
#------------------------#

@app.route("/", methods=["GET", "POST"])
def wordle_homepage():
    
    #Initialise variables
    errors = "" #Initialise error string for printing error if needed
    
    #Ensure relevant variables are global
    global all_words,n_words,all_words_remaining,n_words_remaining,all_possible_letters_remaining,count,next_word_selection,rag_colours

    #Reset global variables if re-starting
    if n_words_remaining<n_words:
        all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
        next_word_selection=""
        rag_colours=""
        
    #----------------------------------#
    #--- Page 1: Process user input ---#
    #----------------------------------#

    if request.method == "POST":
        
        #Initialise method variable e.g. random, rank, brute_force_simple etc.
        accepted_methods=["random","rank","brute_force_simple"] #Initialise list for checking input
        method = None
        
        #Get input for method variable
        method = request.form["methodinput"].lower()
        
        #Check that method variable is from accepted list
        input_flag=0
        if method not in accepted_methods:
            input_flag=1
        
        #If not accepted, output error
        if input_flag==1:
            errors += "Method not accepted. Try again.\n"
        
        #Else, complete calculation
        elif input_flag==0:
            
            #Get first trial word
            mode="real_flask"
            next_word_selection=method
            rag_colours=None
            trial_word=None
            remove_trial_word="No"
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining,error_flag,error_message=find_word_flask(mode,
                                                                                                            next_word_selection,
                                                                                                            rag_colours,
                                                                                                            trial_word,
                                                                                                            all_words_remaining,
                                                                                                            n_words_remaining,
                                                                                                            all_possible_letters_remaining,
                                                                                                            remove_trial_word)
            
            #Return first trial word
            return render_template('first_trial_word_page.html', trial_word=trial_word,remove_trial_word="No",previous_trial_word=trial_word)
    
    #Return homepage
    return render_template('home_page_with_formatting.html', errors=errors)

#--------------------------------------#
#--- Page 3: Input RAG scores pages ---#
#--------------------------------------#

@app.route("/<trial_word>/<remove_trial_word>/<previous_trial_word>", methods=["GET", "POST"])
@app.route("/<trial_word>", methods=["GET", "POST"])
def wordle_solver(trial_word="atest",remove_trial_word="No",previous_trial_word="atest"):
    
    #Initialise variables
    errors = "" #Initialise error string for printing error if needed
    accepted_colours=["Green","Orange","Red"] #Initialise list for checking input
    possible_words="Too many words to currently list."
    
    #Ensure relevant variables are global
    global all_words,n_words,all_words_remaining,n_words_remaining,all_possible_letters_remaining,count,next_word_selection,rag_colours
    
    # If the remove button was pressed, set this flag
    try:
        button = request.form['button']
    except:
        button = "button"
        
    if button=="Trial word not accepted. Generate next best trial word.":
        remove_trial_word="Yes"
    
    #If trial word not accepted, we need to bin it and get the next best word
    if remove_trial_word=="Yes":
        
        #Remove word
        all_words_remaining.remove(trial_word)
        n_words_remaining=n_words_remaining-1
        
        #Get next trial word
        mode="real_flask"
        trial_word=copy.deepcopy(previous_trial_word)
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
        
        #Reset trial word flag
        remove_trial_word="No"
    
    #--------------------------#
    #--- Process user input ---#
    #--------------------------#
    elif request.method == "POST" and remove_trial_word=="No":
        
        #Check that variables are accepted
        input_flag=0
        for colour in rag_colours:
            if colour not in accepted_colours:
                input_flag=1
        
        #If one or more variables are not accepted, output error
        if input_flag==1:
            errors += "<p>At least one input is not accepted. Try again.</p>\n"
        
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
            
    return render_template('rag_input_page.html', errors=errors,possible_words=possible_words,trial_word=trial_word,n_words_remaining=n_words_remaining,remove_trial_word_no="No",remove_trial_word_yes="Yes",previous_trial_word=previous_trial_word)

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