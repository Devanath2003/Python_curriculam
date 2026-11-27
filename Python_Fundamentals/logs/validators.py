# File: app_utils/validators.py

def is_valid_email(email:str) -> bool:
    return "@" in email and "." in email.split("@")[-1]


# Only runs if we execute this file directly - NOT when imported
print("Running standalone validator tests..")
print(is_valid_email("devanath@company.com"))