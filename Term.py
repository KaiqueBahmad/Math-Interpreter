import math

class Term:
    specialConstants = {'e':math.e, 'p':math.pi}

    #   self.constant stands for answering if Term is a constant or a variable
    #   self.value stores a numeric value, appliable only for constant
    #   self.ref stores the string reference to the Term, used after for evaluating
    #       him to a constant value, when it be provided
    def __init__(self, value:str):
        self.constant:bool
        self.special:bool = False
        self.floor:bool = True
        self.negative = False
        if value.startswith('~'):
            self.negative = True
            value = value[1:]
        if value in Term.specialConstants:
            self.constant  = True
            self.special   = True
            self.value     = float(Term.specialConstants[value])
            self.spRef:str = value
            return
        self.constant = Term.isfloat(value)
        if (self.constant):
            
            self.value = float(value)         
        else:
            if (len(value) > 1):
                raise ForbiddenRefException("Reference for a variable should be exactally 1 letter long.")
            if (value == ''):
                raise BlankRefException('Reference for a variable can\'t be a blank string.')
            self.ref = value
    
    @staticmethod
    def isfloat(input:str)->bool:
        if (input[0] == '.' or input[-1] == '.'):
            return False
        return input.replace('.', '').isnumeric()

    def toString(self) -> str:
        if self.constant:
            if self.value - int(self.value) == 0:
                return str(int(self.value))
            return str(self.value)
        if self.special:
            return self.spRef
        if not self.constant:
            return self.ref
    
    def __str__(self) -> str:
        if self.negative:
            return '~'+self.toString()
        return self.toString()

class BlankRefException(Exception):
    pass

class ForbiddenRefException(Exception):
    pass


if (__name__ == "__main__"):
    pass
