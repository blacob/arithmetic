import sys
digits = '0123456789.'
operators = '+-*'
parens = '()'

"""
Parses a list of tokens EXPLST, returning a tuple where the first element is
it's evaluation.
"""
def parse(explst):
    first = explst[0]
    rest = explst[1:]
    if first == '(':
        left, newlist = parse(rest)
        operator = newlist[0]
        right, toss = parse(newlist[1:])
        return eval(left, operator, right), toss[1:]
    return first, rest

"""
Takes numerical types L and R and applies function that OPERATOR represents
"""
def eval(l, operator, r):
    left = float(l)
    right = float(r)
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    else:
        print("ERROR, invalid op: " + operator)
        exit()

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
        return parse(holder)[0]
    except IndexError:
        return "Invalid Input: " + line


def main():
     for i in range(1, len(sys.argv)):
         print(driver(sys.argv[i]))
     print("\nExample Tests: ")
     print("Input: '(521+3)' ... Expected: 524 ... Got: " + str(driver("(521+3)")))
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
