# Wordle Solver (Flask App)
This is a simple web application that helps users (i.e. me!) solve the New York Times's daily [Wordle puzzle](https://www.nytimes.com/games/wordle/).

**Note: This app is under active development. This includes both the backend algorithms that "solve" the Wordle puzzle, and the frontend user interface. The current version of the app should nonetheless work if installed as instructed below. Current areas of development include:**
* **Deployment on serverless infrastructure**
* **Training an RL agent and comparing to existing algorithms**

# Basic overview of web app
The web app currently allows users to select one of three backend algorithms:
* **Random:** This methods generates a random next guess from the list of possible words. This is perhaps the simplest possible method for solving Wordle.
* **Rank:** This method finds the frequency of each letter within the list of remaining possible words, and uses this information to rank the remaining possible words.
* **Brute Force Simple:** This method finds the word that generates the shortest next list of remaining possible words.
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213870880-ac649656-6206-4340-a69c-c70e4353f661.png width="500" height="325">
</p>
The app then generates a trial word, and enables users to input the colours from the Guardian's wordle app before producing the next trial word.
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213871605-8db959a3-dd6e-4849-b7d6-47bde318c2b8.png width="500" height="325">
</p>

This approach is repeated until the puzzle is solved.
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213871625-4d079634-d610-442b-b1ed-396547ebc725.png width="500" height="325">
</p>

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing and virtual web app locally using a Python virtual environment
* Clone this repository: ```git clone https://github.com/richard-flint/wordle_solver.git```
* Navigate to "codebase" folder in this repository using the command line: ```cd \wordle_solver\codebase```
* Activate virtual environment: ```myvenv\Scripts\activate``` (Windows) or ```source venv/bin/activate``` (Linuz/OS)
* Navigate to flask app folder: ```cd flask_app```
* Run flask app: ```python flask_app.py```
* View the app: Visit http://localhost:5000 in your browser to view the app

## Current algorithm performance
The current highest-performing algorithm is called "Brute Force Simple". As noted above, this method finds the word that generates the shortest next list of remaining possible words.

The basic performance across the entire dataset for "Brute Force Simple" is provided in the histogram below. The histogram illustrates the number of guesses required to find each word in the Wordle dataset. For all algorithms tested, the most common number of guesses needed to find a word is 4, but the number of guesses ranges from 1 to 9. In simple terms, a better algorithm will have a distribution that is shifted further to the left i.e. it takes fewer guesses to find more of the words in the dataset.

<div>
    <a href="https://plotly.com/~rflint/5/?share_key=w2YKL9n4LjBk8slPmho0FC" target="_blank" title="wordle_histogram" style="display: block; text-align: center;"><img src="https://plotly.com/~rflint/5.png?share_key=w2YKL9n4LjBk8slPmho0FC" alt="wordle_histogram" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plotly.com/404.png';" /></a>
</div>

The agregated performances of the algorithms can also be compared, for example using a box-and-whisker plot. The plot below illustrates the **mean, variance and range** for all three algorithms. *Note: this differs from the typical box-and-whisker plot, which usually shows the median, interquartile range and range.* The plot below shows that the "Brute Force Simple" algorithm has a lower mean and variance compared to the two other algorithms currently available, meaning "Brute Force Simple" takes fewer guesses on average to find a given Wordle word, and has less variability in its number of guesses.

However, all three algorithms sometimes require more than 6 guesses to find certain Wordle words, with "Brute Force Simple" sometimes requiring up to 9 guesses to find certain words. This is illustrated below by the upper value of the whiskers (i.e. ranges). In the New York Times version of Wordle, users are only allowed up to 6 guesses to find a specific word, with 7 or more guesses registered as a failure. This means that all algorithms currently in this Wordle solver will sometimes fail, which is not ideal. This is a priority feature for future algorithms. Namely, developing algorithms that solve Worldle for all words in 6 or fewer guesses. 

<div>
    <a href="https://plotly.com/~rflint/11/?share_key=7bskfURZS5h5rhpZsorY3q" target="_blank" title="wordle_box_whisker_mean" style="display: block; text-align: center;"><img src="https://plotly.com/~rflint/11.png?share_key=7bskfURZS5h5rhpZsorY3q" alt="wordle_box_whisker_mean" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plotly.com/404.png';" /></a>
</div>

We can also test if the differences between the above distributions are statistically significant, for example by using pairwise t-tests. 

                    | Random                | Rank                  |  Brute Force Simple     |
------------------- | --------------------- | --------------------  |  ---------------------  |
Random              | /                     | 3.5x10<sup>-12</sup>  |  9x10<sup>-64</sup>     |
Rank                | 3.5x10<sup>-12</sup>  | /                     |  2.2x10<sup>-124</sup>  |
Brute Force Simple  | 9x10<sup>-64</sup>    | 2.2x10<sup>-124</sup> |  /                      |

## Authors
Richard Flint, Marina Favaro
