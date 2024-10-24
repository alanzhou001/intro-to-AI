import math
import numpy as np


class Bid():
    def __init__(self, payoff):
        """记录需要的信息"""
        self.payoff=gain
        self.solution_A=[]
        self.solution_B=[]

    def actions(self,previous_action=None):
        """每次出价可以竞标的价格"""
        action=['L','M','H']

        if previous_action == 'M':
            action.remove('L')
        elif previous_action == 'H':
            action=['H']

        return action

    def A_value(self,round,A_action,B_action):
        """让A收益最大化策略时A，B的收益"""
        if round==5:
            return self.payoff[(A_action,B_action)]

        va = -np.inf
        vb = -np.inf
        A_action = self.actions(A_action)
        for a in A_action:
            temp=self.B_value(round+1,a,B_action)
            if temp[0]>va:
                va=temp[0]
                vb=temp[1]
        return va,vb # 最重要的区别，A和B的Value是两个数字，而非一个数字，所以需要分别记录两者的收益，以及两者都是最大化收益

    def B_value(self,round,A_action,B_action):
        """让B收益最大化策略时A，B的收益"""

        if round==5:
            return self.payoff[(A_action,B_action)]

        va = -np.inf
        vb = -np.inf
        B_action = self.actions(B_action)
        for b in B_action:
            temp=self.A_value(round+1,A_action,b)
            if temp[1] > vb:
                va = temp[0]
                vb = temp[1]
        return va, vb

    def minimax(self,round,isA,A_action,B_action):
        """返回每轮出价策略"""

        if round == 5:
            return

        if isA:
            A_action = self.actions(A_action)
            v = -np.inf
            for a in A_action:
                temp = self.B_value(round+1,a,B_action)[0]
                if temp > v:
                    v = temp
                    solution = a
            return solution

        else:

            B_action = self.actions(B_action)
            v = -np.inf
            for b in B_action:
                temp = self.A_value(round+1,A_action,b)[1]
                if temp > v:
                    v = temp
                    solution = b
            return solution
#竞价收益
gain={
    ('H','H'):[8,2],
    ('H','M'):[7,3],
    ('H','L'):[6,4],
    ('M','H'):[3,7],
    ('M','M'):[5,5],
    ('M','L'):[4,6],
    ('L','H'):[2,8],
    ('L','M'):[3,7],
    ('L','L'):[5,5]
}

#每次最优出价策略
b=Bid(gain)
b.minimax(1,True,None,None) #A:L
b.minimax(2,False,'L',None)#B:L
b.minimax(3,True,'L','L') #A:H
b.minimax(4,False,'H','L')#B:L

