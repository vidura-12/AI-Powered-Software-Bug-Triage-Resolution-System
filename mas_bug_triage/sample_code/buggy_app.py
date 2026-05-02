# sample_code/buggy_app.py
# Deliberately buggy Python file — used for testing the MAS system

def divide_numbers(a: int, b: int) -> float:
    # BUG on line 5: No check for division by zero
    return a / b


def get_user_age(user_dict: dict) -> int:
    # BUG on line 10: No check if 'age' key exists in dict
    return user_dict["age"]


def connect_to_database(host: str, port: int):
    # BUG on line 15: hardcoded credentials — security vulnerability
    username = "admin"
    password = "admin123"
    print(f"Connecting to {host}:{port} as {username}")


# This line will crash at runtime — ZeroDivisionError
result = divide_numbers(100, 0)
print(result)