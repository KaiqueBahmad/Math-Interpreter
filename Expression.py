from Operation import Operation
from typing import Tuple, List
from typing import Union
from Properties import Properties
from Term import Term
from math import log
import typing

class Expression:
    def __init__(self, left:Union[Term, 'Expression'], operand:Operation, right:Union[Term, 'Expression']):
        self.left:Term | 'Expression' = left
        self.right:Term | 'Expression' = right
        self.floor:bool = False
        self.operand:Operation = operand
        self.hasVariable = self.checkIfIHaveVariables()
        #It's not used anywhere yet, maybe I'm going to remove it anytime
        if not isinstance(left, Expression) and not isinstance(right, Expression):
            self.floor = True
    
    def checkIfIHaveVariables(self):
        leftIsVariable  = False
        rightIsVariable = False

        if isinstance(self.left, Term):
            leftIsVariable  = not self.left.constant
        elif isinstance(self.left, Expression):
            leftIsVariable = self.left.checkIfIHaveVariables()

        if isinstance(self.right, Term):
            rightIsVariable = not self.right.constant
        elif isinstance(self.left, Expression):
            rightIsVariable = self.right.checkIfIHaveVariables()
        return leftIsVariable or rightIsVariable

    def __str__(self) -> str:
        return f"Exp({self.left}, {Expression.operandsMapping[self.operand]}, {self.right})"

    def derivate(self)->'Expression':
        # if isinstance(self.left, Term) and isinstance(self.right, Term):
        #     if self.left.constant and self.right.constant:
        #         print("sim")
        #         return Term("0")
        if ((isinstance(self.left, Term) and self.left.constant) or not self.left.hasVariable) and ((isinstance(self.right, Term) and self.right.constant)or not self.right.hasVariable):
            pass
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

    @staticmethod
    def simplify(exp:'Expression'):
        if (isinstance(exp.left, Term) and exp.left.constant and exp.left.value == 0): 
            if exp.operand in Properties["zeroInterIrrelevantOperands"]:
                return exp.right
        if (isinstance(exp.right, Term) and exp.right.constant and exp.right.value == 0):
            if exp.operand in Properties["zeroInterIrrelevantOperands"]:
                    return exp.left
        if isinstance(exp.left, Expression):
            exp.left = Expression.simplify(exp.left)
        if isinstance(exp.right, Expression):
            exp.right = Expression.simplify(exp.right)
        return exp

    operandsMapping:dict = {
        Operation.ADITION       : '+',
        Operation.SUBTRACTION   : '-',
        Operation.MULTIPLICATION: '*',
        Operation.DIVISION      : '/',
        Operation.EXPONENTIATION: '^',
        Operation.LOGARITMATION : '¬',
    }

    
    def handleHandlers(self):
        print(self.operand)
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
        while isinstance(a, Expression) or isinstance(b, Expression):
            if isinstance(a, Expression):
                # print(a)
                print("Derivando: ",a)
                a = a.derivate()
                print("Derivado:",a)
            if isinstance(b, Expression):
                # print(b)
                print("Derivando: ",b)
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
    def derivateExponentiation(a:Union[Term, 'Expression'], b:Union[Term, 'Expression']):
        if (isinstance(a, Term) and isinstance(b, Term)):
            if not a.constant and b.constant:
                return Evaluator.evaluate(f'{b.value}*{a.ref}^{b.value-1}')
        else:
            raise NotImplementedError("Derivada ainda não implementada")

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
    def handleMultiplication(a:Union['Expression', Term], b:Union['Expression', Term]):
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
    

class Evaluator:
    #   Here we will have a long journey to make a string input
    #       to be parsed into a expression :)
    zeroInterIrrelevantOperands:list = [
        Operation.ADITION,
        Operation.SUBTRACTION,
    ]
    oneInterIrrelevantOperands:list = [
        Operation.MULTIPLICATION,
        Operation.DIVISION,
    ]
    oneRightIrrelevantOperands:list = [
        Operation.EXPONENTIATION
    ]

    # 2^2 + 7x
    # 
    # Expressao( Expressao(2, 'exp', 2), 'mais', Expressao(7, 'vezes', 'x') )


    operandsMapping:dict = {
        Operation.ADITION       : '+',
        Operation.SUBTRACTION   : '-',
        Operation.MULTIPLICATION: '*',
        Operation.DIVISION      : '/',
        Operation.EXPONENTIATION: '^',
        Operation.LOGARITMATION : '¬',
    }

    @staticmethod
    def evaluate(input_:str) -> Expression:
        input_ = Evaluator.removeUselessChars(input_)
        tokenList = Evaluator.splitIntoTokenList(input_)
        Evaluator.syntaxCheck(tokenList.copy())
        return Evaluator.parse(tokenList)
    
    @staticmethod
    def removeUselessChars(string:str)->str:
        return string.replace("\n","").replace(" ","")

    @staticmethod
    def parse(array:List[str]) -> Expression:
        #Parser will parse based on PENDAS
        #Parentesis solves will work recursivelly
        #Sample input    vvv
        #               ["~12", "*", "x", "+", "(", "2", "/", "x", ")"]
        print('CHUNK: ',array)
        specialChars:list = list(Evaluator.operandsMapping.values())
        brackets:list = ['(',')']
        count:int = 0
        levelOpen:int  = 0
        levelClose:int = 0

        bracketStarts = []

        while count < len(array):
            if array[count] == brackets[0]:
                bracketStarts.append(count)
            if array[count] == brackets[1]:
                start = bracketStarts.pop()
                chunk = array[start+1:count]
                array = array[:start]+[Evaluator.parse(chunk)]+array[count+1:]
                count = 0
                bracketStarts = []
                # if len(bracketStarts):
                #     count = bracketStarts[-1]
            count += 1
        # return
        #The code above parses all the parentesis recursively, from inside to outside
        #------------------------------------------------------------------------------
        #This code will parse every exponentiation or logarithmation
        count = 0
        while count < len(array) - 2:
            if array[count+1] in [Evaluator.operandsMapping[Operation.EXPONENTIATION]]+[Evaluator.operandsMapping[Operation.LOGARITMATION]]:
                array = array[:count]+[Evaluator.createExpression(array[count], array[count+1], array[count+2])]+array[count+3:]
            count+=2
        #This code will parse every multiplication or division
        count = 0
        while count < len(array) - 2:
            if array[count+1] in [Evaluator.operandsMapping[Operation.MULTIPLICATION]]+[Evaluator.operandsMapping[Operation.DIVISION]]:
                array = array[:count]+[Evaluator.createExpression(array[count], array[count+1], array[count+2])]+array[count+3:]
            count+=2
        #This code will parse every adition or subtraction
        count = 0
        while count < len(array) - 2:
            if array[count+1] in [Evaluator.operandsMapping[Operation.ADITION]]+[Evaluator.operandsMapping[Operation.SUBTRACTION]]:
                array = array[:count]+[Evaluator.createExpression(array[count], array[count+1], array[count+2])]+array[count+3:]
            count+=2
        return array[0]

    @staticmethod
    def createExpression(term1:str|Expression, operator:str, term2:str|Expression) -> Expression:
        for i in Evaluator.operandsMapping:
            if Evaluator.operandsMapping[i] == operator:
                if isinstance(term1, str):
                    term1 = Term(term1)
                if isinstance(term2, str):
                    term2 = Term(term2)
                return Expression(term1, i, term2)
        raise NotImplementedError("Not in Evaluator.operandsMapping. Operator"+operator)



    @staticmethod
    def syntaxCheck(array:List[str]):
        specialChars:list = list(Evaluator.operandsMapping.values())
        brackets:list = ['(',')']
        #Grants every token is exclusively only made of letters, numbers or it's a operation / bracket
        for i in array:
            if i.startswith('~'):
                if i[1:] in specialChars+[')'] or i[1:].count('~'):
                    raise SyntaxError('Token not recognized: '+i)
                else:
                    continue
            if i not in specialChars+brackets and not (i.isalpha() or i.replace('.','').isnumeric()):
                if i.count('.') > 1:
                    raise SyntaxError('Token not recognized: '+i)
        #Assets that every opened bracket has a closing other
        if array.count('(') != array.count(')'):
            raise SyntaxError('There are not closed brackets on the expression')
        #Check if every expression inside a bracket is also valid
        if array.count('('):
            Evaluator.checkBracketsExpressions(array.copy())
        #Removes everything inside of the brackets and substitutes by a variable
        levelOpen:int  = 0
        levelClose:int = 0
        count:int = 0
        cappedArray:List[str] = []
        while count < len(array):
            if array[count] not in brackets and not levelOpen:
                cappedArray.append(array[count])
            if array[count] == brackets[0]:
                levelOpen  += 1
            if array[count] == brackets[1]:
                levelClose += 1
            if levelOpen == levelClose and levelOpen:
                levelOpen = 0
                levelClose = 0
                cappedArray.append('@')
            
            count += 1
        #Checks if for every token there is a operation
        if cappedArray[0] in specialChars:
            raise SyntaxError('There is some alone operator at the start of the expression')
        if cappedArray[-1] in specialChars:
            raise SyntaxError('There is some alone operator at the end of expression')
        count = 0
        while count < len(cappedArray) - 1:
            if cappedArray[count] in specialChars:
                raise SyntaxError('There is some operator placed wrong')
            if cappedArray[count+1] not in specialChars:
                raise SyntaxError('There is some operator placed wrong')
            count += 2
        if len(cappedArray) % 2 == 0:
            raise SyntaxError('How did you managed to have an even number of tokens at the expressions?')
        #   At this point it should already be classified a nice input
        #   with a valid syntax :)

    @staticmethod
    def checkBracketsExpressions(array:List[str]):
        specialChars:list = list(Evaluator.operandsMapping.values())
        brackets:list = ['(',')']
        if not array.count(brackets[0]):
            Evaluator.syntaxCheck(array)
        #level stands for Bracket current depth
        levelOpen:int  = 0
        levelClose:int = 0
        count:int = 0
        while count < len(array):
            if array[count] == brackets[0]:
                if levelOpen == 0:
                    start = count
                levelOpen += 1
            if array[count] == brackets[1]:
                levelClose += 1
            if levelOpen == levelClose and levelOpen > 0:
                levelOpen  = 0
                levelClose = 0
                chunk = array[start+1:count]
                Evaluator.checkBracketsExpressions(chunk)            
            count += 1

    @staticmethod
    def splitIntoTokenList(input:str) -> list:
        array:List[str] = []
        buffer:str = ""
        specialChars:list = list(Evaluator.operandsMapping.values())
        brackets:list = ['(',')']

        for letter in input:
            if (letter not in specialChars+brackets):
                buffer += letter
            else:
                if buffer != '':
                    array.append(buffer)
                array.append(letter)
                buffer = ''
        if buffer != '':
            array.append(buffer)
        return array
    
    @staticmethod
    def evaluateZeroInterIrrelevant(input:Expression) -> Tuple[bool, Term] :
        if input.left.constant and input.left.value == 0:
            return [True, input.right]
        if input.right.constant and input.right.value == 0:
            return [True, input.left]
        return [False, None]

    @staticmethod
    def devaluate(input:Expression, options=dict()) -> str:
        return Evaluator.devaluateRecursion(input, '')

    @staticmethod
    def devaluateRecursion(input:typing.Union[Expression, Term], output:str) -> str:
        if isinstance(input.left, Term):
            if isinstance(input.right, Term):
                return f"{input.left.toString()}{Evaluator.operandsMapping[input.operand]}{input.right.toString()}"
            return f"{input.left.toString()}{Evaluator.operandsMapping[input.operand]}{Evaluator.devaluateRecursion(input.right, '')}"
        if isinstance(input.left, Expression):
            if isinstance(input.right, Term):
                return f"{Evaluator.devaluateRecursion(input.left, '')}{Evaluator.operandsMapping[input.operand]}{input.right.toString()}"
            return f"{Evaluator.devaluateRecursion(input.left, '')}{Evaluator.operandsMapping[input.operand]}{Evaluator.devaluateRecursion(input.right, '')}"


if __name__ == '__main__':
    print(Expression.handleLogarithm(2,8))