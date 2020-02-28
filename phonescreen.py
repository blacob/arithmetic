import sys

operators = '+-*'
parens = '()'
digits = '0123456789.'

class Node:
    def __init__(self, data = 0, left = None, right = None, parent = None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

    def setdata(self, data):
        self.data = data

    def __str__(self):
        if self.left is None:
            return str(self.data)
        return (str(self.data) + " \n" + self.left.__str__() + "   " + self.right.__str__())


""" Takes in a list of tokens representing an expression and
    returns it's binary expression tree representation."""
def setup(expression):
    if not expression:
        return None
    root = Node()
    current = root
    for i in range(len(expression)):
        val = expression[i]
        if val == '(':
            current.left = Node(parent = current)
            current = current.left
        elif val in operators:
            current.setdata(val)
            current.right = Node(parent = current)
            current = current.right
        elif val[0] in digits:
            current.setdata(val)
            if current.parent:
                current = current.parent
        elif val == ')':
            if current.parent:
                current = current.parent
    return root

""" Takes in a binary expression tree, as returned by setup. """
def eval(exptree):
    if not exptree.left:
        return int(exptree.data)
    op = exptree.data
    l = eval(exptree.left)
    r = eval(exptree.right)
    if op == '+':
        return l + r
    elif op == '-':
        return l - r
    elif op == '*':
        return l * r
    else:
        print("Your internal procedure structure is corrupted")
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
    return eval(setup(holder))

def main():
     for i in range(1, len(sys.argv)):
         print(driver(sys.argv[i]))
     print("\n Example Tests: ")
     print("Input: '3' ... Expected: 3 ... Got: " + str(driver("3")))
     print("Input: '(1+3)' ... Expected: 4 ... Got: " + str(driver("(1+3)")))
     print("Input: '(4-2)' ...  Expected: 2 ... Got: " + str(driver("(4-2)")))
      print("Input: '((4-2)+(3*2))' ...  Expected: 8 ... Got: " + str(driver("((4-2)+(3*2))")))
     print("Input: '((1+(3*2))-4)' ... Expected: 3 ... Got: " + str(driver("((1+(3*2))-4)")))
     print(driver('bill'))
     print(driver('(bill-bill)'))

if __name__== "__main__":
    main()
