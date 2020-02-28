from funcparserlib.parser import (some, a, many, skip, finished, maybe, with_forward_decls)
import operator
import sys
from functools import reduce
digits = '0123456789.'
operators = '+-*()'



"""
Parses a list of tokens EXPLST, returning a tuple where the first element is
it's evaluation.
Acknowledgement: This is largely based upon Andrey Vlasovskikh's implementation
    of an expression calculator, as seen in the funcparserlib tutorial.
"""
def parse(tokens):
    const = lambda x: lambda _: x
    unarg = lambda f: lambda x: f(*x)
    makeop = lambda s, f: op(s) >> const(f)
    #converting string representing number to respective numeric type
    def makenum(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    #evaluator parser 
    eval = unarg(lambda z, lst: reduce((lambda s, a: a[0](s, a[1])), lst, z))

    #define parsers for primitive types (nums and arithmetic ops)
    number = some(lambda tok: tok[0] in digits) >> makenum
    op = lambda s: some(lambda tok: (tok in operators) and (tok == s))
    skipop = lambda s: skip(op(s))

    #setup basic operations
    add = makeop('+', operator.add)
    sub = makeop('-', operator.sub)
    mul = makeop('*', operator.mul)
    add_op = add | sub
    @with_forward_decls
    def parens():
        return number | (skipop('(') + expr + skipop(')'))

    #composing series of parsers
    term = parens + many(mul + parens) >> eval
    expr = term + many(add_op + term) >> eval
    toplevel = maybe(expr) + skip(finished)

    return toplevel.parse(tokens)

"""
Receives a parenthesized arithmetic expression LINE and returns it's evaluation.
"""
def drive(line):
    holder = []
    cleaned = line.replace(' ', '')
    for c in cleaned:
        if c in operators:
            holder.append(c)
        elif c in digits:
            if len(holder) == 0 or not (holder[-1][0] in digits):
                holder.append(c)
            else:
                holder[-1] = holder[-1] + c
        else:
            return "Invalid Input: " + line
    return parse(holder)

def main():
     for i in range(1, len(sys.argv)):
         print(driver(sys.argv[i]))

     form = "Input: {} ... Expected: {} ... Actual: {}"
     print("\nExample Tests: ")
     print(form.format("(52*2)", 104, drive("(52*2)")))
     print(form.format("4-2", 2, drive("4-2")))
     print(form.format("((4-2)+(3*2))", 8, drive("((4-2)+(3*2))")))
     print(form.format("((1+(3*2))-4)", 3, drive("((1+(3*2))-4)")))
     print(form.format("(5.6+2.4)", 8, drive("(5.6+2.4)")))
     print(form.format("(6)", 6, drive("(6)")))

     print(drive('bill'))
     print(drive('(bill-bill)'))

if __name__== "__main__":
    main()
