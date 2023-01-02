#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#-------------------------------- Other helper functions -----------------------------------------#
#-------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------#
#This file includes a few additional helper functions that don't fit neatly into Steps 0 to 4, but
#which are nonetheless used in the main algorithm

#Import libraries
import numpy as np
import random

#-----------------------------------------------#
#--- Generate initial list of 5 letter words ---#
#-----------------------------------------------#
#This function generates the original (full) list of five letter words from a longlist of words in
#the English language (the "english_words_lower_alpha_set" set in the "english_words" Python package.

def get_all_five_letter_words(all_words_original_set):

    #Get list of all words
    all_words=list(all_words_original_set)

    #--- Reduce list to 5 letter words ---#

    #Initialise 5 letter word list
    all_five_letter_words=[]

    #Find all 5 letter words
    for word in all_words:
        word_length=len(word)
        if word_length==5:
            all_five_letter_words.append(word)

    #Create matrix of letters
    all_letters=create_letter_matrix_from_word_list(all_five_letter_words)

    #--- Remove words that have characters outside of a-z ---#
    
    #Create copy of original list of words
    all_five_letter_words_a_z_only=all_five_letter_words.copy()

    #Initialise alphabet list
    alphabet=list(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])

    #Count number of 5 letter words
    n_five_letter_words=len(all_five_letter_words)

    #Create copy of all_letters matrix
    all_letters_copy=np.copy(all_letters)

    #Remove any words that have 
    for i in range(n_five_letter_words):

        #Define flag for removing letter
        remove=False

        #Check every letter
        for j in range(5):
            letter=all_letters_copy[i,j]
            if letter not in alphabet:
                remove=True

        #Remove word if letter is not in alphabet
        if remove==True:

            #Get word
            word=all_five_letter_words[i]

            #Remove word from list of 5 letter words
            all_five_letter_words_a_z_only.remove(word)
            
    #Count final number of words in word list
    n_words_final=len(all_five_letter_words_a_z_only)
            
    #Return final list
    return all_five_letter_words_a_z_only, n_words_final

def create_letter_matrix_from_word_list(word_list):
    
    #Initialise matrix
    n_words=len(word_list)
    letter_matrix=np.zeros([n_words,5],dtype="U1")

    #Create matrix of letters
    for i in range(n_words):
        for j in range(5):
            word=word_list[i]
            letter_matrix[i,j]=word[j]
    return letter_matrix

#--------------------------#
#--- Generate true word ---#
#--------------------------#
#This function generates a random "true word", which is then "found" using the wordle solver.
#This is intended to emulate the daily unknown word to real wordle game.

def get_random_true_word(all_words):
    n_words=len(all_words)
    true_word_location=random.randint(0,n_words-1)
    true_word=all_words[true_word_location]
    return true_word