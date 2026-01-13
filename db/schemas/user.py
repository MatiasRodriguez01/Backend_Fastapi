def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": str(user["email"]),
        "url": str(user["url"])
    }


def users_schema(clients) -> list: 
    return [user_schema(client) for client in clients]