from math import fabs
from re import M
from tabnanny import check
import numpy as np
import copy
row,col = 6,3 #board size

class AI():
    def __init__(self):
     
        self.gameover = False
        self.board = np.zeros([row,col], dtype=int)
        self.stable = True #False:need to clean
        self.step = 0 #total turns , start from 0
        self.turn = -1 
        self.mypoints = 0
        self.oppopoints = 0
        self.board = np.loadtxt("board.txt", dtype= int)
        
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

    def pred_oppppts(self):
        temp_12 = [0,0]
        temp_13 = [0,0]
        temp_23 = [0,0]   
        max_point = 0
        for i in range(row):
            if i == 0:
                continue
            for j in range(col-2):
                #1 & 2
                if self.board[i][j] == self.board[i][j+1] != self.board[i][j+2] :
                    if self.board[i][j] == self.board[i-1][j+2] != 0:
                        temp_12[0] += self.board[i][j]
                        temp_12[1] = i
                #1 & 3
                elif self.board[i][j] == self.board[i][j+2] != self.board[i][j+1] :
                    if self.board[i][j] == self.board[i-1][j+1] != 0:
                        temp_13[0] += self.board[i][j]
                        temp_13[1] = i
                #2 & 3
                elif self.board[i][j+1] == self.board[i][j+2] != self.board[i][j]:
                    if self.board[i][j+1] == self.board[i-1][j] != 0:
                        temp_23[0] += self.board[i][j+1]
                        temp_23[1] = i
                #check single maximum
                if self.board[i][j] > max_point :
                    max_point = self.board[i][j]
                if j == col - 3 :
                    if self.board[i][j+1] > max_point :
                        max_point = self.board[i][j+1]

                    if self.board[i][j+2] > max_point :
                        max_point = self.board[i][j+2]

        if temp_12 == temp_13 == temp_23 == 0:
            return max_point
        temp_12[0] = temp_12[0] * 3 + max(self.board[temp_12[1]:, 2])
        temp_13[0] = temp_13[0] * 3 + max(self.board[temp_13[1]:, 1])
        temp_23[0] = temp_23[0] * 3 + max(self.board[temp_23[1]:, 0])
        max_point = max(temp_12[0], temp_13[0], temp_23[0])
        return max_point

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


    def make_decision(self):
        #######################################################
        ##### This is the main part you need to implement #####
        #######################################################

        #check whether to end the  game
        last = False
        last_pts = 0
        last_x, last_y = -1, -1
        for i in range( col ) :
            temp_b = self.board[:, i]
            if len(temp_b[temp_b > 0]) == 1 :
                last = True
                if self.board[ row - 1 ][ i ] > last_pts :
                    last_pts = self.board[ row - 1 ][ i ]
                    last_x = row - 1
                    last_y = i
        if last:
            if ( self.mypoints >= self.oppopoints ) | ( self.mypoints + last_pts >= self.oppopoints ) :
                return [ last_x, last_y ]
                
        #find the best move
        gap = -100
        best_x, best_y = -1, -1
        for i in range( row ) :
            for j in range ( col ) :
                if self.board[i][j] == 0 :
                    continue
                temp = copy.copy(self.board)
                pts = self.fake_select(i, j)
                if self.board[:, j].sum() == 0 :
                    if pts > gap :
                        gap = pts
                    self.board = copy.copy(temp)
                    continue
         
                op_pts = self.pred_oppppts()    

                if gap < pts - op_pts :
                    gap = pts - op_pts
                    best_x = i
                    best_y = j

                self.board = copy.copy(temp)
        return [best_x, best_y]
                
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


        #start playing    
        while not self.gameover:
            print('Turn:', self.step)
            if (self.step%2) == self.turn:
                print('It\'s your turn')    
                x,y = self.make_decision()
                print(f"Your move is {x},{y}.")
                # [x,y] = [int(x) for x in input("Enter the move : ").split()]
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
