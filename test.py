from Evaluator import Evaluator
from Expression import Expression
from Term import Term
from Operation import Operation

# 1 + 1 + 1
# exp = Expression(
#     Expression(Term("1.2"), Operation.ADITION, Term("1")),
#     Operation.ADITION,
#     Term("1")
# )
# print(Evaluator.devaluate(exp))


string = "(~127^x+2¬~8)^2*x"
print("Before parse:",string, sep='\n')
print("After parse:",Evaluator.evaluate(string),sep='\n')
# string = "(~127^2+2¬8)^(15*2)"
# string = "(2*2+2)+x"
print("Before parse:",string, sep='\n')
exp = Evaluator.evaluate(string)
print("After parse:",exp,sep='\n')
print("Solve:",exp.solve({"x":1/2}), sep='\n')
print("---------------------------")
# print("Derivative:",exp.derivate())
# # string = '(((x^2)^x)^(y-x))';
# print(Evaluator.evaluate(string))
# print(string)
# Evaluator.evaluate(string)

# def testBracket():
#     array = [x for x in '(~127^2+2¬8)^(15*2)']
#     print(array)
#     levelOpen:int  = 0
#     levelClose:int = 0
#     print("-"*50)

#     bracketStarts = []
#     count:int = 0
#     while count < len(array):
#         if array[count] == '(':
#             bracketStarts.append(count)
#         if array[count] == ')':
#             start = bracketStarts.pop()
#             chunk = array[start+1:count]
#             array = array[0:start]+['@']+array[count+1:]
#             count = start
#             print(chunk)
#         count += 1
#     print("-"*50)

# testBracket()
