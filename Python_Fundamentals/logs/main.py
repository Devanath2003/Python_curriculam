from validators import is_valid_email
from formatters import build_response

def register_endpoint(email: str) -> dict:
    if not is_valid_email(email):
        return build_response("error",{"message": "Invalid email address"})
    return build_response("success", {"registered_email": email.lower()})

if __name__ == "__main__":
    print(register_endpoint("devanath@comapny.com"))
    print(register_endpoint("invalid-email"))