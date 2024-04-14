from typing import Union
import typing
from Operation import Operation
from Term import Term
from math import log

class Expression:

    def __init__(self, left:Union[Term, 'Expression'], operand:Operation, right:Union[Term, 'Expression']):
        self.left:Term | 'Expression' = left
        self.right:Term | 'Expression' = right
        self.floor:bool = False
        self.operand:Operation = operand
        if not isinstance(left, Expression) and not isinstance(right, Expression):
            self.floor = True
    
    def __str__(self) -> str:
        return f"Exp({self.left}, {Expression.operandsMapping[self.operand]}, {self.right})"

    def derivate(self)->'Expression':
        return 
    
    def solve(self, variablesValues={})->float:
        #   When solve is called, it should check if left and right are
        #   constants, if so then, solve, else, try solve left and right
        #   that should work recursively if on the deepest level, left 
        #   and right arent evaluatable, then it should return an error
        left = self.left
        right = self.right
        if isinstance(self.left, Expression):
            left = self.left.solve(variablesValues)
        if isinstance(self.right, Expression):
            right = self.right.solve(variablesValues)
        if isinstance(left, Term):
            if not left.constant:
                if left.ref in variablesValues:
                    left = variablesValues[left.ref]
                else:
                    raise KeyError('There are variables on the expression, some value mapping should be provided for them in order to be able to solve')
            else:
                left = left.value
        if isinstance(right, Term):
            if not right.constant:
                if right.ref in variablesValues:
                    right = variablesValues[right.ref]
                else:
                    raise KeyError('There are variables on the expression, some value mapping should be provided for them in order to be able to solve')
            else:
                right = right.value
        return self.handleHandlers(self.operand)(left,right)


    operandsMapping:dict = {
        Operation.ADITION       : '+',
        Operation.SUBTRACTION   : '-',
        Operation.MULTIPLICATION: '*',
        Operation.DIVISION      : '/',
        Operation.EXPONENTIATION: '^',
        Operation.LOGARITMATION : '¬',
    }

    @staticmethod
    def handleHandlers(operator:Operation):
        handlersMap = {
            Operation.ADITION        : Expression.handleAdition,
            Operation.SUBTRACTION    : Expression.handleSubtraction,
            Operation.MULTIPLICATION : Expression.handleMultiplication,
            Operation.DIVISION       : Expression.handleDivision,
            Operation.EXPONENTIATION : Expression.handleExponentiation,
            Operation.LOGARITMATION  : Expression.handleLogarithm
        }
        return handlersMap[operator]

    @staticmethod
    def handleAdition(a, b):
        return a + b
    
    @staticmethod
    def handleSubtraction(a, b):
        return a - b

    @staticmethod
    def handleMultiplication(a, b):
        return a * b

    @staticmethod
    def handleDivision(a, b):
        return a / b

    @staticmethod
    def handleExponentiation(a, b):
        return a**b

    @staticmethod
    def handleLogarithm(a, b):
        return log(b, a)
    
if __name__ == '__main__':
    print(Expression.handleLogarithm(2,8))