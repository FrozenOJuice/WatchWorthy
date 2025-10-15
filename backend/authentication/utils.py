import os, json
from typing import List, Dict, Any, Optional

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

def user_exists(users: List[Dict[str, Any]], username: str, email: str) -> tuple[bool, Optional[str]]:
    username_taken = any(user["username"] == username for user in users)
    email_taken = any(user["email"] == email for user in users)

    if username_taken and email_taken:
        return True, "Username and Email already taken"
    elif username_taken:
        return True, "Username already taken"
    elif email_taken:
        return True, "Email already taken"
    else:
        return False, None
    
def load_users() -> List[Dict[str, Any]]:
    with open(USERS_FILE, "r") as f:
        try:
            users = json.load(f)
            return users
        except json.JSONDecodeError:
            return []

def save_users(users: List[Dict[str, Any]]) -> None:
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)