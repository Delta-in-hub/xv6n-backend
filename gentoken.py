import uuid


def generate_token(username: str) -> str:
    return f"{username}-{uuid.uuid4().hex}"


if __name__ == "__main__":
    print(generate_token("admin"))
