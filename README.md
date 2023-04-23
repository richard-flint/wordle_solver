# Wordle Solver
This is a simple web application that helps users solve the New York Times's daily [Wordle puzzle](https://www.nytimes.com/games/wordle/).

The online version of the web application can be found at [solvewordle.com](www.solvewordle.com)

**Note: This app is under active development.** This includes both the backend algorithms that "solve" the Wordle puzzle, and the frontend user interface. The current version of the app is nonetheless available at [solvewordle.com](www.solvewordle.com). You can also clone this repo and run (and edit!) the app locally, and there are some instructions for how to do this below. 

# Basic overview of web app
The web app currently allows users to select one of four backend algorithms:
* **Random:** This methods generates a random next guess from the list of possible words. This is perhaps the simplest method for solving Wordle.
* **Rank:** This method finds the frequency of each letter within the list of remaining possible words, and uses this information to rank the remaining possible words. The highest ranked word is the one that's letters appear most frequently in the remaining list of possible words.
* **Brute Force Simple:** Finds the average feedback (green, orange, grey) for each remaining possible word, and ranks the remaining possible words based on this average feedback.
* **ChatGPT:** Uses the ChatGPT API to solve Wordle by describing Wordle in the model's context window. **Note that this method is not currently available in this web app** because of the cost of using the API, but you can try this method yourself by cloning the GitHub repository and running a version of the wordle solver yourself.

This is an example of the page that allows users to select the algorithm, although note that the options may change as the app develops:
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213870880-ac649656-6206-4340-a69c-c70e4353f661.png width="500" height="325">
</p>

The app then generates a trial word.

Users can input this word into the New York Times's [Wordle puzzle](https://www.nytimes.com/games/wordle/), which will then provide different colours as feedback for each letter.

Users can then input these colours into the Wordle Solver by pressing repeatedly on each letter. This cycles through the available colours: Green, Orange and Grey. 

Once the correct colours have been selected, users can generate the next trial word.
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213871605-8db959a3-dd6e-4849-b7d6-47bde318c2b8.png width="500" height="325">
</p>

This approach is repeated until the puzzle is solved.
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213871625-4d079634-d610-442b-b1ed-396547ebc725.png width="500" height="325">
</p>

## Getting Started
The online version of the web application can be found at [solvewordle.com](www.solvewordle.com)

To run the Wordle solver, you need to clone this repository and run the app on a local machine.

### Installing and running web app locally using a Python virtual environment
* Clone this repository: ```git clone https://github.com/richard-flint/wordle_solver.git```
* Create a new python virtual environment using the requirements.txt file. Instructions on how to do this can be found [here](https://docs.python.org/3/library/venv.html)
* Activate virtual environment, usually using ```venv\Scripts\activate``` (Windows) or ```source venv/bin/activate``` (Linuz/OS)
* Navigate to flask app folder: ```cd flask_app```
* Run flask app: ```python flask_app.py```
* View the app: Visit http://localhost:5000 in your browser to view the app

## Analysing current algorithm performance
The current highest-performing algorithm is called "Brute Force Simple". As noted above, this method finds the word that generates the shortest next list of remaining possible words.

The performances of "Random", "Rank" and "Brute Force Simple" across the entire Wordle dataset (i.e. every possible word that may appear in the Wordle puzzle) is illustrated in the histograms below. These histograms illustrate the number of guesses required to find each word in the Wordle dataset. For all algorithms tested, the most common number of guesses needed to find a word is 4, but the number of guesses ranges from 1 to 9. In other words, sometimes the algorithms find the word in 1 guess, sometimes they find the word in 9 guesses, but most often, they find the word in 4 guesses.

<div>
    <a href="https://plotly.com/~rflint/5/?share_key=w2YKL9n4LjBk8slPmho0FC" target="_blank" title="wordle_histogram" style="display: block; text-align: center;"><img src="https://plotly.com/~rflint/5.png?share_key=w2YKL9n4LjBk8slPmho0FC" alt="wordle_histogram" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plotly.com/404.png';" /></a>
</div>

The aggregated performances of the algorithms can be compared using a box-and-whisker plot. The plot below illustrates the **mean, variance and range** for all three algorithms. *Note: this differs from the typical box-and-whisker plot, which usually shows the median, interquartile range and range.* The plot below illustrates that the "Brute Force Simple" algorithm has a lower mean and variance compared to the two other algorithms, meaning "Brute Force Simple" takes fewer guesses on average to find a given Wordle word, and has less variability in its number of guesses.

However, all three algorithms sometimes require more than 6 guesses to find certain Wordle words, with "Brute Force Simple" sometimes requiring up to 9 guesses. This is illustrated below by the upper value of the whiskers (i.e. ranges). In the New York Times version of Wordle, users are only allowed up to 6 guesses to find a specific word, with 7 or more guesses registered as a failure. This means that all algorithms in the current version of the Wordle solver will sometimes fail. This is a priority feature for future algorithms: namely, developing an algorithm that solves Worldle for all words in 6 or fewer guesses, and so never loses the game. 

<div>
    <a href="https://plotly.com/~rflint/11/?share_key=7bskfURZS5h5rhpZsorY3q" target="_blank" title="wordle_box_whisker_mean" style="display: block; text-align: center;"><img src="https://plotly.com/~rflint/11.png?share_key=7bskfURZS5h5rhpZsorY3q" alt="wordle_box_whisker_mean" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plotly.com/404.png';" /></a>
</div>

We can also test whether differences between the above distributions are statistically significant, for example by using pairwise t-tests. The p-values from pairwise t-tests for all three algorithms are provided in Table 1 below. These p-values are all very small, and much smaller than the typical threshold values for t-tests (e.g. p<0.05, or p<0.02). This suggests that the distributions for "Random", "Rank" and "Brute Force Simple" are different, and that the performance improvement for "Brute Force Simple" is statistically significant. In other words, "Brute Force Simple" performs better on average, and it's very unlikely that this performance improvement is the result of random variability in the data.

|                         | Random                | Rank                  |  Brute Force Simple     |
| :-----------------------|:---------------------:|:---------------------:|:-----------------------:|
| **Random**              |                       | 3.5x10<sup>-12</sup>  |  9x10<sup>-64</sup>     |
| **Rank**                | 3.5x10<sup>-12</sup>  |                       |  2.2x10<sup>-124</sup>  |
| **Brute Force Simple**  | 9x10<sup>-64</sup>    | 2.2x10<sup>-124</sup> |                         |

*Table 1: Pairwise t-test (p-values)*

## Authors
Richard Flint, Marina Favaro
