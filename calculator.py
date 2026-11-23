def add(x, y):
    return x + y

def substract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def main():

    print("Simple Calculator")
    print("Select operation:")

    x = float(input("Enter first number: "))
    op = input("Operration: ")
    y = float(input("Enter second number: "))

    if op == '+':
        print("Result:", add(x, y))
    elif op == '-':
        print("Result:", substract(x, y))
    elif op == '*':
        print("Result:", multiply(x, y))
    elif op == '/':
        print("Result:", divide(x, y))
    else:
        print("Invalid operation.")

if __name__ == "__main__":
    main()