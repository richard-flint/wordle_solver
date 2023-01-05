#App lifted largely from tutorial here: https://blog.pythonanywhere.com/169/#step-3-make-the-processing-code-available-to-the-web-app

#Next steps:
# - Create a version of the wordle solver that can integrate with this app.

from flask import Flask, request

from english_words import english_words_set
from english_words import english_words_lower_alpha_set

from helper_functions.other_helper_functions import other_helper_functions as oth
from helper_functions.step_0_initialise_variables import initialise_variables as stp0
from flask_backend import run_wordle_solver_flask

app = Flask(__name__)
app.config["DEBUG"] = True

#-----------------------------------#
#--- Initialise global variables ---#
#-----------------------------------#

#Get list of all 5 letter words
all_words,n_words=oth.get_all_five_letter_words(english_words_lower_alpha_set)

#Initialise dictionary for saving results if doesn't already exist
if "n_guesses_dict" not in locals():
    n_guesses_dict=dict()

#Initialise various variables for "find_word" function
all_words_remaining,n_words_remaining,all_possible_letters_remaining,count=stp0.initialise_variables(all_words)
next_word_selection="rank"
my_count=0

#----------------#
#--- Homepage ---#
#----------------#

@app.route("/", methods=["GET", "POST"])
def wordle_homepage():
    
    #Initialise variables
    errors = "" #Initialise error string for printing error if needed
    accepted_methods=["random","rank"] #Initialise list for checking input
    
    #If using post method (which we are when submitting inputs via a form)
    if request.method == "POST":
        
        #Initialise method variable
        method = None
        
        #Get inputs
        method = request.form["methodinput"].lower()
        
        #Check that method variable is accepted
        input_flag=0
        if method not in accepted_methods:
            input_flag=1
        
        #If not accepted, output error
        if input_flag==1:
            errors += "<p>Method not accepted. Try again.</p>\n"
        
        #Else, complete calculation
        elif input_flag==0:
            
            #Ensure relevant variables are global
            global all_words_remaining,n_words_remaining,all_possible_letters_remaining,next_word_selection
            
            #Get first trial word
            mode="real_flask"
            next_word_selection=method
            rag_colours=None
            trial_word=None
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining=run_wordle_solver_flask(mode,
                                                                                                                    next_word_selection,
                                                                                                                    rag_colours,
                                                                                                                    trial_word,
                                                                                                                    all_words_remaining,
                                                                                                                    n_words_remaining,
                                                                                                                    all_possible_letters_remaining)
            #trial_word="hello"
            
            #Return first trial word
            return '''
                <html>
                    <body>
                        <p>The suggested trial word is: {trial_word}</p>
                        <p><a href="/{trial_word}">Click here to input RAG scores for this trial word</a>
                    </body>
                </html>
            '''.format(trial_word=trial_word)
        
    return '''
        <html>
            <body>
                {errors}
                <p>Welcome to the Wordle Solver</p>
                <p>Enter your method [Options: random, rank]:</p>
                <form method="post" action=".">
                    <p><input name="methodinput" /></p>
                    <p><input type="submit" value="Get first trial word" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

@app.route("/<trial_word>", methods=["GET", "POST"])
def wordle_solver(trial_word):
    
    #Initialise variables
    errors = "" #Initialise error string for printing error if needed
    accepted_colours=["Green","Orange","Red"] #Initialise list for checking input
    
    #If using post method (which we are when submitting inputs via a form)
    if request.method == "POST":
        
        #Initialise colour variables
        colour1 = None
        colour2 = None
        colour3 = None
        colour4 = None
        colour5 = None
        
        #Get inputs
        colour1 = request.form["colour1input"].capitalize()
        colour2 = request.form["colour2input"].capitalize()
        colour3 = request.form["colour3input"].capitalize()
        colour4 = request.form["colour4input"].capitalize()
        colour5 = request.form["colour5input"].capitalize()
        rag_colours=[colour1,colour2,colour3,colour4,colour5]
        
        #Check that variables are accepted
        input_flag=0
        for colour in rag_colours:
            if colour not in accepted_colours:
                input_flag=1
        
        #If one or more variables are not accepted, output error
        if input_flag==1:
            errors += "<p>At least one input is not accepted. Try again.</p>\n"
        
        #Else, complete calculation
        elif input_flag==0:
            
            #------------------------#
            #------------------------#
            #--- Calculate result ---#
            #------------------------#
            #------------------------#
            
            #Ensure relevant variables are global
            global all_words_remaining,n_words_remaining,all_possible_letters_remaining,next_word_selection,my_count
            
            #Get first trial word
            mode="real_flask"
            trial_word,all_words_remaining,n_words_remaining,all_possible_letters_remaining=run_wordle_solver_flask(mode,
                                                                                                                    next_word_selection,
                                                                                                                    rag_colours,
                                                                                                                    trial_word,
                                                                                                                    all_words_remaining,
                                                                                                                    n_words_remaining,
                                                                                                                    all_possible_letters_remaining)
            #my_count+=1
            #trial_word="hello "+str(my_count)
            
    return '''
        <html>
            <body>
                {errors}
                <p>The next guess is: {trial_word}</p>
                <p>Enter your colours:</p>
                <form method="post" action="/{trial_word}">
                    <p><input name="colour1input" /></p>
                    <p><input name="colour2input" /></p>
                    <p><input name="colour3input" /></p>
                    <p><input name="colour4input" /></p>
                    <p><input name="colour5input" /></p>
                    <p><input type="submit" value="Get next Wordle guess" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors,trial_word=trial_word)

if __name__ == '__main__':
  app.run()