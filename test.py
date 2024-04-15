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


# string = "(~127^x+2¬~8)^15*x"
# print("Before parse:",string, sep='\n')
# print("After parse:",Evaluator.evaluate(string),sep='\n')
# string = "(~127^2+2¬8)^15*2"
string = "(2*2+2)+x"
print("Before parse:",string, sep='\n')
exp = Evaluator.evaluate(string)
print("After parse:",exp,sep='\n')
print("Solve:",exp.solve({"x":13}), sep='\n')
# print("---------------------------")
# print("Derivative:",exp.derivate())