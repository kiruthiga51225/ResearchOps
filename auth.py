import json
import hashlib
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "users.json"


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def load_users():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            users,
            f,
            indent=4
        )


def register_user(username, password):
    users = load_users()

    if username in users:
        return False, "Username already exists."

    users[username] = {
        "password": hash_password(password),
        "search_history": []
    }

    save_users(users)

    return True, "Account created successfully."


def login_user(username, password):
    users = load_users()

    if username not in users:
        return False, "User not found."

    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password."

    return True, "Login successful."


def add_search(username, question, report):
    users = load_users()

    if username not in users:
        return

    users[username]["search_history"].append({
        "question": question,
        "report": report
    })

    save_users(users)


def get_history(username):
    users = load_users()

    if username not in users:
        return []

    return users[username].get(
        "search_history",
        []
    )