# Wordle Solver (Flask App)
This is a simple web application that helps users solve the Guardian's daily [Wordle puzzle](https://www.nytimes.com/games/wordle/). 

**Note: This app is under active development, including both backend algorithms and the frontend user interface. Current areas of development include:**
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
  <img src=https://user-images.githubusercontent.com/63592862/213870880-ac649656-6206-4340-a69c-c70e4353f661.png width="500" height="325">
</p>

This approach is repeated until the puzzle is solved.
<p align="center">
  <img src=https://user-images.githubusercontent.com/63592862/213870880-ac649656-6206-4340-a69c-c70e4353f661.png width="500" height="325">
</p>

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
You will need to have Python and Flask installed on your system.

## Installing
Clone the repository
Copy code
git clone https://github.com/YOUR_USERNAME/wordle-flask-app.git
Install the required packages
Copy code
pip install -r requirements.txt
Run the app
Copy code
python app.py
Visit http://localhost:5000 in your browser to view the app.
Built With
Flask - The web framework used
Wordle - The library used to generate word clouds
Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Authors
Your Name - Initial work - YOUR_USERNAME

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
Hat tip to anyone whose code was used
Inspiration
etc
