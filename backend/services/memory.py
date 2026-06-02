import json
from pathlib import Path

MEMORY_FILE = Path(
    "backend/data/history.json"
)


def load_history():

    if not MEMORY_FILE.exists():
        return []

    with open(
        MEMORY_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_history(history):

    with open(
        MEMORY_FILE,
        "w"
    ) as f:

        json.dump(
            history,
            f,
            indent=2
        )


def add_message(role, content):

    history = load_history()

    history.append(
        {
            "role": role,
            "content": content
        }
    )

    save_history(history)


def get_history():

    return load_history()


def clear_history():

    save_history([])