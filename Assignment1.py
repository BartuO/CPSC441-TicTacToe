import socket
import sys
import tkinter as tk










client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "136.159.5.25"

port = 6969

print("WELCOME TO THE TIC TAC TOE XD")

client_socket.connect((host, port))











def newGame():
    print("hello")
    client_socket.sendall("NEWG".encode("ascii"))
    board = client_socket.recv(1024).decode("ascii").split(":")[1].split(",")

    client_char = "X"

    for i in board:
        if(i != "2"):
            client_char = "O"
            break

    gameLoop(board, client_char)


def loadGame():
    return 0

def gameLoop(board, client_char):
    gameOn = True

    while gameOn:
        print(board)

        makeMove((1,1))

        board = getBoard()




def convertBoardToText(board):

 

    counter = 0

    board_for_interface = []

    for i in range(3):
        row = []
        for b in range(3):

            if(board[counter] == "2"):
                row.append("")
            elif(board[counter] == "0"):
                row.append("X")
            elif(board[counter] == "1"):
                row.append("O")

            counter += 1

        board_for_interface.append(row)


    return board_for_interface
            

        

def makeMove(coordinate):
    f, s = coordinate
    client_socket.sendall(("MOVE:" + str(f) + "," + str(s)).encode("ascii"))


def getBoard():
    board = client_socket.recv(1024).decode("ascii").split(":")
    if(board == "OVER"):
        #endgame implementation
        print("gameover")
    elif(board == "EROR"):
        #error handling
        print("illegal move or smthng else")
    elif(board == "BORD"):
        return board[1].split(",")





##interface
global clean_list
global client_char
clean_list = []

window = tk.Tk()
window.title("TICTACTOE")
window.geometry("700x500")

global interface_board
interface_board = [["", "", ""], ["", "", ""], ["", "", ""]]

def clear_frame():
    global clean_list

    for widget in clean_list:
        widget.destroy()

    clean_list = []
    



frame = tk.Frame(window)
frame.pack(fill = tk.BOTH, expand = True)


def mainMenuScene():
    clear_frame()


    mainMenu = tk.Frame(window)
    mainMenu.place(relx=.5, rely=.5,anchor= "center")
    clean_list.append(mainMenu)

   
    greeting_label = tk.Label(mainMenu, text="Welcome", font=("Helvetica", 16))
    greeting_label.grid(row=1, column=1, pady=(10, 5))
    clean_list.append(greeting_label)  

    button1 = tk.Button(mainMenu, text="New Game", width=15, height=2, command = newGameScene)
    button1.grid(row=2, column=1, padx=5)
    clean_list.append(button1)  

    button2 = tk.Button(mainMenu, text="Button 2", width=15, height=2)
    button2.grid(row=3, column=1, padx=5)
    clean_list.append(button2)  

    button3 = tk.Button(mainMenu, text="Button 3", width=15, height=2)
    button3.grid(row=4, column=1, padx=5)
    clean_list.append(button3)  

    button4 = tk.Button(mainMenu, text="Button 4", width=15, height=2)
    button4.grid(row=5, column=1, padx=5)
    clean_list.append(button4)  

    


def handle_click(row, col):
    if not interface_board[row][col]['text']:
        interface_board[row][col]['text'] = client_char

def refreshBoard():
    for row in range(3):
        for col in range(3):
            interface_board[row][col]['text'] = interface_board[row][col]
        


def gameScene():
    
    clear_frame()




    gameScene = tk.Frame(window)
    gameScene.place(relx=.5, rely=.45,anchor= "center")
    clean_list.append(gameScene)

    menubar = tk.Menu(window)
    
    menubar.add_command(label="Open")
    menubar.add_command(label="Save")
    menubar.add_separator()
    menubar.add_command(label="Exit")


    window.config(menu = menubar)

    clean_list.append(menubar)


    for row in range(3):
        for col in range(3):
            label = tk.Label(gameScene, text="", width=6, height=3, relief=tk.RIDGE, font=("Helvetica", 24))
            label.grid(row=row, column=col, padx= 0, pady = 0)
            interface_board[row][col] = label
            clean_list.append(label)
    
    for row in range(3):
        for col in range(3):
            interface_board[row][col].bind("<Button-1>", lambda event, row=row, col=col: handle_click(row, col))

    playButton = tk.Button(gameScene, text="Play", width=15, height=2)
    playButton.grid(row = 4, column = 1, pady = 15)
    clean_list.append(playButton)  


def changeInterfaceBoard(board):
    for row in range(3):
        for col in range(3):
            interface_board[row][col]['text'] = str(board[row][col])


def loadGameScene():
    return 0



def newGameScene():

    global interface_board
    global client_char 
    
    client_socket.sendall("NEWG".encode("ascii"))
    board = client_socket.recv(1024).decode("ascii").split(":")[1].split(",")

    client_char = "X"

    for i in board:
        if(i != "2"):
            client_char = "O"
            break
    
    print(board)

    changeInterfaceBoard(convertBoardToText(board))

    print(intre)

    gameScene()



mainMenuScene()
window.mainloop()







client_socket.close()