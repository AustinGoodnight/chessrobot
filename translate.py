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
                column=9
            case 'b':
                column=8
            case 'c':
                column=7
            case 'd':
                column=6
            case 'e':
                column=5
            case 'f':
                column=4
            case 'g':
                column=3
            case 'h':
                column=2
            case _:
                return -1
        match(row_num):
            case '1':
                row=1
            case '2':
                row=2
            case '3':
                row=3
            case '4':
                row=4
            case '5':
                row=5
            case '6':
                row=6
            case '7':
                row=7
            case '8':
                row=8
            case _:
                return -1
        return row,column

