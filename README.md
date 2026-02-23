# Mastermind Project - implementation of the game and game simulation algorithm
## Project description
The project consists of 3 modules:
1. Interactive game mode - allows you to play the Mastermind game in an extended version, 
   meaning with the possibility to choose the number of colors and slots, it has a graphical interface.
   The exact rules of the game are printed when the application starts and are publicly available
   on the internet.
2. Automatic mode - an algorithm simulating the extended version of the game, it does not have 
   a graphical interface - data is entered directly into the console.
3. Evaluating module - contains a function verifying the guess against the hidden sequence, it is 
   used in the other 2 modules and is not interactive.
## Technologies used
The project was created using:
- Python 3.12.3
- Kivy 2.2.1
## How to use
1. Install all needed libraries by typing the following command in the console:
   ``` 
   pip install -r requirements.txt
   ```
2. To run the interactive game mode:
   ```
   python3 master_graj.py
   ```
2. To run the automatic mode:
   ```
   python3 master_automat.py
   ```
## Sources
While creating this project, I used the following websites:
https://www.w3schools.com/python/
https://kivy.org/doc/stable/
and the Kivy course https://www.youtube.com/watch?v=l8Imtec4ReQ