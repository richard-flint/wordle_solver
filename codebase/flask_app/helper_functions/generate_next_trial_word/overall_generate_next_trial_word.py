#Import
from helper_functions.generate_next_trial_word import option_1_random_guess as stp1_1
from helper_functions.generate_next_trial_word import option_2_most_frequent_letter as stp1_2
from helper_functions.generate_next_trial_word import option_3_brute_force as stp1_3
from helper_functions.generate_next_trial_word.option_5_chatbot import chatbot as stp1_5

#Generate next trial word
def generate_next_trial_word(WordleGameParameters,ThisWordleRound,AllWordleRounds):
    
    #Option 1: Generate trail word at random
    if WordleGameParameters.method=="random":
        ThisWordleRound=stp1_1.generate_random_trial_word(ThisWordleRound)

    #Option 2: Generate trial word by finding word whose letters appear in the most amount of other words 
    elif WordleGameParameters.method=="rank":
        ThisWordleRound=stp1_2.generate_word_from_most_frequent_remaining_letters(ThisWordleRound)

    #Option 3: Brute force
    elif (WordleGameParameters.method=="brute_force_simple" or WordleGameParameters.method=="brute_force_extended"):
        ThisWordleRound=stp1_3.generate_word_using_brute_force(WordleGameParameters,ThisWordleRound)
        
    #Option 4: Reinforcement learning
        
    #Option 5: Chatbot
    elif (WordleGameParameters.method=="chatbot_easy" or WordleGameParameters.method=="chatbot_hard"):
        ThisWordleRound=stp1_5.generate_word_using_chatbot(WordleGameParameters,ThisWordleRound,AllWordleRounds)
        
    return ThisWordleRound