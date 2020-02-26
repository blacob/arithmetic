import sys
digits = '0123456789.'
operators = '+-*'
parens = '()'

def parse(explst):

    first = explst[0]
    rest = explst[1:]
    if first == '(':
        left, newlist = parse(explst[1:])
        #print(left, newlist)
        operator = newlist[0]
        right, toss = parse(newlist[1:])
        #print(right, toss)
        return eval(left, operator, right), toss[1:]
    elif first[0] in digits or first in operators:
        return first, explst[1:]



def eval(l, operator, r):
    left = int(l)
    if not r:
        return left
    right = int(r)
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    else:
        print("ERROR, invalid op: " + operator)
        exit()

""" Receives a parenthesized arithmetic expression and returns it's value. """
def driver(line):
    holder = []
    cleaned = line.replace(' ', '')
    for c in cleaned:
        if c in parens or c in operators:
            holder.append(c)
        elif c in digits:
            if len(holder) == 0 or not (holder[-1] in digits):
                holder.append(c)
            else:
                holder[-1] = holder[-1] + c
        else:
            return "Invalid Input: " + line
    return parse(holder)[0]

def main():
     for i in range(1, len(sys.argv)):
         print(driver(sys.argv[i]))
     print("\n Example Tests: ")
     print("Input: '(1+3)' ... Expected: 4 ... Got: " + str(driver("(1+3)")))
     print("Input: '(4-2)' ...  Expected: 2 ... Got: " + str(driver("(4-2)")))
     print("Input: '4-3' ...  Expected: 1 ... Got: " + str(driver("4-3")))
     print("Input: '((4-2)+(3*2))' ...  Expected: 8 ... Got: " + str(driver("((4-2)+(3*2))")))
     print("Input: '((1+(3*2))-4)' ... Expected: 3 ... Got: " + str(driver("((1+(3*2))-4)")))
     print("Input: '3' ... Expected: 3 ... Got: " + str(driver("3")))
     print(driver('bill'))
     print(driver('(bill-bill)'))

if __name__== "__main__":
    main()
