import socket
import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog




# cd C:\Users\bartu\Desktop\UniStuff\2023Fall\CPSC441\Assignment1\CPSC441-TicTacToe && python tictacClient.py 136.159.5.25 6969

"""
Things to add:
Load/save game ~~ hardcoded directory! -- done
endgame screen information -- done
Exit -- done
Go back to menu option -- done
commandline arguments -- done 
centre in the middle --done
show score?
error handling on network/game
readme
better mainmenu
make sure to remove print statements after finishing


change the icon?


after finishing:
check if tkinter is ok
beat AI

 """


if len(sys.argv) != 3:
    print("Wrong number of arguments. Exiting")
    sys.exit()
else:
    host = sys.argv[1]
    port = int(sys.argv[2])





current_directory = os.path.dirname(os.path.abspath(__file__))
saves_directory = current_directory + "/Game Saves"

if not os.path.exists(saves_directory):
    os.mkdir(saves_directory)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



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
        global won

        print("gameover")
        game_on = False
        
        if board[1].split(",")[0] == "S":
            won = False
        elif board[1].split(",")[0] == "C":
            won = True
        else:
            won = None
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
global won
global score
global interface_board

score = [0,0,0] # Client, Draw, AI
won = None
temp_move = None
clean_list = []
interface_board = [["", "", ""], ["", "", ""], ["", "", ""]]



window = tk.Tk()
window.title("TICTACTOE")
width = 700
height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2

window.geometry(f"{width}x{height}+{x}+{y}")




def clear_frame():
    global clean_list

    for widget in clean_list:
        widget.destroy()

    clean_list = []
    



frame = tk.Frame(window)
frame.pack(fill = tk.BOTH, expand = True)


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension = ".txt", initialdir = saves_directory)
    if file_path:
        with open(file_path, "w") as f:
            f.write(str(client_char) + ",")
    
            for row in range(3):
                for col in range(3):
                    i = interface_board[row][col]["text"]
                    if (i == ""):
                        f.write("2,")
                    elif(i == "X"):
                        f.write("0,")
                    elif(i == "O"):
                        f.write("1,")


        



def load_file():
    file_path = filedialog.askopenfilename(initialdir = saves_directory, defaultextension=".txt")
    if file_path:
        with open(file_path, "r") as f:
            game = f.readline()
            if game:

                global client_char
                global game_on

                client_socket.sendall(f"LOAD:{game[:-1]}".encode("ascii"))
                board = client_socket.recv(1024).decode("ascii").split(":")[1].split(",")
                game_on = True

                client_char = game[0]

                gameScene()

                refreshInterfaceBoard(convertBoardToText(board))
    else:
        #error handling etc
        return 0


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

    button2 = tk.Button(mainMenu, text="Load Saved Game", width=15, height=2, command = load_file)
    button2.grid(row=3, column=1, padx=5)
    clean_list.append(button2)  

    button3 = tk.Button(mainMenu, text="Show Score", width=15, height=2, command = showScoreScene)
    button3.grid(row=4, column=1, padx=5)
    clean_list.append(button3)  

    button4 = tk.Button(mainMenu, text="Exit", width=15, height=2, command = exitGame)
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
    if temp_move != None:
        makeMove(temp_move)
        temp_move = None
        refreshInterfaceBoard(convertBoardToText(getBoard()))
        if(game_on == False):
                    global won
                    if won == True:
                        score[0] += 1
                        answer = messagebox.askquestion("Game Over", "You won the game. \n\nWould you like to start a new game? ")
                        if answer == "yes":
                            newGameScene()
                        else:
                            mainMenuScene()
                    elif won == False:
                        score[2] += 1
                        answer = messagebox.askquestion("Game Over", "AI won the game. \n\nWould you like to start a new game? ")
                        if answer == "yes":
                            newGameScene()
                        else:
                            mainMenuScene()
                    else:
                        score[1] += 1
                        answer = messagebox.askquestion("Game Over", "Game is a draw. \n\nWould you like to start a new game? ")
                        if answer == "yes":
                            newGameScene()
                        else:
                            mainMenuScene()


def refreshInterfaceBoard(board):
    global interface_board
    for row in range(3):
        for col in range(3):
                if(board[row][col] == "X"):
                    interface_board[row][col]["fg"] = "red"
                elif(board[row][col] == "O"):
                    interface_board[row][col]["fg"] = "blue"
                interface_board[row][col]['text'] = board[row][col]
        
def exitGame():
    result = messagebox.askquestion("Exit", "Are you sure?")
    if result == "yes":
        client_socket.sendall("CLOS".encode("ascii"))
        window.destroy()



def gameScene():
    
    clear_frame()




    gameScene = tk.Frame(window)
    gameScene.place(relx=.5, rely=.45,anchor= "center")
    clean_list.append(gameScene)

    menubar = tk.Menu(window)
    
    menubar.add_command(label=" Save ", command = save_file)

    menubar.add_separator()
    menubar.add_command(label=" Back To Main Menu ", command = mainMenuScene)


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

    
def showScoreScene():
    global score

    clear_frame()
    
    scoreScene = tk.Frame(window)
    scoreScene.place(relx=.5, rely=.45,anchor= "center")
    clean_list.append(scoreScene)

    client_label = tk.Label(scoreScene, text= f"Client Won: {score[0]}", fg = "blue")
    draw_label = tk.Label(scoreScene, text=  f"Draw: {score[1]}")
    ai_label = tk.Label(scoreScene, text= f"AI Won: {score[2]}", fg = "red")

    client_label.grid(row=0, column=0, padx=10, pady=10)
    draw_label.grid(row=0, column=1, padx=10, pady=10)
    ai_label.grid(row=0, column=2, padx=10, pady=10)

    main_menu= tk.Button(scoreScene, text="Go Back To Main Menu", command= mainMenuScene)
    main_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=20)

mainMenuScene()
window.mainloop()







client_socket.close()