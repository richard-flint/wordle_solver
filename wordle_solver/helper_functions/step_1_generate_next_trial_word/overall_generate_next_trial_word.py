from helper_functions.step_1_generate_next_trial_word import option_1_random_guess as stp1_1
from helper_functions.step_1_generate_next_trial_word import option_2_most_frequent_letter as stp1_2
from helper_functions.step_1_generate_next_trial_word import option_3_brute_force as stp1_3

def generate_next_trial_word(next_word_selection,all_words_remaining,n_words_remaining,all_possible_letters_remaining,mode):

    #Option 1: Generate trail word at random
    if next_word_selection=="random":
        trial_word=stp1_1.generate_random_trial_word(all_words_remaining)

    #Option 2: Generate trial word by finding word whose letters appear in the most amount of other words 
    elif next_word_selection=="rank":
        trial_word=stp1_2.generate_word_from_most_frequent_remaining_letters(all_words_remaining,
                                                                             n_words_remaining,
                                                                             all_possible_letters_remaining)

    #Option 3: Brute force
    elif (next_word_selection=="brute_force_simple" or next_word_selection=="brute_force_extended"):
        trial_word=stp1_3.generate_word_using_brute_force(next_word_selection,all_words_remaining,n_words_remaining,all_possible_letters_remaining,mode)

    #Print trial word
    #If mode=="real" (i.e. we are running the wordle solver for real), we need to print out the next
    #word selection so that the user can input this into their app.
    if mode=="real":
        print("\nThe next guess is: ",trial_word)
        
    return trial_word