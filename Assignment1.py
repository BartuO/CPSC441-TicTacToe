import socket
import sys
import tkinter as tk
from tkinter import messagebox




"""
Things to add:
Load/save game ~~ hardcoded directory!
endgame screen information
show score?
Exit
Go back to menu option
commandline arguments
error handling on network/game
readme
better mainmenu
make sure to remove print statements after finishing




 """





client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "136.159.5.25"

port = 6969

print("WELCOME TO THE TIC TAC TOE XD")

client_socket.connect((host, port))















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
    global game_on
    board = client_socket.recv(1024).decode("ascii").split(":")
    
    if(board[0] == "OVER"):
        #endgame implementation
        
        print("gameover")
        game_on = False
        return board[1].split(",")[1:]
    elif(board[0] == "EROR"):
        #error handling
        print("illegal move or smthng else")
    elif(board[0] == "BORD"):

        return board[1].split(",")





##interface
global clean_list
global client_char
global game_on
global temp_move
global interface_board


temp_move = None
clean_list = []
interface_board = [["", "", ""], ["", "", ""], ["", "", ""]]



window = tk.Tk()
window.title("TICTACTOE")
window.geometry("700x500")




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

    


def handleClick(row, col):
    global temp_move
    global interface_board
    if(game_on == True):
        if not interface_board[row][col]['text']:
            
            if temp_move is not None:
                interface_board[temp_move[0]][temp_move[1]]["text"] = "" 

            temp_move = (row,col)
            interface_board[row][col]['text'] = client_char
            
            
            
def confirmMove():
    global temp_move

    makeMove(temp_move)
    temp_move = None
    refreshInterfaceBoard(convertBoardToText(getBoard()))
    if(game_on == False):
                messagebox.showinfo("Game Over", "The game is over!")


def refreshInterfaceBoard(board):
    global interface_board
    for row in range(3):
        for col in range(3):
                if(board[row][col] == "X"):
                    interface_board[row][col]["fg"] = "red"
                elif(board[row][col] == "O"):
                    interface_board[row][col]["fg"] = "blue"
                interface_board[row][col]['text'] = board[row][col]
        


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
            interface_board[row][col].bind("<Button-1>", lambda event, row=row, col=col: handleClick(row, col))

    playButton = tk.Button(gameScene, text="Play", width=15, height=2, command = confirmMove)
    playButton.grid(row = 4, column = 1, pady = 15)

    clean_list.append(playButton)  




def loadGameScene():
    return 0



def newGameScene():

    global interface_board
    global client_char 
    global game_on
    
    client_socket.sendall("NEWG".encode("ascii"))
    board = client_socket.recv(1024).decode("ascii").split(":")[1].split(",")
    game_on = True

    client_char = "X"

    for i in board:
        if(i != "2"):
            client_char = "O"
            break
    
    print(board)

    gameScene()

    refreshInterfaceBoard(convertBoardToText(board))

    

    



mainMenuScene()
window.mainloop()







client_socket.close()