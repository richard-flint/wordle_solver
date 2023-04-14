#Define initial messages
intro_message='''there is an online game called wordle. the aim of wordle is to find a five-letter word using as few guesses as possible. the correct five-letter word changes every day, so there is a new word to guess each day. to find the correct word, users input five-letter words as guesses, and the game provides feedback in the form of colours for each letter. these colours help the user to narrow down and prioritise future guesses.

the available colours are green, orange and grey. a green letter means that a given letter in the user's guess is correct. this means that this letter appears in the final word  in the same location. an orange letter in the user's guess means that this letter appears in the final word, but it is currently in the wrong location in the user's guess. a grey letter means that a given letter in the user's guess does not appear in the final word. 

for example, if the word of the day is "apple" and a user guesses "plate", then the feedback would be "orange", "orange", "orange", "grey", "green". this is because the "p", "l" and "a" in the user's guess "plate" all appear in the final word "apple", but in different positions in the word, so they are given an  "orange" feedback. the "t" in the user's guess "plate" does not appear in the final word "apple", so this letter is given a "grey" feedback. the "e" in the user's guess "plate" is given a "green" feedback, because the letter "e" appears in the exact same location in the final word "apple".

there is a slight nuance to the rules for repeated letters. more specifically, if a user's guess has a repeated letter, and the number of times that this letter appears in the user's guess is greater than the number of times that the same letter appears in the final word, then the letter will only receive either "green" or "orange" up to the number of occurences in the final word. any additional occurrences will be colored "grey".

for example, if the final word is "plumb" and a user guesses the word "apple", then the feedback would be "grey", "orange", "grey", "orange", "grey". the first "p" in "apple" receives an "orange" feedback, because the letter "p" occurs in "plumb" in a different location. however, the second "p" in "apple" receives a "grey" feedback, because there is only one "p" in the final word "plumb".

when generating new guesses, an effective strategy should aim to select a word that reduces the total remaining uncertainty in the game by the greatest amount. the most basic measure for uncertainty in the game is the number of remaining possible word. if this is used as a proxy for uncertainty, an effective strategy would aim to select a word that narrows down the list of remaining possible words by the greatest amount. in other words, the most effective guess would produce the shortest list of possible remaining words for the following guess.'''

start_prompt='''we are now going to play wordle. to start, you can guess any five letter word. given the above description of an effective strategy, what word do you select?

you have to select one word only, and please place your final selection between <output> xml tags. for example, if you select the word "petal" as the next guess, then output this as <output>petal</output>.'''

initial_message=intro_message+start_prompt

#Define subsequent messages
subsequent_message_1='''We are currently in the middle of playing wordle. So far, we have made the following guesses, and received the following feedback. '''

#Option "easy" will include an updated list of remaining possible words
subsequent_message_2_easy='''Based on these guesses and the corresponding feedback, we can work out that the correct word must be one of the following remaining possible words:'''

subsequent_message_3_easy='''Given your understanding of Wordle and of an effective Wordle strategy, and given the previous guesses, feedback, and list of remaining possible words, please provide the best next guess for the Wordle game. you have to select one word only, and this word should be from the above list of remaining possible words. please place your final selection between <output> xml tags. for example, if you select the word "petal" as the next guess, then output this as <output>petal</output>.'''

#Option "hard" will NOT include an updated list of remaining possible words, and so more closely resembles a human playing the game

subsequent_message_3_hard='''Given your understanding of Wordle and of an effective Wordle strategy, and given the previous guesses and feedback, please provide the best next guess for the Wordle game . you have to select one word only, and please place your final selection between <output> xml tags. for example, if you select the word "petal" as the next guess, then output this as <output>petal</output>.'''