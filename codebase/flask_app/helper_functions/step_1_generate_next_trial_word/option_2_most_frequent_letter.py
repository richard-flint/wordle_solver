#-----------------------------------------------------------------#
#--- Step 1 Option 2: Generate word from most frequent letters ---#
#-----------------------------------------------------------------#

#*** Algorithm steps ***#

#This function generates the next guess through the following algorithm:
#--- 1.From the list of remaining possible words, find the frequency that each
#      letter in the alphabet appears in each column i.e. for column 0, how many
#      times do the letters "a-z" appear across the full list of remaining words?
#      And then same for columns 1 to 4.
#--- 2.Rank the occurances of each letter for each column i.e. for column 0,
#      rank the letters "a-z", with the most frequently occuring letter receiving
#      the highest rank (26), and the least frequently occuring letter receiving
#      the lowest rank (1). Repeate for columns 1 to 4.
#--- 3.Assign a score for each remaining word based on the rank of each letter e.g.
#    for the word "swamp", each letter "s", "w", "a", "m" and "p" is assigned a 
#    score based on the rank of the letter in its associated column.
#--- 4.Add up the scores for each letter in each word to get a total score for
#    each word.
#--- 5.Find the word with the highest score - this is the next guess.

#*** Rationale for this algorithm***#

#By finding words whose letters occur frequently in other words in the list, we
#are able to get more "information" about the remaining lists e.g. if a letter occurs
#at a high frequency in the list of remaining words, and we test that letter and
#receive a "red" score, then this will remove a comparatively large number of words,
#and thus reduce the list of remaining possible words at a faster rate.

#*** Ideas for modifications/extensions ***#

# - At present, we use the rank as the score, but we could also use the letter frequency.
#   By using the rank, we lose some information compared to frequency, although it does
#   even the weighting all 5 columns.

#Import libraries
import numpy as np

#Define function
def generate_word_from_most_frequent_remaining_letters(all_words_remaining,
                                                       n_words_remaining,
                                                       all_possible_letters_remaining):
    
    #Initialise alphabet list                
    alphabet=list(["a","b","c","d","e","f","g",
                   "h","i","j","k","l","m","n",
                   "o","p","q","r","s","t","u",
                   "v","w","x","y","z"])
    
    #Initialise matrix for counting the occurance of each letter in each column
    letter_count_all_letters_all_columns=np.zeros([len(alphabet),5])
    
    #Create matrix of letters for all words remaining
    all_words_remaining_as_letter_matrix=np.zeros([n_words_remaining,5],dtype="U1")
    for i in range(n_words_remaining):
        for j in range(5):
            word=all_words_remaining[i]
            all_words_remaining_as_letter_matrix[i,j]=word[j]

    #--- For each column in the remaining list of words, calculate the occurance of each letter ---#
    for j in range(5):
        for i in range(len(alphabet)):
            letter=alphabet[i]
            letter_count=np.sum(all_words_remaining_as_letter_matrix[:,j]==letter)
            letter_count_all_letters_all_columns[i,j]=letter_count
            
    #--- Rank occurances of each letter in each column ---#

    #Initialise rank matrix
    rank_matrix=np.zeros([len(alphabet),5])

    #Rank letter occurances in each column
    for j in range(5):
        rank_vector=letter_count_all_letters_all_columns[:,j].argsort()
        rank_matrix[:,j]=np.copy(rank_vector)
    
    #--- Find the word with the highest overall score ---#

    #Initialise rank matrix for each letter in each word
    rank_matrix_all_letters_all_words=np.zeros([np.shape(all_words_remaining_as_letter_matrix)[0],
                                                np.shape(all_words_remaining_as_letter_matrix)[1]])

    #Find rank of each letter in each word
    for j in range(5):
        for i in range(n_words_remaining):

            #Get letter in word
            letter=all_words_remaining[i][j]

            #Find position of letter in alphabet
            letter_position= (np.array(alphabet)==letter)

            #Find rank of letter in column
            letter_rank=rank_matrix[:,j][letter_position]

            #Save rank
            rank_matrix_all_letters_all_words[i,j]=letter_rank[0]

    #Create score for each word by adding up rank of each letter
    score_each_word=np.sum(rank_matrix_all_letters_all_words,axis=1)

    #Find max score
    max_score=max(score_each_word)

    #Find position of max scoring word
    for i in range(n_words_remaining):
        if score_each_word[i]==max_score:
            max_score_position=i

    #Find max scoring word
    max_score_word=all_words_remaining[max_score_position]
    
    #Return max scoring word
    return max_score_word