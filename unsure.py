
import sys
import chess
import chess.engine

ENGINE_PATH = "stockfish" #connects to stockfish on system path

def locationOnEdge(x1,y1,x2,y2):
    #goes from 0,0 to x1,y1
    #grabs piece then goes to x2,y2
    #then goes back to 0,0
    #all along the edges
    motorController(.5,'x') # to edge
    motorController(.5,'y') # to edge
    motorController(x1-1,'x')
    motorController(y1-1,'y')
    motorController(.5,'x') # to center
    motorController(.5,'y') # to center
    mag.on()
    time.sleep(.5)
    motorController(-.5,'x') # back to edge
    motorController(-.5,'y') # back to edge
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    motorController(.5,'x') # to center
    motorController(.5,'y') # to center
    mag.off()
    motorController((-x2),'x') # back to edge
    motorController((-y2),'y') # back to edge
    '''
    motorController((-x2)+1,'x')
    motorController((-y2)+1,'y')
    #motorController(-.5,'x') # to (0,0)
    motorController(-.5,'y') # to (0,0)
    '''

def locationOffEdge(x1,y1,x2,y2):
    motorController(x1,'x')
    motorController(y1,'y')
    mag.on()
    time.sleep(2)
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    mag.off()
    motorController(-x2,'x')
    motorController(-y2,'y')


def edgeTraceX():
    mag.on()
    motorController(1.5,'y')
    motorController(8, 'x')

    time.sleep(5)
    motorController(-8,'x')
    motorController(-1.5,'y')
    mag.off()

def edgeTraceY():
    mag.on()
    motorController(1.5,'x')
    motorController(8, 'y')

    time.sleep(5)
    motorController(-8,'y')
    motorController(-1.5,'x')
    mag.off()

def spaceTest():
    mag.on()
    motorController(9,'y')
    for i in range(8):
        motorController(1, 'x')
        time.sleep(2)

    motorController(-8,'x')
    motorController(-9,'y')

def translatey(y):
    #char input
    if y == 'a':
        yout = 1
    if y == 'b':
        yout = 2
    if y == 'c':
        yout = 3
    if y == 'd':
        yout = 4
    if y == 'e':
        yout = 5
    if y == 'f':
        yout = 6
    if y == 'g':
        yout = 7
    if y == 'h':
        yout = 8
    return yout

def translatex(x):
    return 9-x

def send_move_to_physical_board(move_uci: str, is_capture: bool):
    """
    Hook for your motor/robot controller.

    Parameters
    ----------
    move_uci : str
        Move in UCI form, e.g. "e2e4", "g1f3", "e7e8q", "e1g1".
    is_capture : bool
        True if the move captures a piece, False otherwise.

    Replace the body of this function with whatever your
    physical board controller expects (serial, socket, etc.).
    """
    # TODO: Replace this stub with your real communication
    print(f"[ROBOT] move={move_uci}, capture={is_capture}")


# ---------------------------------------------
# UTILS
# ---------------------------------------------

def print_board_and_status(board: chess.Board):
    print(board)
    print()
    print(f"FEN: {board.fen()}")
    print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
    print(f"Move number: {board.fullmove_number}")
    if board.is_check():
        print("Check!")
    print("-" * 40)


def get_user_move(board: chess.Board) -> chess.Move:
    """
    Get a *legal* move in UCI from stdin.
    """
    while True:
        user_input = input("Your move (UCI, e.g. e2e4, or 'q' to quit): ").strip()

        if user_input.lower() in ("q", "quit", "exit"):
            print("User quit the game.")
            sys.exit(0)

        try:
            move = chess.Move.from_uci(user_input)
        except ValueError:
            print("Invalid UCI format. Example: e2e4, g1f3, e7e8q.")
            continue

        if move not in board.legal_moves:
            print("Illegal move for this position. Try again.")
            continue

        return move


# ---------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------

def main():
    # Human is White, engine is Black
    board = chess.Board()

    # Start Stockfish as a UCI engine
    try:
        engine = chess.engine.SimpleEngine.popen_uci([ENGINE_PATH])
    except FileNotFoundError:
        print(f"Could not start engine at path: {ENGINE_PATH}")
        print("Make sure Stockfish is installed and ENGINE_PATH is correct.")
        return

    print("Starting new game: You (White) vs Stockfish (Black)")
    print("Enter moves in UCI format, e.g. e2e4, g1f3, e7e8q.")
    print("-" * 40)

    try:
        while not board.is_game_over():
            print_board_and_status(board)

            if board.turn == chess.WHITE:
                # --------------------------
                # HUMAN MOVE
                # --------------------------
                move = get_user_move(board)
                move_uci = move.uci()
                is_capture = board.is_capture(move)

                board.push(move)
                send_move_to_physical_board(move_uci, is_capture)

            else:
                # --------------------------
                # ENGINE MOVE
                # --------------------------
                print("Engine thinking...")

                # Time control for engine; adjust as you like
                result = engine.play(board, chess.engine.Limit(time=0.5))
                move = result.move

                if move is None:
                    print("Engine has no move (checkmate/stalemate).")
                    break

                move_uci = move.uci()
                is_capture = board.is_capture(move)

                print(f"Engine plays: {move_uci}")
                board.push(move)
                send_move_to_physical_board(move_uci, is_capture)

        # ------------------------------
        # GAME OVER
        # ------------------------------
        print_board_and_status(board)
        print("Game over.")
        print(f"Result: {board.result()}")
        if board.is_checkmate():
            print("Checkmate.")
        elif board.is_stalemate():
            print("Stalemate.")
        elif board.is_insufficient_material():
            print("Draw by insufficient material.")
        elif board.can_claim_fifty_moves():
            print("Draw (50-move rule).")
        elif board.can_claim_threefold_repetition():
            print("Draw (threefold repetition).")

    finally:
        engine.quit()


if __name__ == "__main__":
    main()
