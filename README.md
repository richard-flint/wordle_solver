# Wordle Solver (Flask App)
This is a simple web application that helps users solve the Guardian's daily [Wordle puzzle](https://www.nytimes.com/games/wordle/). 

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

### 

## Authors
Richard Flint, Marina Favaro
