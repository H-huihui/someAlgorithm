# -*- coding: utf-8 -*-

class Maze(object):
    
    def __init__(self,x,y,oriten,maps):
        '''
        the Maze class has three attri
        whit x and y being the coordinates and oriten with orientation
        '''
        self.x = x #this is the position of x
        self.y = y #this is the positon of y
        self.oriten = oriten # this is the orientation
        self.map = Map(maps) # init a map object
        self.steps = 0 # count the steps of way
        self.height = self.map.getHeight()
        
    '''
    the forward function,orientation rules is:
        0:positive in y-axis(north)
        1:negative in x-axis(west)
        2:negative in y-axis(south)
        3:positive in x-axis(east)
        and show the result of one step
        and count steps
    '''
    
    def forward(self):# go forward just one step
        if self.oriten == 0: # to judge the orientation
            self.y = self.y+1
        elif self.oriten == 1:
            self.x = self.x-1
        elif self.oriten == 2:
            self.y = self.y-1
        else:
            self.x = self.x+1
        self.show()
        self.steps+=1
        
    '''
    the turn Right function:
        just turns the provided pose right one time
        and show the result of turn right
        and count step
    '''
    def turnRight(self):
        #turns the provided pose right
        if self.oriten== 0:
            self.oriten=3
        elif self.oriten == 1:
            self.oriten = 0
        elif self.oriten == 2:
            self.oriten =1
        elif self.oriten == 3:
            self.oriten = 2
        else:
            return False #just a check
        self.show() #show the result
        self.steps+=1 #count steps
    '''
    the turn left function:
        the same as turnLeft function
    '''
    def turnLeft(self):
        #turns the provided pose right
        if self.oriten== 0:
            self.oriten=1
        elif self.oriten == 1:
            self.oriten = 2
        elif self.oriten == 2:
            self.oriten =3
        elif self.oriten == 3:
            self.oriten = 0
        else:
            return False 
        self.show()
        self.steps+=1
    
    '''
    isWallInFront function:
        judge the next step is a wall,the means:
        if next step equals 'X':
            return True
        else:
            return False
    '''
    def isWallInFront(self):
        #return true if the cell in front of given pose is occupied
        if self.oriten == 0:
            temp = self.map[self.y+1,self.x]
        elif self.oriten ==1:
            temp = self.map[self.y,self.x-1]
        elif self.oriten ==2:
            temp = self.map[self.y-1,self.x]
        elif self.oriten ==3:
            temp = self.map[self.y,self.x+1]
        else:
            exit()
        if temp == 'X':
            return True
        elif temp == '.':
            return False
    '''
    isWallRightSide function:
        like isWallInFront function means:
            if right side equals 'X':
                return True
            else:
                return False
    '''
    def isWallRightSide(self):
        #check there is a wall in the right side
        if self.oriten == 0:
            temp = self.map[self.y,self.x+1]
        elif self.oriten ==1:
            temp = self.map[self.y+1,self.x]
        elif self.oriten ==2:
            temp = self.map[self.y,self.x-1]
        elif self.oriten ==3:
            temp = self.map[self.y-1,self.x]
        else:
            exit()
        if temp == 'X':  # check the right side
            return True
        elif temp == '.':
            return False  # return False
        
    def show(self):
        #print the result of pose
        print("[["+str(self.x)+", "+str(self.y)+"]"+", "+str(self.oriten)+"]")
        
    '''
    findWall function is one of the most important functions
    in this function, we find the Wall position
    Go forward until you either:
        reach an exit
        have a wall to the right side
        have a wall in front of you
            in this case turn left once
        
    '''
    def findWall(self):
        flag = True
        # the flag is the sign of exit the loop
        
        while flag:
            if self.y>self.height-2 or self.y<1 or self.x>18 or self.x<1:
                break
            
            elif self.isWallRightSide():
                # there are wall right side
                flag = False
            elif self.isWallInFront():
                #there are wall front
                self.turnLeft()
                flag = False
            else:
                #step forward
                self.forward()
    '''
    floWall function:
    Do until you reach an exit:
        if no wall on your right:
            turn right
            step forward
        else if wall in front of you:
            turn left
        else:
            step forward
    '''
    def folloWall(self):
        while True:
             if self.y>self.height-2 or self.y<1 or self.x>18 or self.x<1:
                 self.forward()
                 #this is end
                 break
             elif not self.isWallRightSide():
                 #there no wall on your right
                 self.turnRight()
                 self.forward()
             elif self.isWallInFront():
                 #there wall front of you
                 self.turnLeft()
             else:
                 #go step forward
                 self.forward()
'''
this class is to save the map
'''
class Map(object):
    def __init__(self,content):
        #takes a position as input and return the map value(0 or 1)
        self.map = content
        
    def __getitem__(self,x):
        return self.map[x[0]][x[1]]
        print()
    def getHeight(self):
        return len(self.map[0])

if __name__ == "__main__":
    files = open('maze.test')
    contents = files.readlines()
    result = []
    
    for line in contents:
        if line[0]=='#':
            continue
        elif (line[0] == 'X' or line[0] == '.') and len(line) ==21:
            line = line.strip()
            result.insert(0,line)
        elif line[0]!='X' and line[0]!='.':
            startPoint = line.strip().split()
            try:
                x,y,o = eval(startPoint[0]),eval(startPoint[1]),eval(startPoint[2])
            except Exception:
                exit(0)
            if o==1 or o==2 or o==3 or o==0:
                pass
            else:
                exit(0)
        else:
            exit(0)
            
    M = Map(result)
    maze = Maze(x,y,o,result)
    maze.show()
    maze.findWall()
    maze.folloWall()
