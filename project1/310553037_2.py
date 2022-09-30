from calendar import isleap
from copy import copy
from re import S
import numpy as np
import copy
row,col = 10,5 #board size

class AI():
    def __init__(self):
     
        self.gameover = False
        self.board = np.zeros([row,col], dtype=int)
        self.stable = True #False:need to clean
        self.step = 0 #total turns , start from 0
        self.turn = -1 
        self.mypoints = 0
        self.oppopoints = 0
        self.board = np.loadtxt("board2.txt", dtype= int)
        
        # #make board
        # tmp = (np.arange(row)/2)+1
        # while(1):
        #     for i in range(col):
        #         np.random.shuffle(tmp)
        #         self.board[:,i] = tmp
        #     if self.checkstable() == True:
        #         break
        # self.show_board()
        
    def checkstable(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])-2):
                if abs(self.board[r][c]) == abs(self.board[r][c+1]) == abs(self.board[r][c+2]) != 0:
                    self.stable = False
                    return self.stable
        self.stable = True
        return self.stable

    def drop(self): # drop the tile 
        for c in range(col):
            if self.board[:,c].sum()!=0:
                k = -len(self.board[:,c][self.board[:,c]>0])
                self.board[k:,c] = self.board[:,c][self.board[:,c]>0]
                self.board[:k,c] = 0

    def checkgameover(self): #any of last row == 0
        self.gameover = np.any(self.board[-1] == 0)
        return self.gameover

    def clean(self): #clean the tile , return points
        unstable = 1
        points = 0
        while(unstable):
            unstable = 0
            for i in range(row):
                for j in range(col-2):
                    if abs(self.board[i][j]) == abs(self.board[i][j+1]) == abs(self.board[i][j+2]) != 0:
                        self.board[i][j] = self.board[i][j+1] = self.board[i][j+2] = -abs(self.board[i][j])
                        unstable = 1
            points -= self.board[self.board<0].sum()
            self.board[self.board<0] = 0
            self.drop()
        self.checkgameover()        
        return points
        
    def check_last(self, length) :
        isLast = False
        pts = 0
        x, y = -1, -1
        for i in range(col) :
            temp_b = self.board[:, i]
            if len(temp_b[temp_b > 0]) == length :
                isLast = True
                if length == 2 :
                    if self.board[ row - 2 ][ i ] + self.board[ row - 1 ][ i ] > pts :
                        pts = self.board[ row - 2 ][ i ] + self.board[ row - 1 ][ i ]
                        x = row - 2
                        y = i
                else :
                    if self.board[ row - 1 ][ i ] > pts :
                        pts = self.board[ row - 1 ][ i ]
                        x = row - 1
                        y = i
        if isLast:
            if ( self.mypoints >= self.oppopoints ) | ( self.mypoints + pts >= self.oppopoints ) :
                return x, y
        return -1, -1

    def fake_select(self, x, y) :
        pts = self.board[x][y]
        self.board[1:x + 1,y] = self.board[:x,y]
        self.board[0][y] = 0
        if self.board[:, y].sum() == 0 :
            return pts 
        unstable = 1
        while(unstable):
            unstable = 0
            for a in range(row):
                for b in range(col-2):
                    if abs(self.board[a][b]) == abs(self.board[a][b+1]) == abs(self.board[a][b+2]) != 0:
                        self.board[a][b] = self.board[a][b+1] = self.board[a][b+2] = -abs(self.board[a][b])
                        unstable = 1
            pts -= self.board[self.board<0].sum()
            self.board[self.board<0] = 0
            self.drop()            
        return pts

    def pred_oppppts(self, gap):
        max_pts = -1
        for x in range(row) :
            for y in range(col) :
                if self.board[x][y] == 0 :
                    continue
                temp = copy.copy(self.board)
                pts = self.fake_select(x, y)
                last_row = self.board[row - 1, :]
                if len(last_row[last_row == 0]) != 0 :
                    if pts > max_pts :
                        if pts >= gap :
                                self.board = copy.copy(temp) 
                                return 0 
                        max_pts = pts
                            
                else :
                    if pts >= gap :
                        self.board = copy.copy(temp) 
                        return 0
                    for a in range(row) :
                        for b in range(col) :
                            if self.board[a][b] == 0 :
                                continue
                            temp2 = copy.copy(self.board)
                            pts2 = self.fake_select(a, b)
                            if pts + pts2 > max_pts :
                                max_pts = pts + pts2
                                if max_pts >= gap :
                                    self.board = copy.copy(temp) 
                                    return 0      

                            self.board = copy.copy(temp2)
                self.board = copy.copy(temp) 
        return max_pts  

    def first_opPts(self) :
        max_pts = -1
        for x in range(row) :
                for y in range(col) :
                    if self.board[x][y] == 0 :
                        continue
                    temp3 = copy.copy(self.board)
                    pts = self.fake_select(x, y)
                    if self.board[:, y].sum() == 0 :
                        if pts > max_pts :
                            max_pts = pts
                    else :
                        for a in range(row) :
                            for b in range(col) :
                                if self.board[a][b] == 0 :
                                    continue
                                temp4 = copy.copy(self.board)
                                pts2 = self.fake_select(a, b)
                                if pts + pts2 > max_pts :
                                    max_pts = pts + pts2
                                self.board = copy.copy(temp4)
                    self.board = copy.copy(temp3)  
        return max_pts                               

    def second_move(self, x, y) :
        new_x, new_y = self.check_last(1) 
        if new_x != -1 and new_y != -1 :
            return new_x, new_y
        return x, y
    
    def make_decision(self):
        #######################################################
        ##### This is the main part you need to implement #####
        #######################################################        
        
        x, y = -1, -1
        second_x, second_y = -1, -1
        last_x, last_y = self.check_last(1)
        if last_x != -1 and last_y != -1 :
            return last_x, last_y, 0, 0

        last_x, last_y = self.check_last(2)
        if last_x != -1 and last_y != -1 :
            second_x = last_x + 1
            second_y = last_y
            return last_x, last_y, second_x, second_y

        gap = -1000   
        op_pts = 0  
        for i in range(row) :
            for j in range(col) :
                if self.board[i][j] == 0 :
                    continue
                temp = copy.copy(self.board)
                pts = self.fake_select(i, j)
                last_row = self.board[row-1, :]
                if len(last_row[last_row == 0]) != 0 :
                    if pts > gap :
                            gap = pts
                            x = i
                            y = j
                            second_x = 0
                            second_y = 0
                    self.board = copy.copy(temp)
                    continue
                for a in range(row) :
                    for b in range(col) :
                        if self.board[a][b] == 0 :
                            continue
                        temp2 = copy.copy(self.board)
                        sndPts = self.fake_select(a, b)

                        if pts + sndPts - gap <= 2 :
                            self.board = copy.copy(temp2)                            
                            continue 

                        if self.board[:, b].sum() == 0 :
                            if pts + sndPts > gap :
                                gap = pts + sndPts
                                x = i
                                y = j
                                second_x = a
                                second_y = b
                            self.board = copy.copy(temp2)
                            continue
                            
                        else :    
                            if gap == -1000 :                         
                                op_pts = self.first_opPts()
                            else :
                                op_pts = self.pred_oppppts(pts + sndPts - gap)

                        if op_pts == 0 :
                            self.board = copy.copy(temp2)
                            continue

                        if pts + sndPts - op_pts > gap :
                            gap = pts + sndPts - op_pts 
                            x = i
                            y = j
                            second_x = a
                            second_y = b
                        self.board = copy.copy(temp2)
                self.board = copy.copy(temp)
        return x, y, second_x, second_y
        
        # return format : [x,y]
        # Use AI to make decision !
        # random is only for testing !
    
    def rand_select(self):
        p = 0
        while not(p):
            x= np.random.randint(row)
            y= np.random.randint(col)
            p = self.board[x][y]
        return [x,y]

    def make_move(self, x, y):
        pts = self.board[x][y]
        self.board[1:x+1,y] = self.board[0:x,y]
        self.board[0][y] = 0

        if self.checkgameover(): 
            return pts
        
        pts += self.clean()
        return pts
        
    def start(self):
        print("Game start!")      
        print('――――――――――――――――――')
        self.show_board()
        self.turn = int(input("Set the player's order(0:first, 1:second): "))
        second_x, second_y = -1, -1

        #start playing    
        while not self.gameover:
            print('Turn:', self.step)
            if ((self.step%4)//2) == self.turn:
                print('It\'s your turn')
                if self.step % 4 == 0 or self.step % 4 == 2:
                    x, y, second_x, second_y = self.make_decision()
                else :
                    x, y = self.second_move(second_x, second_y)
                print(f"Your move is {x},{y}.")
                #[x,y] = [int(x) for x in input("Enter the move : ").split()]
                assert (0<=x and x<=row-1 and 0<=y and y<=col-1)
                assert (self.board[x][y]>0)
                pts = self.make_move(x,y)
                self.mypoints += pts
                print(f'You get {pts} points')  
                self.show_board()

            else:
                print('It\'s opponent\'s turn')
                #x,y = self.rand_select() # can use this while testing ,close it when you submit
                [x,y] = [int(x) for x in input("Enter the move : ").split()] #open it when you submit
                assert (0<=x and x<=row-1 and 0<=y and y<=col-1)
                assert (self.board[x][y]>0)
                print(f"Your opponent move is {x},{y}.")
                pts = self.make_move(x,y)
                self.oppopoints += pts
                print(f'Your opponent\'s get {pts} points')
                self.show_board()

            self.step += 1

        #gameover
        if self.mypoints > self.oppopoints:
            print('You win!')
            return 1
        elif self.mypoints < self.oppopoints:
            print('You lose!')
            return -1
        else:
            print('Tie!')
            return 0

    def show_board(self):
        print('my points:', self.mypoints)
        print('opponent\'s points:', self.oppopoints)
        print('The board is :')
        print(self.board)
        print('――――――――――――――――――')

if __name__ == '__main__':
 
    game = AI()
    game.start()
