# Wordle

This iteration of Wordle was developed using Python 3.9, and runs on a server that supports multiple concurrent clients/players.


## Installation

Unzip the contents to a target destination. 
The package should contain the following files, along with this readme:
- server.py
- client.py
- guess.txt
- target.txt


## Usage

Once all files are contained within the same folder, the game can be run through the command line interface. The server must be run before the clients. The server and each separate concurrent client will require a separate command line interface.


## Game Rules

When a new client connects to the server, the server will randomly select a word from its target word list to be the target word for that client. The server will give the client an initial hint, consisting of five underscores: "_____"

The client will then need to send along guesses of five-letter words until it discovers the target word. After each valid guess, the server will respond with a five-character hint. Each hint depends on the previous guess from the user, and is determined as follows (in order of priority):

1. If a letter at a given position in the guess matches the letter at that same position in the target word, the character at that position in the hint will be the corresponding letter from the guess in uppercase.
2. If a letter at a given position in the guess does not match the letter at that same position in the target word, but the letter in the guess does appear somewhere in the target word that has not already been matched by this or the previous rule, the character at that position in the hint will be the corresponding letter from the guess in lowercase.
3. If neither of the conditions above are met, the character at a given position in the hint will be an underscore: "_"

Once the client has correctly guessed the target word, the server sends a score to the player consisting of the number of valid guesses it took to discover the target word, followed by a "GAME OVER" message. 
Players are prompted with "INVALID GUESS" when a guess does not exist in the guess.txt file. Invalid guesses do not increment the score counter.
Note: Player guesses are not case-sensitive.


## Author
Jesse Chow

Last Updated: 06 May 2022
