from backend.services.memory import (
    add_message,
    get_history,
    clear_history
)


clear_history()

add_message(
    "user",
    "Hello"
)

add_message(
    "assistant",
    "Hi"
)

print(
    get_history()
)