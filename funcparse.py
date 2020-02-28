from funcparserlib.parser import (some, a, many, skip, finished, maybe, with_forward_decls)
import operator
import sys
from functools import reduce
digits = '0123456789.'
operators = '+-*'
parens = '()'

"""
Parses a list of tokens EXPLST, returning a tuple where the first element is
it's evaluation.
"""
def parse(tokens):
    print(tokens)
    const = lambda x: lambda _: x
    unarg = lambda f: lambda x: f(*x)

    makeop = lambda s, f: op(s) >> const(f)

    def make_number(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def eval_expr(z, lst):
        return reduce((lambda s, a: a[0](s, a[1])), lst, z)
    eval = unarg(eval_expr)

    number = some(lambda tok: tok[0] in digits)
    op = lambda s: some(lambda tok: (tok in operators) and (tok == s))
    op_ = lambda s: skip(op(s))

    add = makeop('+', operator.add)
    sub = makeop('-', operator.sub)
    mul = makeop('*', operator.mul)

    add_op = add | sub

    @with_forward_decls
    def primary():
        return number | (op_('(') + expr + op_(')'))

    term = primary + many(mul + primary) >> eval
    expr = term + many(add_op + term) >> eval


    toplevel = maybe(expr) #+ finished
    return toplevel.parse(tokens)

"""
Receives a parenthesized arithmetic expression LINE and returns it's evaluation.
"""
def driver(line):
    holder = []
    cleaned = line.replace(' ', '')
    for c in cleaned:
        if c in parens or c in operators:
            holder.append(c)
        elif c in digits:
            if len(holder) == 0 or not (holder[-1][0] in digits):
                holder.append(c)
            else:
                holder[-1] = holder[-1] + c
        else:
            return "Invalid Input: " + line

    try:
        return parse(holder)
    except IndexError:
        return "Invalid Input: " + line


def main():
     for i in range(1, len(sys.argv)):
         print(driver(sys.argv[i]))
     print("\nExample Tests: ")
     print("Input: '(2+3)' ... Expected: 5 ... Got: " + str(driver("(2+3)")))
     print("Input: '(4-2)' ...  Expected: 2 ... Got: " + str(driver("(4-2)")))
     print("Input: '((4-2)+(3*2))' ...  Expected: 8 ... Got: " + str(driver("((4-2)+(3*2))")))
     print("Input: '((1+(3*2))-4)' ... Expected: 3 ... Got: " + str(driver("((1+(3*2))-4)")))
     print("Input: '3' ... Expected: 3 ... Got: " + str(driver("3")))
     print("Input: '(5.6+2.4)' ... Expected: 8 ... Got: " + str(driver("(5.6+2.4)")))
     print(str(driver("(6)")))
     print(driver('bill'))
     print(driver('(bill-bill)'))

if __name__== "__main__":
    main()
