import socket
import threading
import json

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

turn = False
board = '         b'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def main():
    input("\tTic-Tac-Toe\n-------------------------\nPress Enter to Host Game")
    print("[STARTING] server is starting...")
    start()


def print_board():
    display_board = '012345678'
    print(f'{display_board[0]} | {display_board[1]} | {display_board[2]}')
    print('- - - - -')
    print(f'{display_board[3]} | {display_board[4]} | {display_board[5]}')
    print('- - - - -')
    print(f'{display_board[6]} | {display_board[7]} | {display_board[8]}')
    print('\n')
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print('- - - - -')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print('- - - - -')
    print(f'{board[6]} | {board[7]} | {board[8]}')

def check_for_win(board):
    for i in range(3):
        if board[i*3] == 'X' and board[i*3 + 1] == 'X' and board[i*3 + 2] == 'X':
            return True
        if board[i] == 'X' and board[i+3] == 'X' and board[i+6] == 'X':
            return True
    if board[0] == 'X' and board[4] == 'X' and board[8] == 'X':
        return True
    elif board[2] == 'X' and board[4] == 'X' and board[6] == 'X':
        return True
    return False

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            global board
            if msg == DISCONNECT_MESSAGE:
                print("game over")
                connected = False
                board = '         b'
            elif msg =="Your turn!":
                take_turn(conn)
            elif msg[-1] == 'b':
                board = msg
                take_turn(conn)
            
            # my_string = str(msg)
            # msg_object = json.loads(my_string)
            # print(f"[{addr}] {msg}")
    
    conn.close()

def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} ")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")
            
def take_turn(conn):
    print("Your turn")
    print_board()
    choice = -1
    while choice < 0 or choice > 8:
        input_string = input("Which spot would you like to claim?\n>")
        if input_string in '012345678':
            choice = int(input_string)
    global board
    board = board[:choice] + "X" + board[choice+1:]
    print_board()
    if check_for_win(board):
        print("You won!")
        send("You lost!",conn)
        board = '         b'
    elif ' ' not in board:
        print("cats game!")
        send("Cats game!",conn)
        board = '        b'
    else:
        send(board,conn)
        print("Waiting on other player...")

        
main()
