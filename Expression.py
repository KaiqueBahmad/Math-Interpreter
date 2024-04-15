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
        print(self)
        if isinstance(self.left, Term) and isinstance(self.right, Term):
            if self.left.constant and self.right.constant:
                print("sim")
                return Term("0")
        return self.handleHandlers()["derivate"](self.left,self.right)
    
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
        return self.handleHandlers()["solve"](left,right)

    def simplify(self):
        return self

    operandsMapping:dict = {
        Operation.ADITION       : '+',
        Operation.SUBTRACTION   : '-',
        Operation.MULTIPLICATION: '*',
        Operation.DIVISION      : '/',
        Operation.EXPONENTIATION: '^',
        Operation.LOGARITMATION : '¬',
    }

    
    def handleHandlers(self):
        if self.operand == Operation.INVALID:
            raise TypeError("Operator type is: "+str(self.operand))
        handlersMap = {
            Operation.ADITION        : {
                "solve"   : Expression.handleAdition,
                "derivate": Expression.derivateAdition
            },
            #The difference between subtraction and adition actually dont exist
            #so I should later remove the Operation.SUBTRACTION and threat it just like
            #a commo ADITION
            Operation.SUBTRACTION    : {
                "solve"   : Expression.handleSubtraction,
                "derivate": Expression.derivateSubtraction
            },
            Operation.MULTIPLICATION : {
                "solve"   : Expression.handleMultiplication,
                "derivate": Expression.derivateMultiplication
            },
            #Same as the comment above, maybe i can threat multiplication and division
            #the same way
            Operation.DIVISION       : {
                "solve"   : Expression.handleDivision,
                "derivate": Expression.derivateDivision
            },
            Operation.EXPONENTIATION : {
                "solve"   : Expression.handleExponentiation,
                "derivate": Expression.derivateExponentiation
            },
            Operation.LOGARITMATION  : {
                "solve":Expression.handleLogarithm,
                "derivate":Expression.derivateLogaritmation
            }
        }
        return handlersMap[self.operand]

    @staticmethod
    def derivateAdition(a:Union[Term, 'Expression'], b:Union[Term, 'Expression']):
        if isinstance(a, Expression):
            # print(a)
            a = a.derivate()
        if isinstance(b, Expression):
            # print(b)
            b = b.derivate()
        if a.constant:
            return Expression.fallRule(
                Expression(
                    b,
                    Operation.EXPONENTIATION,
                    Term("1")
                )
            )
        if b.constant:
            return Expression.fallRule(
                Expression(
                    a,
                    Operation.EXPONENTIATION,
                    Term("1")
                )
            )      

    @staticmethod
    def fallRule(exp:'Expression')->'Expression':
        return Expression(
            Term(exp.right.value),
            Operation.MULTIPLICATION,
            Expression(
                exp.left,
                Operation.EXPONENTIATION,
                Term(exp.right.value - 1)
            )
        ).simplify()

    @staticmethod
    def derivateSubtraction(a, b):
        pass
    @staticmethod
    def derivateMultiplication(a, b):
        pass
    @staticmethod
    def derivateDivision(a, b):
        pass
    @staticmethod
    def derivateExponentiation(a, b):
        pass
    @staticmethod
    def derivateLogaritmation(a, b):
        pass

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