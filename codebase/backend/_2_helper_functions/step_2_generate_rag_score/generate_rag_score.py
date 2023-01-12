#---------------------#
#--- Check letters ---#
#---------------------#
#This function compares a trial word against the actual word, and returns a
#RAG rating for each letter using the following (standard Wordle) definitions:
#--- "Green"  = trial letter is the same as true letter
#--- "Orange" = trial letter appears at least once in true word, but not in the
#               current position in the trial word
#--- "Red"    = trial letter does not appear in true word

#The function returns a list of words that correspond to five 
#RAG ratings, one for each letter

def check_letters_automatically(true_word,trial_word):
    
    #Initialise score list
    true_word_letters=[]
    trial_word_letters=[]
    all_scores=[]
    
    #Get lists of letters
    for i in range(5):
        true_word_letters.append(true_word[i])
        trial_word_letters.append(trial_word[i])
        
    #Get rag score for each letter in trial word
    for i in range(5):
        if trial_word_letters[i]==true_word_letters[i]:
            all_scores.append("Green")
        elif trial_word_letters[i] in true_word_letters:
            all_scores.append("Orange")
        else:
            all_scores.append("Red")
            
    #Return final value
    return all_scores

def check_letters_manually():

    #Create lists for checking user input
    accepted_colours=["Green","Orange","Red"]
    accepted_yes_no=["yes","y","no","n"]

    #Create list for iterating
    position_list=["first","second","third","fourth","fifth"]
    
    #Run loop until all inputs are satisfied
    while True:
        
        #Set flags
        result=0
        result_2=0
        result_3=0
        check_lowercase="no"

        #Initialise score list
        all_scores=[]

        #Loop over all positions
        for position in position_list:

            #Loop until we receive an acceptable answer
            while result==0:

                #Get colour
                input_string=f"What is the colour of the {position} letter? [OPTIONS: Green, Orange, Red]"
                colour=input(input_string)

                #Make lowercase with capitalised first letter
                colour_lowercase=colour.capitalize()
                
                #Map single letters to words
                if colour_lowercase=="G":
                    colour_lowercase ="Green"
                elif colour_lowercase=="O":
                    colour_lowercase ="Orange"
                elif colour_lowercase=="R":
                    colour_lowercase ="Red"

                #Check that the colour is acceptable
                result=accepted_colours.count(colour_lowercase)

                #If result is not accepted, output error message and ask user to re-enter
                if result==0:
                    print("Input not accepted. Please re-enter with accepted input.")

            #Save answer
            all_scores.append(colour_lowercase)

            #Reset "result" flag
            result=0

        #Print final list
        print("Your final list is: ",all_scores)

        #Check if user is happy with final result
        while result_2==0:

            #Get input
            check=input("Do you want to proceed? [Options: Yes, No]")
            check_lowercase=check.lower()

            #Check if input is acceptable
            result_2=accepted_yes_no.count(check_lowercase)

            #If input is not acceptable, output error message and ask to re-enter
            if result_2==0:
                print("Input not accepted. Please re-enter with accepted input.")
                
        #Reset flag
        result_2=0

        #If happy, return final value
        if check_lowercase == "yes" or check_lowercase == "y":
            return all_scores

        #If not happy, double check
        elif check_lowercase == "no" or check_lowercase == "n":
            
            #Loop until we receive accepted input
            while result_3==0:

                #Get double check input
                double_check=input("You have selected 'No', which suggests you want to re-enter your colours. Are you sure you want to re-enter your colours? If you enter 'Yes', this will delete all your previous inputs, and you will be required to re-enter colours for positions 1 to 5. If you enter 'No', this will accept your existing input and proceed to the next stage of the wordle solver.")
                double_check_lowercase=double_check.lower()

                #Check if input is acceptable
                result_3=accepted_yes_no.count(double_check_lowercase)

                if result_3==0:
                    print("Input not accepted. Please re-enter with accepted input.")

            #Reset flag
            result_3=0
            
            #If happy, return final value
            if double_check_lowercase == "no" or double_check_lowercase == "n":
                return all_scores

            #If not happy, the function will loop back to the start