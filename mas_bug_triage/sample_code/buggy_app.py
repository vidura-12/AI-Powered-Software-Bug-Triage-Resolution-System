# sample_code/buggy_app.py
# This is a deliberately buggy file for testing the MAS

def divide_numbers(a: int, b: int) -> float:
    # BUG: No check for division by zero
    return a / b


def get_user_age(user_dict: dict) -> int:
    # BUG: No check if 'age' key exists
    return user_dict["age"]


result = divide_numbers(100, 0)   # Line 12: This will crash
print(result)