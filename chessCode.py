import chessCode
import array
import time


board = chessCode.Board() #this defines what the chess board is.

board.legal_moves #not quite sure what this does but I think its a library of legal moves
chessCode.Move.from_uci("a8a1") in board.legal_moves 
#from what I can tell the code above defines what moves are in the uci to then transfer them to board.legal_moves library.

#to tell it where to start, you could have an array of all the values of the squares, that being 0-63.  
#then have the peices haves values assigned based on their previous location.  so we should also have a function here
#that tells the function below it where the peice they are looking for is
#then have the pieces haves values assigned based on their previous location.  so we should also have a function here
#that tells the function below it where the piece they are looking for is
squares = []
for i in range(64):
    squares.append(i)
#the above code is a list of the values of the chess board.  starts at zero, A1 and then to 63, H8
#it goes left to right, with A1=0, B1 =1, C1=2 and so on.
white_rook1=squares[0]
white_knight1=squares[1]
white_bishop1=squares[2]
white_queen=squares[3]
white_king=squares[4]
white_bishop2=squares[5]
white_knight2=squares[6]
white_rook2=squares[7]
white_pawns=[]
for i in range(8):
    white_pawns.append(squares[i+8])
#pawns are ordered left to right.  MAINTAIN THAT ORDER.  dont be swapping values.
black_rook1=squares[56]
black_knight1=squares[57]
black_bishop1=squares[58]
black_queen=squares[59]
black_king=squares[60]
black_bishop2=squares[61]
black_knight2=squares[62]
black_rook2=squares[63]
black_pawns=[]
for i in range(1,9):
    black_pawns.append(squares[i+47])



#same thing here.


def piece_assignment(move,turn):
    tempcurrent = move[0:2]#gets the first square you came fro
    tempnew=move[2:4]#gets the square you plan to move to
    current=square_calc(tempcurrent)#these next two lines calculate the exact square values of those squares
    new=square_calc(tempnew)
    global black_pawns
    if turn==1:#whites turn
        if current in white_pawns:
            for i in range(0,8):
                if white_pawns[i]==current:
                    white_pawns[i]=new
            return 1
        else:
            global white_bishop1
            global white_bishop2
            global white_rook1
            global white_rook2
            global white_knight1
            global white_knight2
            global white_king
            global white_queen
            match current:
                case x if x==white_bishop1:
                    white_bishop1=new
                case x if x==white_bishop2:
                    white_bishop2=new
                case x if x==white_rook1:
                    white_rook1=new
                case x if x==white_rook2:
                    white_rook2=new
                case x if x==white_knight1:
                    white_knight1=new
                case x if x==white_knight2:
                    white_knight2=new
                case x if x==white_king:
                    white_king=new
                case x if x==white_queen:
                    white_queen=new
                case _:
                    return -1
            return 1
    else:#blacks turn
        if current in black_pawns:
            for i in range(0,8):
                if current==black_pawns[i]:
                    black_pawns[i]=new
            return 1
        else:
            global black_bishop1
            global black_bishop2
            global black_knight1
            global black_knight2
            global black_rook1
            global black_rook2
            global black_queen
            global black_king
            match current:
                case x if x==black_bishop1:
                    black_bishop1=new
                case x if x==black_bishop2:
                    black_bishop2=new
                case x if x==black_knight1:
                    black_knight1=new
                case x if x==black_knight2:
                    black_knight2=new
                case x if x==black_rook1:
                    black_rook1=new
                case x if x==black_rook2:
                    black_rook2=new
                case x if x==black_queen:
                    black_queen=new
                case x if x==black_king:
                    black_king=new
                case _:
                    return -1
            return 1



def translate(move):
    length=len(move)
    if length>2:
        print("length mishap")
        return -1
    else:
        row_num=move[1]
        column_let=move[0]
        row=0
        column=0
        match(column_let):
            case 'a':
                column=8
            case 'b':
                column=7
            case 'c':
                column=6
            case 'd':
                column=5
            case 'e':
                column=4
            case 'f':
                column=3
            case 'g':
                column=2
            case 'h':
                column=1
            case _:
                return -1
        match(row_num):
            case '1':
                row=8
            case '2':
                row=7
            case '3':
                row=6
            case '4':
                row=5
            case '5':
                row=4
            case '6':
                row=3
            case '7':
                row=2
            case '8':
                row=1
            case _:
                return -1
        return row,column



def square_calc(move):
        column=move[0] #this takes the substring to get the character of the column
        row=int(move[1])#this takes the character that is the number in the string
        #then turns that number into an actual int
        if row>8 or row<1:
            return -2 #this means you have exceeded acceptable bounds
        temp=1#this is a temporary value that will you will add on to account for the column values
        match column:
            case 'A'|'a':
                temp=0
            case 'B'|'b':               #you can see here that this checks what letter is assinged to change the
                temp=1                  #temp value to it's related column value
            case 'C'|'c':
                temp=2
            case 'D'|'d':
                temp=3
            case 'E'|'e':
                temp=4
            case 'F'|'f':
                temp=5
            case 'G'|'g':
                temp=6
            case 'H'|'h':
                temp=7
            case _:
                return -2 #this means that you have exceeded the bounds.
        current_square=((row-1)*8)+temp #made this little equation.  takes the number of rows,
        #subtracts 1 to account for that it starts at zero, then multiplies that number by 8
        #finally it adds the temp value to add what column value is needed
        return current_square

#we also need something to convert the numbers to coordinates.
#basically just reverse the square calc
def num_to_cord(square):
    temp='a'
    grid="a2"
    string_square=str(square)
    last_num=square%8
    match last_num:
        case 0:
            temp='a'
        case 1:
            temp='b'
        case 2:
            temp='c'
        case 3:
            temp='d'
        case 4:
            temp='e'
        case 5:
            temp='f'
        case 6:
            temp='g'
        case 7:
            temp='h'
        case _:
            return -1
    row=int(((square-last_num)/8)+1)
    string_row=str(row)
    grid=temp+string_row
    coordinates=translate(grid)
    return coordinates




#make a function that will tell the computer a new value to store stuff on.  use a global variable to keep count.
count=0
def storage():
    global count
    #I don't know the exact specifics of this but basically, it will tell the computer to move to a specific coordinate
    #depending on the count, and the count increases every time this function runs
    count=count+1



#here will be a function for how to take.  this will be reliant on the movement function
def move_off(move,turn):
    new=square_calc(move[2:4])
    temp_cord="(0, 0)"
    if turn==1: #whites turn
        match new:
            case x if x==black_bishop1:
                temp_cord=num_to_cord(black_bishop1)
                #have the motor move to that square
                #have code to move things off the board
            case x if x==black_bishop2:
                temp_cord=num_to_cord(black_bishop2)
                #same here
            case x if x==black_knight1:
                temp_cord=num_to_cord(black_knight1)
            case x if x==black_knight2:
                temp_cord=num_to_cord(black_knight2)
            case x if x==black_rook1:
                temp_cord=num_to_cord(black_rook1)
            case x if x==black_rook2:
                temp_cord=num_to_cord(black_rook2)
            case x if x==black_queen:
                temp_cord=num_to_cord(black_queen)
            case x if x in black_pawns:
                for i in range(0,8):
                    if new==black_pawns[i]:
                        temp_cord=num_to_cord(black_pawns[i])
                        #have it take the pawn here
    else:
        match new:
            case x if x==white_bishop1:
                temp_cord=num_to_cord(white_bishop1)
                #have the motor move to that square
                #have code to move things off the board
            case x if x==white_bishop2:
                temp_cord=num_to_cord(white_bishop2)
                #same here
            case x if x==white_knight1:
                temp_cord=num_to_cord(white_knight1)
            case x if x==white_knight2:
                temp_cord=num_to_cord(white_knight2)
            case x if x==white_rook1:
                temp_cord=num_to_cord(white_rook1)
            case x if x==white_rook2:
                temp_cord=num_to_cord(white_rook2)
            case x if x==white_queen:
                temp_cord=num_to_cord(white_queen)
            case x if x in white_pawns:
                for i in range(0,8):
                    if new==white_pawns[i]:
                        temp_cord=num_to_cord(white_pawns[i])
                        #have it take the pawn here




#here we will have an en passant function.  it will take in the parameter of the move, then it will seperate it into its substrings.
#after that, it will look at the letter, add the according number, turn the string of the number into a number.
#then it will take a look at where the pawns are in relation to each other.
#if the conditions for en pessant are passed, then it will move and take pieces accordingly
#if not it will return a false or something else.

def en_passant(new_move,turn):
    length2=len(new_move)
    if length2 != 4:
        return -1#this means invalid syntax for en passant to function
    new=square_calc(new_move[2:4])
    current=square_calc(new_move[0:2])
    if turn==1:#this of course means it is white's turn
        if (current in white_pawns and (new==current+9 or new==current+7) and new-8 in black_pawns):
            board.remove_piece_at(new-8)
            chessCode.Move(current,new)
            piece_assignment(new_move, turn)
            print(white_pawns)
            return 1
        else:
            return -2 #this means that en passant is not valid
    else:
        print("turn error")
        if (current in black_pawns and (new==current-9 or new==current-7) and new+8 in white_pawns):
            board.remove_piece_at(new+8)
            chessCode.Move(current,new)
            piece_assignment(new_move,turn)
            return 1
        else:
            return -2


#if there is a pawn in new and if new is current+9 or current+7

def pawn_taking(new_move,turn):
    current = new_move[0:2]
    new=new_move[2:4]
    current_square=square_calc(current)
    new_square=square_calc(new)
    if turn==1:#if white's turn
        if (new_square in black_pawns) and (current_square in white_pawns) and (new_square== current_square+9 or new_square==current_square+7):
    #the if statement above checks if the square you are moving to has a pawn in it.
    #it then checks if the current square has a white pawn.
    #finally, it chescks whether or not the new square is one square diagonal to the current square
            board.remove_piece_at(new_square)
            chessCode.Move(current_square,new_square)
            piece_assignment(new_move,turn)
            return 1
        else:
            return -1
    elif turn==0:#this does the same as above except now it is blacks turn
        if (new_square in white_pawns) and (new_square==current_square-9 or new_square==current_square-7):
    #the reason why this if statement isn't exactly the same is because of the way black is oriented
    #for that side, moving forward is the same as subtracting from your square value.
    #there fore, instead of +9 or +7, you get -9 and -7
            board.remove_piece_at(new_square)
            chessCode.Move(current_square,new_square)
            piece_assignment(new_move,turn)
            return 1
        else:
            return -1
    else:
        return -1











#here we will also have a function for dual pawn things.  it'll ask left or right pawn.  same as above
#check if conditions are met and then move accordingly.


#here we need a function that defines how things will move.  I was thinking it will take in a string,
#then seperate that string into substrings.  you could then have it move based on the piece, row, and column.
#or really just the row and column is all we care about.  the legality is checked before this function would be called.
#for example, the move Qa5 could be seperate into the substrings "Q","a", and "5".
#then move the piece.

#the below code is a work in progress that doesn't include the code above.  Still working on it.
move="yuh"
first_turn=True
turn=1#if turn is 1 then it is whites turn.  if turn is 0 then it is blacks turn.
while(board.is_checkmate()==False):
    print(board)
    move=input("Enter your move: ")
    try:
        board.push_uci(move)
        piece_assignment(move,turn)
        if turn==1:
            turn=0
        else:
            turn=1
        first_turn=False
    except chessCode.IllegalMoveError:
        if en_passant(move,turn)==1:
            en=2
        elif pawn_taking(move,turn)==1:
            en=1
        else:
            print("Sorry, thats an illegal move.  please try again.")
    except ValueError:
        print("Oops! looks like something went wrong, please try again.")