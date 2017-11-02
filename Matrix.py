# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""  
class MatrixSyntaxError(Exception):
    pass
    
class Matrix():  
    
    def __init__(self,s):
        
        self.result = self.clean(s)
        self.row = len(self.result)
        self.column = len(self.result[0])
        self.shape = (self.row,self.column)
        self._matrix = [[0]*self.column for i in range(self.row)]
                        
    def clean(self,s):
        s = s.replace(' ','')
        s = s.replace(';',',')
        try:
            temp1 = eval(s)
        except:
            raise MatrixSyntaxError
        return temp1
        
    def __str__(self):
        return self.show(self.result)
        
    def __add__(self,N):
        assert N.shape == self.shape
        M = Matrix(repr(N.result).replace('],','];'))
        for r in range(self.row):
            for c in range(self.column):
                M[r, c] = self[r, c] + N[r, c]
        return M
        
    def show(self,result):
        temp = result
        for r in range(self.row):
            for j in range(self.column):
                if (int(temp[r][j])==temp[r][j]):
                    temp[r][j] = int(temp[r][j])
                else:
                    continue
        resultx  = repr(result).replace('],','];')
        return resultx
        
    def __getitem__(self,index,*arg):
        if not arg:
            if isinstance(index, int):
                return self.result[index]
            elif isinstance(index, tuple):
                if isinstance(index[0],slice) and isinstance(index[1],slice):
                    resultlist = []
                    for i in range(self.row):
                        templist = []
                        for j in range(self.column):
                            ii = index[0].start + i * index[0].step
                            stop1 = index[0].stop
                            jj = index[1].start + j * index[1].step
                            stop2 = index[0].stop
                            if ii < stop1 and jj < stop2:
                                templist.append(self.result[ii][jj])
                            else:
                                continue
                        if templist:
                            resultlist.append(templist)
                    M = Matrix(repr(resultlist).replace('],','];'))
                    return M
                else:
                    return self.result[index[0]][index[1]]
            else:
                raise MatrixSyntaxError
        else:
            raise MatrixSyntaxError
            
    def __setitem__(self,index,value):
        if isinstance(value,Matrix):
            if value.row == 1 and value.column == self.column:
                self.result[index] = value.result[0]
            elif isinstance(index,tuple) and isinstance(index[0],slice) and isinstance(index[1],slice):
                for i in range(self.row):
                    for j in range(self.column):
                        ii = index[0].start + i * index[0].step
                        jj = index[1].start + j * index[1].step
                        stop1 = index[0].stop
                        stop2 = index[1].stop
                        if ii<stop1 and jj<stop2:
                            self.result[ii][jj] = value[i,j] 
                        else:
                            continue
            else:
                raise MatrixSyntaxError     
        elif isinstance(index,int):
            self.result[index] = value
        elif isinstance(index,tuple):
            self.result[index[0]][index[1]]=value
        else:
            raise MatrixSyntaxError
            
    def __eq__(self,N):
        assert isinstance(N,Matrix)
        if N.shape == self.shape:
            for r in range(self.row):
                for c in range(self.column):
                    if self[r,c] == N[r,c]:
                        continue
                    else:
                        return False
            return True
        else:
            return False
            
    def __sub__(self,N):
        assert N.shape == self.shape
        M = Matrix(repr(N.result).replace('],','];'))
        for r in range(self.row):
            for c in range(self.column):
                M[r,c] = self[r,c]-N[r,c]
        return M
        
    def __mul__(self,N):
        if isinstance(N,int) or isinstance(N,float):
            M = Matrix(repr(self.result).replace('],','];'))
            for r in range(self.row):
                for c in range(self.column):
                    M[r,c] = self[r,c]*N
            return M
            
        elif isinstance(N,Matrix):
            if self.row == N.column:
                M = Matrix(repr(self.result).replace('],','];'))
                for r in range(self.row):
                    for c in range(N.column):
                        M[r,c] = 0
                        for k in range(self.row):
                            M[r,c] += self[r,k] * N[k,c]
                return M
            else:
                raise MatrixSyntaxError
        else:
            raise MatrixSyntaxError
            
    def __truediv__(self,N):
        if isinstance(N,int) or isinstance(N,float):
            M = Matrix(repr(self.result).replace('],','];'))
            for r in range(self.row):
                for c in range(self.column):
                    M[r,c] = self[r,c]/float(N)
        return M
    
    def __pow__(self,k):
        assert self.row == self.column
        M = Matrix(repr(self.result).replace('],','];'))
        
        for i in range(k-1):
            M = M * self
        return M
    def identity(self):
        if self.row == self.column:
            M = Matrix(repr(self.result).replace('],','];'))
            for r in range(self.row):
                for c in range(self.column):
                    M[r,c] = 1.0 if r == c else 0.0
            return M
        else:
            raise MatrixSyntaxError
    def isIdentity(self):
        if self.row == self.column:
            for r in range(self.row):
                for c in range(self.column):
                    if r == c and int(self[r,c]) == 1:
                        continue
                    elif r!=c and int(self[r,c]) == 0:
                        continue
                    else:
                        return False
            return True
        else:
            return False
        
    def isSquare(self):
        return self.row == self.column
        
    def determinant(self):
        assert self.row == self.column
        if self.shape == (2,2):
            return self[0,0]*self[1,1] - self[0,1]*self[1,0]
        else:
            sum = 0.0
            for c in range(self.column + 1):
                sum = sum + (-1)**(c+1)*self[1,c]*self.cofactor(1,c).determinant()
            return sum
    def transposition(self):
        M = Matrix(repr(self.result).replace('],','];'))
        for r in range(self.column):
            for c in range(self.row):
                M[r,c] = self[c,r]
        return M
        
    def cofactor(self,row,column):
        assert self.row == self.column
        assert self.row >= 3
        assert row <= self.row and column <= self.column
        M = Matrix(repr(self.result).replace('],','];'))
        for r in range(self.row):
            if r == row:
                continue
            for c in range(self.column):
                if c == column:
                    continue
                rr = r-1 if r>row else r
                cc = c-1 if c>column else c
                
                M[rr,cc] = self[r,c]
        return M
    def inverse(self):
        assert self.row == self.column
        M = Matrix(repr(self.result).replace('],','];'))
        M.column = M.column*2
        isIden = self.identity()
        
        for r in range(1,M.row):
            temp = self[r]
            temp.extend(isIden[r])
            M[r] = temp
        
        for r in range(1,M.row):
            if M[r,r] == 0:
                for rr in range(r,M.row):
                    if M[rr,r]!=0:
                        M[r],M[rr] = M[rr],M[r]
                    break

            temp = M[r,r]
            for c in range(r,M.column):
                M[r,c] /=temp
                print("M[{0},{1}] /={2}".format(r,c,temp))
            
            for rr in range(1,M.row):
                temp = M[rr,r]
                for c in range(r, M.column):
                    if rr == r:
                        continue
                    M[rr,c] -=temp*M[r,c]
                    print("M[{0},{1}] -={2}*M[{3},{1}]".format(rr,c,temp,r))
                
        N = Matrix(self.row,self.column)
        for r in range(1,self.row):
            N[r] = M[r][self.row:]
        return N
