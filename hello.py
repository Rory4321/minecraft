# hello.py
def greet(name):
    return f"Hello, {name}! Welcome to AI Club!"

def main():
    user_name = input("What's your name? ")
    message = greet(user_name)
    print(message)

    # Do a simple calculation
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print(f"{num1} + {num2} = {num1 + num2}")

if __name__ == "__main__":
    main()