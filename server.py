from _thread import *
import socket
import random
import sys


def hint_generator(guess, answer):
    """Checks the guessed word against the correct word, and generates a hint to be sent to the client.
    If a letter at a given position in the guess matches the letter at that same position in the answer,
    the character at that position in the hint will be the corresponding letter from the guess in uppercase.
    If a letter at a given position in the guess does not match the letter at that same position in the answer,
    but the letter in the guess does appear somewhere in the target word that has not already been matched,
    the character at that position in the hint will be the corresponding letter from the guess in lowercase.
    Otherwise, the character at a given position in the hint will be an underscore"""
    hint = ["_", "_", "_", "_", "_"]
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            hint[i] = guess[i].upper()
    for i in range(len(guess)):
        if guess[i] in answer and guess[i] != answer[i]:
            if (hint.count(guess[i]) + hint.count(guess[i].lower())) < answer.count(guess[i]):
                hint[i] = guess[i].lower()
    return "".join(hint)


def read_random_word():
    """Opens the list of target words and returns a random word from the list."""
    with open('target.txt') as f:
        words = f.read().splitlines()
        return random.choice(words)


def wordle_game_server(client):
    """wordle_game_server(socket) contains the logic for the Wordle game and will run the game when called"""
    selected_word = read_random_word()
    number_of_guesses = 0
    active_game_state = True
    # Send the first hint to the client to start the game
    client.send(bytes("_____"+"\n", 'utf-8'))
    while active_game_state:
        # Converts the incoming guess to upper case
        guess = client.recv(1024).decode('utf-8').upper()
        # Validate the incoming guess
        with open('guess.txt') as f:
            if guess in f.read():
                # Increment number_of_guesses if the guess was valid
                number_of_guesses += 1
                # If the guess matches the target word, send the game ending prompt to the client
                if guess == selected_word:
                    client.send(bytes(str(number_of_guesses), 'utf-8'))
                    client.send(bytes("GAME OVER"+"\n", 'utf-8'))
                    active_game_state = False
                else:
                    # If the guess does not match the target word, hints are sent to the client
                    new_hint = hint_generator(guess, selected_word)
                    client.send(bytes(new_hint+"\n", 'utf-8'))
            else:
                # If the guess was invalid, notify the client
                client.send(bytes("INVALID GUESS"+"\n", 'utf-8'))


def main():
    # Create a server socket, then bind to it
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reserving a port for this game
    host = socket.gethostname()
    port = 12345
    # Attempt to bind to the socket.
    # If successful, print a confirmation message.
    # If unsuccessful, exit with error message.
    try:
        s.bind((host, port))
        print(f"Server socket successfully bound to Port {port}")
    except socket.error as e:
        print(f"Error. Server is unable to connect to Port {port}")
        print(e)
        sys.exit(1)
    # Put the server socket into listening mode, queuing up to 5 connection requests
    s.listen(5)
    # Connect to incoming clients. Start the game once 'START GAME' is received from the client.
    while True:
        client_socket, address = s.accept()
        print(f"Received a connection from {address}")
        client_message = client_socket.recv(1024)
        if client_message.decode('utf-8') == "START GAME":
            client_socket.send(bytes("Welcome to Wordle. Try to guess the following 5 letter word", 'utf-8'))
            print(f"Game starting with {address}")
            start_new_thread(wordle_game_server, (client_socket,))
        else:
            print(f"Game start with {address} unsuccessful")
            break
    # Close the connection with the client once the game ends
    client_socket.close()


if __name__ == '__main__':
    main()
