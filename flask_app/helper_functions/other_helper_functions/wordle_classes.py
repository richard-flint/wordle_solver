class WordleRound:
    def __init__(self,
                 n_previous_guesses,
                 previous_trial_word,
                 previous_rag_score,
                 n_words_remaining,
                 remaining_words,
                 remaining_letters,
                 round_number,
                 trial_word,
                 error,
                 error_message):
        
        self.n_previous_guesses = n_previous_guesses
        self.previous_trial_word = previous_trial_word
        self.previous_rag_score = previous_rag_score
        self.n_words_remaining = n_words_remaining
        self.remaining_words = remaining_words
        self.remaining_letters = remaining_letters
        self.round_number = round_number
        self.trial_word = trial_word
        self.error = error
        self.error_message = error_message
        
class WordleGame:
    def __init__(self,
                 all_words,
                 n_words,
                 method,
                 mode):
        
        self.all_words = all_words
        self.n_words = n_words
        self.method = method
        self.mode = mode