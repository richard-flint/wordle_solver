def find_word_loop_function(all_words,true_word,next_word_selection,mode,rag_colours,all_words_remaining,n_words_remaining,all_possible_letters_remaining,count):
    
    #------------------------------#
    #--- Step 1: Generate guess ---#
    #------------------------------#

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

    #-----------------------------------------------#
    #--- Step 2: Compare guess against true word ---#
    #-----------------------------------------------#
    #This assigns "green", "amber" or "red" for each letter in the trial word compared...
    #...to the true word

    #If we are in "real" mode, this is done by the user
    if mode=="real":
        rag_score=stp2.check_letters_manually()

    elif mode=="real_web_app":
        rag_score=copy.deepcopy(rag_colours)

    #If we are not in "real" mode, this is done automatically
    elif mode!="real":
        rag_score=stp2.check_letters_automatically(true_word,trial_word)

    #-----------------------------------------------------------------#
    #--- Step 3: Generate updated list of remaining possible words ---#
    #-----------------------------------------------------------------#
    all_words_remaining,all_possible_letters_remaining=stp3.get_remaining_words(all_words_remaining,
                                                                                all_possible_letters_remaining,
                                                                                rag_score,
                                                                                trial_word)

    #Return number of words in update list if running in "real" mode
    if mode == "real":
        print("Number of possible words remaining: ",len(all_words_remaining))

    #-----------------------------------------#
    #--- Step 4: Update tracking variables ---#
    #-----------------------------------------#

    #Get number of remaining words
    n_words_remaining=len(all_words_remaining)

    #Add one to i for tracking number of loops
    count+=1
    
    return all_words_remaining,n_words_remaining,all_possible_letters_remaining,count