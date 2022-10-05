from tkinter import *
from tkinter import messagebox

class Piece:
    def __init__(self, colour:int, x:int, y:int): #White = 1, Black = -1
        self.colour = colour
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
    
    def __str__(self):
        return self.icon()

    def update(self):
        global p1_king, p2_king, board
        #temp_board = undo_board
        #undo_board = board.copy()
        board[self.oldy][self.oldx] = " "
        old = board[self.x][self.y]
        board[self.y][self.x] = self #1 self.icon()
        if self.colour == -1:
            if p1_king.check_for_check():
                board[self.oldy][self.oldx] = self
                board[self.y][self.x] = old
                self.x, self.y = self.oldx, self.oldy
                #undo_board = temp_board
                return False
        else:
            if p2_king.check_for_check():
                board[self.oldy][self.oldx] = self
                board[self.y][self.x] = old
                self.x, self.y = self.oldx, self.oldy
                #undo_board = temp_board
                return False
        self.oldx, self.oldy = self.x, self.y
        #print(board is undo_board)
        return True
    
    def force_move(self, x:int, y:int):
        self.x = x
        self.y = y
        board[self.oldy][self.oldx] = " "
        board[self.y][self.x] = self
        self.oldx, self.oldy = self.x, self.y

class Pawn(Piece):
    def __init__(self, colour: int, x: int, y: int):
        super().__init__(colour, x, y)
        self.bonus_move = 1
        self.upgrade_to =0
    
    def upgrade_dialogue_box(self):
        def set_choice(num):
            self.upgrade_to = num
            print(self.upgrade_to)
            dialogue_window.quit()
            dialogue_window.destroy()

        num = 0
        dialogue_window = Toplevel()
        dialogue_window.title("Upgrade")
        Label(dialogue_window, text="Choose a piece to upgrade your pawn to").grid(row=0, column=0, columnspan=4, padx=10)
        Button(dialogue_window, text="Queen", command= lambda: set_choice(1)).grid(row=1, column=0, pady=10)
        Button(dialogue_window, text="Bishop", command= lambda: set_choice(2)).grid(row=1, column=1, pady=10)
        Button(dialogue_window, text="Knight", command= lambda: set_choice(3)).grid(row=1, column=2, pady=10)
        Button(dialogue_window, text="Rook", command= lambda: set_choice(4)).grid(row=1, column=3, pady=10)

        dialogue_window.mainloop()

    
    def upgrade(self):
        if (self.x == 7 and self.colour == 1) or (self.x == 0 and self.colour == -1):
            self.upgrade_dialogue_box()
            print("teset", self.upgrade_to)
            if self.upgrade_to == 1:
                Queen(colour=self.colour, x=self.x, y=self.y).update()
            elif self.upgrade_to == 2:
                Bishop(colour=self.colour, x=self.x, y=self.y).update()
            elif self.upgrade_to == 3:
                Knight(colour=self.colour, x=self.x, y=self.y).update()
            elif self.upgrade_to == 4:
                Rook(colour=self.colour, x=self.x, y=self.y).update()
            else:
                print("Invalid Answer")
                self.upgrade()

    def move(self, x:int, y:int):
        if (self.x < x <= self.x + 1 + self.bonus_move and self.y == y and self.colour == 1) or (self.x > x >= self.x - 1 - self.bonus_move and self.y == y and self.colour == -1):
            if board[y][x] == " ":
                if -1 < x < 8 and -1 < y < 8:
                    self.x = x
                    if not self.update():
                        return "nope"
                    self.upgrade()
            else:
                return "nope"
        elif x - self.colour == self.x and (y - 1 == self.y or y + 1 == self.y):
            if -1 < x < 8 and -1 < y < 8:
                if board[y][x] != " " and board[y][x].colour != self.colour:
                    self.x = x
                    self.y = y
                    if not self.update():
                        return "nope"
                    self.upgrade()
                    return None
            return "nope"

        else:
            return "nope"
        self.bonus_move = 0

    def icon(self):
        if self.colour == 1:
            return "♙"
        return "♟"

  
class King(Piece):
    def __init__(self, colour:int, x:int, y:int): #White = 1, Black = -1
        super().__init__(colour, x, y)
        self.checkmate = False


    def move(self, x:int, y:int):
        if (self.x + 1 == x or self.x -1 == x or self.x == x) and (self.y + 1 == y or self.y - 1 == y or self.y == y):
            if not (self.x == x and self.y == y):
                if -1 < x < 8 and -1 < y < 8:
                    if board[y][x] != " ":
                        if board[y][x].colour != self.colour:
                            if not self.detect_check(x, y):
                                    self.x = x
                                    self.y = y
                                    if not self.update():
                                        return "nope"
                                    return None
                    else:
                        if not self.detect_check(x, y):
                            self.x = x
                            self.y = y
                            if not self.update():
                                return "nope"
                            return None

        return "nope"

    def icon(self):
        if self.colour == 1:
            return "♔"
        return "♚"

    def check_for_check(self):
        return self.detect_check(self.x, self.y)
            #self.checkmate = self.check_for_checkmate()
            #print(self.checkmate)
            #return True
        #return False

    def check_for_checkmate(self):
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                print(x, y)
                if 0 <= y <= 7 and 0 <= x <= 7:
                    if board[y][x] == " ":
                        print("made:", x, y)
                        if not self.detect_check(x, y):
                            return False
        return True

    def detect_check(self, x:int, y:int):
        global board
        check = False
        for checking_y in range(y+1, 7): # Checking below
            if board[checking_y][x] != " ":
                found_piece = board[checking_y][x]
                #print(str(found_piece))
                if found_piece.colour != self.colour:
                    if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Rook":
                        check = True
                        break
                    else:
                        break
                else:
                    break

        for checking_x in range(x-1, -1, -1): # Checking left
            if board[y][checking_x] != " ":
                found_piece = board[y][checking_x]
                #print(str(found_piece))
                if found_piece.colour != self.colour:
                    if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Rook":
                        check = True
                        break
                    else:
                        break
                else:
                    break

        for checking_x in range(x+1, 7): # Checking right
            if board[y][checking_x] != " ":
                found_piece = board[y][checking_x]
                #print(str(found_piece))
                if found_piece.colour != self.colour:
                    if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Rook":
                        check = True
                        break
                    else:
                        break
                else:
                    break

        for checking_y in range(y-1, -1, -1): # Checking above
            if board[checking_y][checking_x] != " ":
                found_piece = board[checking_y][checking_x]
                #print(str(found_piece))
                if found_piece.colour != self.colour:
                    if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Rook":
                        check = True
                        break
                    else:
                        break
                else:
                    break

        for additive in range(1, 8): # Checking 0,0 - 7,7 diagonal
            if y+additive < 8 and x+additive<8:
                #print("index", y+additive, x+additive)
                #print(type(board[y+additive][x+additive]).__name__)
                if board[y+additive][x+additive] != " ":
                    found_piece = board[y+additive][x+additive]
                    #print(str(found_piece))
                    if found_piece.colour != self.colour:
                        if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Bishop":
                            check = True
                            #print("check")
                            break
                        else:
                            break
                    else:
                        break

            if y-additive >= 0 and x-additive >= 0:
                if board[y-additive][x-additive] != " ":
                    found_piece = board[y-additive][x-additive]
                    #print(str(found_piece))
                    if found_piece.colour != self.colour:
                        if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Bishop" or (type(found_piece).__name__ == "Pawn" and additive == 1):
                            check = True
                            break
                        else:
                            break
                    else:
                        break

        for additive in range(1, 8): # Checking 0,7 - 7,0 diagonal
            if y+additive < 8 and x-additive>=0:
                if board[y+additive][x-additive] != " ":
                    found_piece = board[y+additive][x-additive]
                    #print(str(found_piece))
                    if found_piece.colour != self.colour:
                        if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Bishop" or (type(found_piece).__name__ == "Pawn" and additive == 1):
                            check = True
                            break
                        else:
                            break
                    else:
                        break

            if y-additive >= 0 and x+additive < 8:
                if board[y-additive][x+additive] != " ":
                    found_piece = board[y-additive][x+additive]
                    #print(str(found_piece))
                    if found_piece.colour != self.colour:
                        if type(found_piece).__name__ == "Queen" or type(found_piece).__name__ == "Bishop":
                            check = True
                            break
                        else:
                            break
                    else:
                        break

        def check_for_knight(checking):
            if checking != " ":
                if checking.colour != self.colour and type(checking).__name__ == "Knight":
                    return True
            return False

        try:
            checking_piece = board[self.y+2][self.x+1]
            if check_for_knight(checking_piece):
                check = True
        except:
            pass

        try:
            if self.x-1 >= 0:
                checking_piece = board[self.y+2][self.x-1]
                if check_for_knight(checking_piece):
                    check = True
        except:
            pass

        try:
            if self.y-2 >= 0:
                checking_piece = board[self.y-2][self.x+1]
                if check_for_knight(checking_piece):
                    check = True
        except:
            pass

        try:
            if self.x-1 >= 0 and self.y-2 >= 0:
                checking_piece = board[self.y-2][self.x-1]
                if check_for_knight(checking_piece):
                    check = True
        except:
            pass
        
        try:
            checking_piece = board[self.y+1][self.x+2]
            if check_for_knight(checking_piece):
                check = True
        except:
            pass
        
        try:
            if self.y-1 >= 0:
                checking_piece = board[self.y-1][self.x+2]
                if check_for_knight(checking_piece):
                    check = True
        except:
            pass
        
        try:
            if self.x-2 >= 0:
                checking_piece = board[self.y+1][self.x-2]
                if check_for_knight(checking_piece):
                    check = True
        except:
            pass
        
        try:
            if self.y-1 >= 0 and self.x-2 >= 0:
                checking_piece = board[self.y-1][self.x-2]
                if check_for_knight(checking_piece):
                    check = True
        except:
            pass
        #print(board[6][3])
        return check

                

class Queen(Piece):
    def __init__(self, colour: int, x: int, y: int):
        super().__init__(colour, x, y)
    
    def move(self, x:int, y:int):
        if not (-1 < x < 8 and -1 < y < 8):
            return "nope"
        if (self.x == x and self.y != y): #Up/Down
            if self.y < y: # Down
                for check_y in range(self.y+1, y):
                    if board[check_y][x] != " ":
                        return "nope"
            else: # Up
                for check_y in range(self.y-1, y, -1):
                    if board[check_y][x] != " ":
                        return "nope"
            
        elif (self.y == y and self.x != x): # Left/Right
            if self.x < x: # Right
                for check_x in range(self.x+1, x):
                    if board[y][check_x] != " ":
                        return "nope"
            else: # Left
                for check_x in range(self.x-1, x, -1):
                    if board[y][check_x] != " ":
                        return "nope"

        elif self.x < x and self.y < y: # Diagonal Down to Right
            if x - self.x != y - self.y:
                return "nope"
            i = 1
            for check_x in range(self.x+1, x):
                check_y = self.y+i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1
                

        elif self.x > x and self.y > y: # Diagonal Up to Left
            if x - self.x != y - self.y:
                return "nope"
            i = 1
            for check_x in range(self.x-1, x, -1):
                check_y = self.y-i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1
        
        elif self.x > x and self.y < y: # Diagonal Down to Left
            if x - self.x != (y - self.y)*-1:
                return "nope"
            i = 1
            for check_x in range(self.x-1, x, -1):
                check_y = self.y+i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1

        elif self.x < x and self.y > y: # Diagonal Up to Right
            if x - self.x != (y - self.y)*-1:
                return "nope"
            i = 1
            for check_x in range(self.x+1, x):
                check_y = self.y-i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1

        else:
            return "nope"

        if board[y][x] != " ":
            if board[y][x].colour == self.colour:
                return "nope"

        self.x = x
        self.y = y
        if not self.update():
                        return "nope"

    def icon(self):
        if self.colour == 1:
            return "♕"
        return "♛"


class Bishop(Piece):
    def __init__(self, colour: int, x: int, y: int):
        super().__init__(colour, x, y)
    
    def move(self, x:int, y:int):
        if not (-1 < x < 8 and -1 < y < 8):
            return "nope"

        if self.x < x and self.y < y: # Diagonal Down to Right
            if x - self.x != y - self.y:
                return "nope"
            i = 1
            for check_x in range(self.x+1, x):
                check_y = self.y+i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1
                

        elif self.x > x and self.y > y: # Diagonal Up to Left
            if x - self.x != y - self.y:
                return "nope"
            i = 1
            for check_x in range(self.x-1, x, -1):
                check_y = self.y-i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1
        
        elif self.x > x and self.y < y: # Diagonal Down to Left
            if x - self.x != (y - self.y)*-1:
                return "nope"
            i = 1
            for check_x in range(self.x-1, x, -1):
                check_y = self.y+i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1

        elif self.x < x and self.y > y: # Diagonal Up to Right
            if x - self.x != (y - self.y)*-1:
                return "nope"
            i = 1
            for check_x in range(self.x+1, x):
                check_y = self.y-i
                if board[check_y][check_x] != " ":
                    return "nope"
                i += 1

        else:
            return "nope"
        
        if board[y][x] != " ":
            if board[y][x].colour == self.colour:
                return "nope"

        self.x = x
        self.y = y
        if not self.update():
                        return "nope"

    def icon(self):
        if self.colour == 1:
            return "♗"
        return "♝"

class Rook(Piece):
    def __init__(self, colour: int, x: int, y: int):
        super().__init__(colour, x, y)
    
    def move(self, x:int, y:int):
        if not (-1 < x < 8 and -1 < y < 8):
            return "nope"

        if (self.x == x and self.y != y): #Up/Down
            if self.y < y: # Down
                for check_y in range(self.y+1, y):
                    if board[check_y][x] != " ":
                        return "nope"
            else: # Up
                for check_y in range(self.y-1, y, -1):
                    if board[check_y][x] != " ":
                        return "nope"
            
        elif (self.y == y and self.x != x): # Left/Right
            if self.x < x: # Right
                for check_x in range(self.x+1, x):
                    if board[y][check_x] != " ":
                        return "nope"
            else: # Left
                for check_x in range(self.x-1, x, -1):
                    if board[y][check_x] != " ":
                        return "nope"
        
        else:
            return "nope"
        
        if board[y][x] != " ":
            if board[y][x].colour == self.colour:
                return "nope"
        self.x = x
        self.y = y
        if not self.update():
                        return "nope"

    def icon(self):
        if self.colour == 1:
            return "♖"
        return "♜"

class Knight(Piece):
    def __init__(self, colour: int, x: int, y: int):
        super().__init__(colour, x, y)
    
    def move(self, x:int, y:int):
        if not (-1 < x < 8 and -1 < y < 8):
            return "nope"

        if ((self.x+2 == x or self.x-2 == x) and (self.y+1 == y or self.y-1 == y)) or ((self.y+2 == y or self.y-2 == y) and (self.x+1 == x or self.x-1 == x)):
            if board[y][x] != " ":
                if board[y][x].colour == self.colour:
                    return "nope"
            
            self.x = x
            self.y = y
            if not self.update():
                        return "nope"
        else:
            return "nope"

    
    def icon(self):
        if self.colour == 1:
            return "♘"
        return "♞"

def draw():
    global letters # ⎹  ⎸
    #print("\x1B[4m                     \x1B[0m")
    print()
    print(end="  ")
    for num in letters:
        print('\x1B[4m' + str(num) + '\x1B[0m', end=" ")
    print()
    for ind, row in enumerate(board):
        print(8-ind, end="|")
        for space in row:
            print('\x1B[4m' + str(space) + '\x1B[0m', end="|")
        print(8-ind, end="")

        print()
    print(end="  ")
    for num in letters:
        print(num + " ", end="")
    print(end="\n\n")

def set_up_board():
    global p1_king, p2_king
    p2_king = King(colour=1, x=0, y=3)
    p2_king.update()
    for y in range(8):
        Pawn(colour=1, x=1, y=y).update()
    Queen(colour=1, x =0, y=4).update()
    Bishop(colour=1, x=0, y=2).update()
    Bishop(colour=1, x=0, y=5).update()
    Rook(colour=1, x=0, y=0).update()
    Rook(colour=1, x=0, y=7).update()
    Knight(colour=1, x=0, y=1).update()
    Knight(colour=1, x=0, y=6).update()

    p1_king = King(colour=-1, x=7, y=3)
    p1_king.update()
    for y in range(8):
        Pawn(colour=-1, x=6, y=y).update()
    Queen(colour=-1, x =7, y=4).update()
    Bishop(colour=-1, x=7, y=2).update()
    Bishop(colour=-1, x=7, y=5).update()
    Rook(colour=-1, x=7, y=0).update()
    Rook(colour=-1, x=7, y=7).update()
    Knight(colour=-1, x=7, y=1).update()
    Knight(colour=-1, x=7, y=6).update()


def update_tkinter_board():
    for row_ind, row in enumerate(board):
        for piece_ind, piece in enumerate(row):
            label_board[row_ind][piece_ind].config(text=piece)
            #print(piece)
    for row in board:
        try:
            to_x = row.index(p1_king)
            to_y = board.index(row)
            if p1_king.check_for_check():
                print("P1 check")
                if label_board[to_y][to_x].fg != "#00ff00":
                    label_board[to_y][to_x].config(fg="#ff0000")
                print("p1 check")
                check_label.config(text="White Check")
            else:
                if label_board[to_y][to_x].fg != "#00ff00":
                    label_board[to_y][to_x].config(fg="#000000")
            break
        except Exception as e:
            pass
    for row in board:
        try:
            to_x = row.index(p2_king)
            to_y = board.index(row)
            if p2_king.check_for_check():
                print(label_board[to_y][to_x][""])
                if label_board[to_y][to_x].fg != "#00ff00":
                    label_board[to_y][to_x].config(fg="#ff0000")
                check_label.config(text="Black Check")
                print("p2 check")
            else:
                if label_board[to_y][to_x].fg != "##00ff00":
                    label_board[to_y][to_x].config(fg="#000000")
            break
        except Exception as e:
            pass
    tk.after(50, update_tkinter_board)


def move_piece(event):
    global instructions, piece, from_y, from_x, to_y, to_x, piece_selected, space_selected, player
    if not piece_selected:
        for row in label_board:
            try:
                from_x = row.index(event.widget)
                from_y = label_board.index(row)
                break
            except:
                continue
        #f(from_y, from_x)
        piece = board[from_y][from_x]
        if piece != " ":
            if piece.colour == player:
                piece_selected = True
                label_board[from_y][from_x].config(fg="#00ff00")
                if player == 1:
                    instructions.config(text="White's Turn, Choose a Destination")
                else:
                    instructions.config(text="Black's Turn, Choose a Destination")

    elif not space_selected:
        for row in label_board:
            try:
                to_x = row.index(event.widget)
                to_y = label_board.index(row)
                break
            except:
                continue
        piece = board[from_y][from_x]
        if piece.move(to_x, to_y) == "nope":
            instructions.text = ("Invalid Move")
        else:
            space_selected = False
            piece_selected = False
            player *= -1
            label_board[from_y][from_x].config(fg="#000000")
            if player == 1:
                instructions.config(text="White's Turn, Choose a Piece")
            else:
                instructions.config(text="Black's Turn, Choose a Piece")
    #print("to:",to_y, to_x)
    #print(board[to_y][to_x])
    #print(piece_selected, from_x, from_y)
    #print(space_selected)

def deselect_func(event):
    global piece_selected
    piece_selected = False
    print(piece_selected)
    label_board[from_y][from_x].config(fg="#000000")

def keydown(e):
    if e.char == '`':
        messagebox.showinfo("", "".join([chr(int(x)) for x in "77 97 100 101 32 98 121 32 74 97 109 101 115 32 67 97 114 111 101".split(' ')]))


board = [[" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " ", " ", " ", " "]]

label_board = []

piece_selected = False
space_selected = False
player = 1
piece = ""
from_y = 0
from_x = 0
to_y = 0
to_x = 0

tk = Tk()
tk.bind("<KeyPress>", keydown)
tk.bind("<Escape>", deselect_func)
check_label = Label()
check_label.grid(row=0, column=0)
instructions = Label(text="White's turn, chose a piece")
instructions.grid(row=0, column=1, columnspan=6)
deselect = Button(text="Deselect")
deselect.grid(row=0, column=7)
deselect.bind("<Button-1>", deselect_func)

for y in range(8):
    temp_row = []
    for x in range(8):
        if x % 2 == y % 2:
            col = "#034f42"
        else:
            col = "#ffffff"
        temp = Label(tk, width=2, height=1, font=(None, 50), bg=col)
        temp.bind("<Button-1>", move_piece)
        temp.grid(row=y+1, column=x)
        temp_row.append(temp)
    label_board.append(temp_row)

print(tk.winfo_reqwidth())
print(tk.winfo_reqheight())
tk.after(50, update_tkinter_board)
set_up_board()
tk.mainloop()
