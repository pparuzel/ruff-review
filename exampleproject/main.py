# You can have any logic in this project,
# stage the changes, and ruff will verify them.

def BadCode() -> int:
    x = 'helo wrold'
    if id(x) % 3 == 0:
        return 42
    return x

if __name__ == "__main__":
    print(BadCode())
