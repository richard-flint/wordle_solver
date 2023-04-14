from helper_functions.generate_next_trial_word.option_5_chatbot.openai_api_key import private_openai_api_key
from helper_functions.generate_next_trial_word.option_5_chatbot.messages import *
import os
import openai

def generate_word_using_chatbot(WordleGameParameters,ThisWordleRound,AllWordleRounds):
    
    #Get API key
    openai.api_key = private_openai_api_key
    
    #Initialise error checks
    error=0
    error_message=""
    check_word=0
    count=0
    all_guesses=[]
    
    #Get list of possible words for checking output
    if ThisWordleRound.round_number==1:
        all_possible_words=ThisWordleRound.remaining_words
    else:
        all_possible_words=AllWordleRounds["round_1"].remaining_words
    
    #*******************#
    #*** First round ***#
    #*******************#
    
    #Check if this is the first round
    if ThisWordleRound.round_number==1:
        
        #Get initial message
        message=initial_message
        
        #Loop until we get valid word (up to a limit!)
        while check_word==0 and count<10:
        
            #If first round, generate guess
            guess=get_chatbot_next_guess(message)

            #Check guess is from list of possible words
            if guess in all_possible_words:
                
                #If yes, we can exit
                check_word=1
            
            #Else generate an additional message to help steer model
            else:
                all_guesses.append(guess)
                additional_message_1="You have previously tried the following words, but they have been rejected as invalid words: "
                additional_message_2=str(all_guesses).replace("[","").replace("]","")
                additional_message_3="Remember, words must be five letters, and cannot be proper nouns or plural nouns. Please generate another guess."
                additional_message_all=additional_message_1+additional_message_2+additional_message_3
                message=initial_message+additional_message_all
                
                #Add one onto count
                count+=1
                
        #If we got to 10 counts, then return error
        if count==10:
            error=1
            error_message="Chatbot could not find initial valid word with 10 guesses. These guesses were: "+additional_message_2
            
    #*****************#
    #*** 2+ rounds ***#
    #*****************#
    elif ThisWordleRound.round_number>1:
        
        #*** Generate initial message ***#
        
        #Initialise string for previous guesses and rag words
        message_previous_guesses_rag_scores=""
        
        #Get previous guesses and rag scores and convert to strings for promt message
        if "round_2" in AllWordleRounds.keys(): #Only worth doing if there's at least round_2 saved
            for specific_round in AllWordleRounds.keys():
                if specific_round!="round_1":   #Round_1 does not have a rag score
                    previous_guess=AllWordleRounds[specific_round].previous_trial_word
                    previous_rag_score=str(AllWordleRounds[specific_round].previous_rag_score).replace("[","").replace("]","")
                    previous_rag_score=previous_rag_score.lower().replace("red","grey")

                    #Add to string
                    message_previous_guesses_rag_scores+="Guess: "+previous_guess+". Feedback for this guess: "+previous_rag_score+". "
                        
        #Add guess and rag score from this round
        previous_guess=ThisWordleRound.previous_trial_word
        previous_rag_score=str(ThisWordleRound.previous_rag_score).replace("[","").replace("]","")
        message_previous_guesses_rag_scores+="Guess: "+previous_guess+". Feedback for this guess: "+previous_rag_score+". "
        
        #*** Generate full message ***#
        
        #The easy version also provides a list of possible remaining words
        if WordleGameParameters.method=="chatbot_easy":
            message=(intro_message+subsequent_message_1+message_previous_guesses_rag_scores+subsequent_message_2_easy+
                    str(ThisWordleRound.remaining_words).replace("[","").replace("]","")+". "+subsequent_message_3_easy)

        #The harder version does not provide the chatbot with the list of remaining possible words
        elif WordleGameParameters.method=="chatbot_hard":
            message=intro_message+subsequent_message_1+message_previous_guesses_rag_scores+subsequent_message_3_hard
            
        #*** Get next guess ***#
        
        #Loop until we get valid word (up to a limit!)
        while check_word==0 and count<10:
        
            #Generate guess
            guess=get_chatbot_next_guess(message)

            #Check guess is from list of available words
            if guess in all_possible_words:
                
                #If yes, we can exit
                check_word=1
            
            #Else generate an additional message to help steer model
            else:
                all_guesses.append(guess)
                additional_message_1="You have previously tried the following words, but they have been rejected as invalid words: "
                additional_message_2=str(all_guesses).replace("[","").replace("]","")
                additional_message_3="Remember, words must be five letters, and cannot be proper nouns or plural nouns.Please generate another guess, and please wrap words in an <output> xml tag."
                additional_message_all=additional_message_1+additional_message_2+additional_message_3
                message=initial_message+additional_message_all
                
                #Add one onto count
                count+=1
                
        #If we got to 10 counts, then return error
        if count==10:
            error=1
            error_message="Chatbot could not find initial valid word with 10 guesses. These guesses were: "+additional_message_2
    
    #*********************#
    #*** Return values ***#
    #*********************#
    
    #Guess
    if error==1:
        ThisWordleRound.trial_word="error"
    elif error==0:
        ThisWordleRound.trial_word=guess
        
    #Error messages
    ThisWordleRound.error=error
    ThisWordleRound.error_message=error_message
        
    return ThisWordleRound
    
def get_chatbot_next_guess(message):
    
    #Pre-process message
    message=message.replace("\n","")

    #Get first guess
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0.2,
      messages=[
        {"role": "user", "content": message}
      ]
    )

    #Get output as variable
    chatgpt_api_output=str(completion.choices[0].message["content"])

    #Print output
    #print(chatgpt_api_output)
    
    #Extract guess from output
    start_index=chatgpt_api_output.find("<output>")
    
    #Check if there is a space after xml tag
    if chatgpt_api_output[start_index+8:start_index+9]==" ":
        guess=chatgpt_api_output[start_index+9:start_index+9+5]
        
    elif chatgpt_api_output[start_index+8:start_index+9]==">":
        guess=chatgpt_api_output[start_index+9:start_index+9+5]
        
    else:
        guess=chatgpt_api_output[start_index+8:start_index+8+5]
        
    #Print guess
    #print(guess)
        
    return guess