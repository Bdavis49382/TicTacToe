import socket
import json

HEADER = 64
PORT = 5050
SERVER = "10.11.6.55"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def print_board(board):
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print('- - - - -')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print('- - - - -')
    print(f'{board[6]} | {board[7]} | {board[8]}')

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("Waiting for other player...")
    handle_response()
    
def handle_response():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        if msg[-1] == 'b':
            take_turn(msg)
        else:
            print(f"From Server: {msg}")

def check_for_win(board):
    for i in range(3):
        if board[i*3] == 'O' and board[i*3 + 1] == 'O' and board[i*3 + 2] == 'O':
            return True
        if board[i] == 'O' and board[i+3] == 'O' and board[i+6] == 'O':
            return True
    if board[0] == 'O' and board[4] == 'O' and board[8] == 'O':
        return True
    elif board[2] == 'O' and board[4] == 'O' and board[6] == 'O':
        return True
    return False

def take_turn(board):
    print("Your turn")
    display_board = '012345678'
    print_board(display_board)
    print('\n\n\n')
    print_board(board)
    choice = -1
    while choice < 0 or choice > 8:
        input_string = input("Which spot would you like to claim?\n>")
        if input_string in '012345678':
            choice = int(input_string)
    board = board[:choice] + "O" + board[choice+1:]
    print_board(board)
    if check_for_win(board):
        print("you won!")
        send(DISCONNECT_MESSAGE)
    elif ' ' not in board:
        print("cats game!")
        send(DISCONNECT_MESSAGE)
    else:
        send(board)
    


send("Your turn!")