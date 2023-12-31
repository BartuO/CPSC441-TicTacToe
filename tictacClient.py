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
show score? -- done
error handling on network/game -- done
readme -- 
better mainmenu -- done
make sure to remove print statements after finishing --done
change the icon? -- done
add comments -- done

after finishing:
check if tkinter is ok -- done
beat AI

 """



if len(sys.argv) != 3: #Checking if correct number of arguments are given
    print("Wrong number of arguments. Exiting")
    sys.exit()
else:
    host = sys.argv[1]
    port = int(sys.argv[2])




#Getting the directory of the file
current_directory = os.path.dirname(os.path.abspath(__file__))
saves_directory = current_directory + "/Game Saves"

#If the directory to put saves files in don't exist, create one
if not os.path.exists(saves_directory):
    os.mkdir(saves_directory)


try: #Creating the socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print(f"An error has occured during socket creation: {e}")
    sys.exit()


print("WELCOME TO THE TICTACTOE")


try: #Connecting to the server
    client_socket.connect((host, port))
except Exception as e:
    print(f"An error has occured while connecting to the server: {e}")
    sys.exit()












"""
This function takes the board from the protocol and turns it into a 2-dimensional list that the interface can use.
"""

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
            

        
"""
This function sends the move played by the player to the server in the right messsage protocol.
"""
def makeMove(coordinate):
    f, s = coordinate
    try:
        client_socket.sendall(("MOVE:" + str(f) + "," + str(s)).encode("ascii"))
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit()

"""
This functions recieves the message from the server and decides on how to use it.
"""
def getBoard():
    global game_on
    try:
        board = client_socket.recv(1024).decode("ascii").split(":")
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit()



    if(board[0] == "OVER"):#endgame implementation
        
        global won
        game_on = False
        
        if board[1].split(",")[0] == "S":
            won = False
        elif board[1].split(",")[0] == "C":
            won = True
        else:
            won = None
        return board[1].split(",")[1:]
    
    elif(board[0] == "EROR"):#error handling
        
        error_message = "This should never happen in any case because of the way game and interface are designed. \nIf it does, please reach out to me at: bartu.okan@ucalgary.ca \n\nPress 'Yes' if you would like to start a new game, 'No' if you would like to exit the game. "
        answer = messagebox.askquestion("ERROR", error_message)
        if answer == "yes":
            newGameScene()
        else:
            exitGame()

    elif(board[0] == "BORD"):#game continues 

        return board[1].split(",")





##Interface and Game Logic

global clean_list #list of widgets to clear when changing frames
global client_char  #character of the client, either X or O
global game_on  # True if the game still goes on, False if not
global temp_move #Temporary move on the client-side, is confirmed after play button is pressed and message is sent to the server
global won #True if the player won the game, false if not
global score #List of the score for the showScore() function [ClientWins, Draws, AIWins]
global interface_board #2-D List of the board that is displayed on the interface

score = [0,0,0] # Client, Draw, AI
won = None
temp_move = None
clean_list = []
interface_board = [["", "", ""], ["", "", ""], ["", "", ""]]


#Setting up the interface

window = tk.Tk()
window.title("TICTACTOE")
width = 700
height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2

##window.iconbitmap(current_directory + "/tictactoe.ico")  #commented out because i can't submit images
window.geometry(f"{width}x{height}+{x}+{y}")

frame = tk.Frame(window)
frame.pack(fill = tk.BOTH, expand = True)


""""
This functions clears the scene
"""
def clear_frame():
    global clean_list

    for widget in clean_list:
        widget.destroy()

    clean_list = []
    





"""
This function handles saving the game to a text file
"""
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


        


"""
This functions handles loading the file
"""
def load_file():
    file_path = filedialog.askopenfilename(initialdir = saves_directory, defaultextension=".txt")
    if file_path:
        with open(file_path, "r") as f:
            game = f.readline()
            if game and len(game) == 20:

                global client_char
                global game_on
                try:
                    client_socket.sendall(f"LOAD:{game[:-1]}".encode("ascii"))
                    board = client_socket.recv(1024).decode("ascii").split(":")[1].split(",")
                    game_on = True
                except Exception as e:
                    print(f"Connection error: {e}")
                    sys.exit()

                client_char = game[0]

                gameScene()

                refreshInterfaceBoard(convertBoardToText(board))
            else:#error handling
                messagebox.showinfo("Error", "Problem loading the save file.")

    else:#error handling
        messagebox.showinfo("Error", "Problem loading the save file.")
        

"""
This functions handles creating the Main Menu Scene and its interactions.
"""
def mainMenuScene():
    clear_frame()


    mainMenu = tk.Frame(window)
    mainMenu.place(relx=.5, rely=.5,anchor= "center")
    clean_list.append(mainMenu)

   
    greeting_label = tk.Label(mainMenu, text="Welcome", font=("Helvetica", 16))
    greeting_label.grid(row=1, column=1, pady=(10, 5))
    clean_list.append(greeting_label)


    button1 = tk.Button(mainMenu, text="New Game", width=15, height=2, command = newGameScene)
    button1.grid(row=3, column=1, padx=5)
    clean_list.append(button1)  

    button2 = tk.Button(mainMenu, text="Load Saved Game", width=15, height=2, command = load_file)
    button2.grid(row=4, column=1, padx=5)
    clean_list.append(button2)  

    button3 = tk.Button(mainMenu, text="Show Score", width=15, height=2, command = showScoreScene)
    button3.grid(row=5, column=1, padx=5)
    clean_list.append(button3)  

    button4 = tk.Button(mainMenu, text="Exit", width=15, height=2, command = exitGame)
    button4.grid(row=6, column=1, padx=5)
    clean_list.append(button4)  

    

"""
This functions handles clicks on the game board when a game is being played.
"""
def handleClick(row, col):
    global temp_move
    global interface_board
    if(game_on == True):
        if not interface_board[row][col]['text']:
            
            if temp_move is not None:
                interface_board[temp_move[0]][temp_move[1]]["text"] = "" 

            temp_move = (row,col)
            interface_board[row][col]['text'] = client_char
            
            
"""
This functions handles the play button. It sends the information of the move that is played to the server after the button is pressed.
It also handles the endgame screen.
"""            
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

"""
This functions handles refreshing the interface game board after a move has been played by the server.
"""
def refreshInterfaceBoard(board):
    global interface_board
    for row in range(3):
        for col in range(3):
                if(board[row][col] == "X"):
                    interface_board[row][col]["fg"] = "red"
                elif(board[row][col] == "O"):
                    interface_board[row][col]["fg"] = "blue"
                interface_board[row][col]['text'] = board[row][col]

"""
This functions handles the exit game button.
"""        
def exitGame():
    result = messagebox.askquestion("Exit", "Are you sure?")
    if result == "yes":
        try:
            client_socket.sendall("CLOS".encode("ascii"))
            window.destroy()
        except Exception as e:
            print(f"Connection error: {e}")
            sys.exit()

"""
This function handles the game scene. 
"""
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




"""
This function handles the new game option in the main menu.
"""
def newGameScene():

    global interface_board
    global client_char 
    global game_on
    
    try:
        client_socket.sendall("NEWG".encode("ascii"))
        board = client_socket.recv(1024).decode("ascii").split(":")[1].split(",")
        game_on = True
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit()

    client_char = "X"

    for i in board:
        if(i != "2"):
            client_char = "O"
            break
    


    gameScene()

    refreshInterfaceBoard(convertBoardToText(board))

"""
This function handles the show score option in the main menu
"""    
def showScoreScene():
    global score

    clear_frame()
    
    scoreScene = tk.Frame(window)
    scoreScene.place(relx=.5, rely=.45,anchor= "center")
    clean_list.append(scoreScene)

    client_label = tk.Label(scoreScene, text= f"Player Won: {score[0]}", fg = "blue")
    draw_label = tk.Label(scoreScene, text=  f"Draw: {score[1]}")
    ai_label = tk.Label(scoreScene, text= f"AI Won: {score[2]}", fg = "red")

    client_label.grid(row=0, column=0, padx=10, pady=10)
    draw_label.grid(row=0, column=1, padx=10, pady=10)
    ai_label.grid(row=0, column=2, padx=10, pady=10)

    main_menu= tk.Button(scoreScene, text="Go Back To Main Menu", command= mainMenuScene)
    main_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=20)





#Creating the scenes and starting the interface
mainMenuScene()
window.mainloop()


try: #Closing the connection with the server
    client_socket.close()
except Exception as e:
    print(f"Connection error: {e}")
    sys.exit()