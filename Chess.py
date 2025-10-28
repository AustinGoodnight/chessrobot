import chess
import time
import gpiozero
import array
import pathfinding

board = chess.Board() #this defines what the chess board is.

board.legal_moves #not quite sure what this does but I think its a library of legal moves
chess.Move.from_uci("a8a1") in board.legal_moves 
#from what I can tell the code above defines what moves are in the uci to then transfer them to board.legal_moves library.

#to tell it where to start, you could have an array of all the values of the squares, that being 0-63.  
#then have the peices haves values assigned based on their previous location.  so we should also have a function here
#that tells the function below it where the peice they are looking for is
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

def peice_assignment(move,turn):
    tempcurrent = move[0:2]#gets the first square you came fro
    tempnew=move[2:4]#gets the square you plan to move to
    current=square_calc(tempcurrent)#these next two lines calculate the exact square values of those squares
    new=square_calc(tempnew)
    if(len(move)>2):#I now realize that this is useless because I moved to UCI move sets.  Ill have to adjust that.
        piece=move[0]
        if turn==1:#white's turn
            match piece:
                case 'K'|'k':
                    global white_king
                    white_king=new
                case 'Q'|'q':
                    global white_queen
                    white_queen=new
                case 'N'|'n':
                    global white_knight1
                    if(white_knight1==current):
                        white_knight1=new
                    else:
                        global white_knight2
                        white_knight2=new
                case 'B'|'b':
                    global white_bishop2
                    global white_bishop1
                    if(white_bishop1==current):
                        white_bishop1=new
                    else:
                        white_bishop2=new
                case 'R'|'r':
                    global white_rook1
                    global white_rook2
                    if(white_rook1==current):
                        white_rook1=new
                    else:
                        white_rook2=new
                case _:
                    return -1
        else:
            match piece:
                case 'K'|'k':
                    global black_king
                    black_king=new
                case 'Q'|'q':
                    global black_queen
                    black_queen=new
                case 'N'|'n':
                    global black_knight1
                    global black_knight2
                    if(black_knight1==current):
                        black_knight1=new
                    else:
                        black_knight2=new
                case 'B'|'b':
                    global black_bishop1
                    global black_bishop2
                    if(black_bishop1==current):
                        black_bishop1=new
                    else:
                        black_bishop2=new
                case 'R'|'r':
                    global black_rook1
                    global black_rook2
                    if(black_rook1==current):
                        black_rook1=new
                    else:
                        black_rook2=new
                case _:
                    return -1
    elif len(move)==2:
        if turn==1:
            for i in range(0,8):
                if current==white_pawns[i]:
                    white_pawns[i]=new
        else:
            for i in range(0,8):
                if current==black_pawns[i]:
                    black_pawns[i]=new
    else:
        return -1#this means that this not a valid move.  shouldn't be a problem, normally.





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



        
#here will be a function for how to take.  this will be reliant on the movement function

#here we will have an en passant function.  it will take in the parameter of the move, then it will seperate it into its substrings.
#after that, it will look at the letter, add the according number, turn the string of the number into a number.
#then it will take a look at where the pawns are in relation to each other.
#if the conditions for en pessant are passed, then it will move and take pieces accordingly
#if not it will return a false or something else.

def en_passant(new_move,turn):
    length2=len(new_move)
    if length2 != 4:
        print("length error")
        return -1#this means invalid syntax for en passant to function
    new=square_calc(new_move[0:2])
    current=square_calc(new_move[2:4])
    if turn==1:#this of course means it is white's turn
        print("whites turn")
        if (current in white_pawns and (new==current+9 or new==current+9) and new-8 in black_pawns):
            print("should work")
            board.remove_piece_at(new-8)
            chess.Move(current,new)
            peice_assignment(new_move, turn)
            return 1
        else:
            print("if statement error")
            return -2 #this means that en passant is not valid
    else:
        print("turn error")
        if (current in black_pawns and (new==current-9 or new==current-7) and new+8 in white_pawns):
            board.remove_piece_at(new+8)
            chess.Move(current,new)
            peice_assignment(new_move,turn)
            return 1
        else:
            return -2
        
#if there is a pawn in new and if new is current+9 or current+7

def pawn_taking(new_move,turn):
    current = new_move[0,2]
    new=new_move[2,4]
    current_square=square_calc(current)
    new_square=square_calc(new)
    if turn==1:#if white's turn
        if (new_square in black_pawns) and (current_square in white_pawns) and (new_square== current_square+9 or new_square==current_square+7):
            #the if statement above checks if the square you are moving to has a pawn in it.
            #it then checks if the current square has a white pawn.
            #finally, it chescks whether or not the new square is one square diagonal to the current square
            board.remove_piece_at(new_square)
            chess.Move(current_square,new_square)
            peice_assignment(new_move,turn)
            return 1
        else:
            return -1
    elif turn==0:#this does the same as above except now it is blacks turn
        if (new_square in white_pawns) and (new_square==current_square-9 or new_square==current_square-7):
            #the reason why this if statement isn't exactly the same is because of the way black is oriented
            #for that side, moving forward is the same as subtracting from your square value.
            #there fore, instead of +9 or +7, you get -9 and -7
            board.remove_piece_at(new_square)
            chess.Move(current_square,new_square)
            peice_assignment(new_move,turn)
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
        peice_assignment(move,turn)
        if turn==1:
            turn=0
        else:
            turn=1
            first_turn=False
    except chess.IllegalMoveError:
        if en_passant(move,turn)==1:
            en=2
        elif pawn_taking(move,turn)==1:
            en=1
        else:
            print("Sorry, thats an illegal move.  please try again.")
    except ValueError:
        print("Oops! looks like something went wrong, please try again.")
            



