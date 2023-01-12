#-------------------------------------------------------------------------#
#----------------------- Initialise variables ----------------------------#
#-------------------------------------------------------------------------#
#This function just initialises a few variables that are used elsewhere,
#as it's a bit neater to do this initialisation in a separate function

def initialise_variables(all_words):
    
    #Generate list of all possible letters for each letter in word
    alphabet=list(["a","b","c","d","e","f","g",
                   "h","i","j","k","l","m","n",
                   "o","p","q","r","s","t","u",
                   "v","w","x","y","z"])
    
    all_possible_letters=dict(column_0=alphabet.copy(),
                              column_1=alphabet.copy(), 
                              column_2=alphabet.copy(),
                              column_3=alphabet.copy(),
                              column_4=alphabet.copy())
    
    #Initialise list of remaining possible words
    all_words_remaining=all_words.copy()
    
    #Initialise variable for counting the number remaining words
    n_words_remaining=len(all_words_remaining)
    
    #Initialise i for tracking number of loops
    i=0
    
    #Return variables
    return all_words_remaining,n_words_remaining,all_possible_letters,i