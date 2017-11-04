import numpy as np

def plot_sudoku(arr):
    for i in range(0,9,1):
        for j in range(0,9,1):
            print(arr[i,j] ),
        print


def solve(arr):

    for i in range(0,9,1):
        for j in range(0,9,1):
            if arr[i][j] == 0:
                #empty space found, save position
                pos = [i,j]

                #check for number placement
                for num in range(1,10,1):
                    if is_safe(num,pos,arr):
                        #place number
                        arr[i][j] = num
                        #solve for the rest of the grid
                        if solve(arr):
                            return True
                        else:
                            #if no solution found, find the next number for placement
                            arr[i,j] = 0
                            continue
                return False
    #no empty space found, Sudoku solved!
    return True


def is_safe(num,pos,arr):
    #check row & col & box
    return safe_row(num,pos[0],arr) and safe_col(num,pos[1],arr) and safe_box(num,pos,arr)

def safe_row(num,ind,arr):
    return not(num in arr[ind,:])

def safe_col(num,ind,arr):
    return not(num in arr[:,ind])

def safe_box(num,pos,arr):

    #find  3 x 3  box indexes
    box_row = 3*(pos[0] / 3)
    box_col = 3*(pos[1] / 3)

    return not(num in arr[box_row:box_row+3,box_col:box_col+3])

if __name__=="__main__":
    print("Sudoku Solver\n");
    # creating a 2D array for the grid
    grid=[[0 for x in range(9)]for y in range(9)]
    #input grid
    grid = np.array([[3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]])
    if  solve(grid):
        print("Sudoku Solved!\n")
        plot_sudoku(grid)
    else:
        print("No solution found\n")