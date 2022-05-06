import socket
import sys


def main():
    # Create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    # Attempt to connect to the server. If unsuccessful, exit with error message.
    try:
        s.connect((host, port))
    except socket.error as e:
        print(f"Error. Unable to connect to the server at ({host}, {port})")
        print(e)
        sys.exit(1)
    # Send the 'START GAME' prompt to the server
    s.send(bytes("START GAME", 'utf-8'))
    # Receive and print the welcoming message from the server
    print(s.recv(1024).decode('utf-8'))
    # Receive the first hint from the server to confirm game start
    server_hint = s.recv(1024)
    if server_hint.decode('utf-8') == "_____"+"\n":
        active_game_state = True
        print(server_hint.decode('utf-8'))
        while active_game_state:
            # Prompt the user for a guess.
            guess = input("Enter a 5 letter word: ")
            # Perform client side validation. Invalid guesses cause the game to terminate.
            if len(guess) != 5:
                print("Error. User input is too short.")
                break
            elif guess.isalpha() is False:
                print("Error. User input is invalid.")
                break
            else:
                # Valid guesses are sent to the server
                s.send(bytes(guess, 'utf-8'))
            # If the response from the server is a numerical score, the game ends.
            # Otherwise, the game continues.
            server_response = s.recv(1024).decode('utf-8')
            if server_response.isdigit():
                print("Your word is correct!")
                print(f"Number of valid guesses: {server_response}")
                print(s.recv(1024).decode('utf-8'))
                active_game_state = False
            else:
                print(server_response)
        # Close the connection to the server
        s.close()
    s.close()


if __name__ == '__main__':
    main()
