Math interpreter, translates user input to a more computer-friendly format (called Expressions). 
Expressions have methods such as, solve and derivate.
  -Solve: Resolves a expression into a constant value, if expressions have variables,
          it accepts a Dictionary conatining a value mapping for those variables. EX:
            expression = Exp(Exp(Exp(2, *, 2), +, 2), +, x)
            expression.solve({"x":13}) -> 19.0
  -Derivate: Returns the derivative of the Expression, the output format will also be
      an expression or a Term

      
