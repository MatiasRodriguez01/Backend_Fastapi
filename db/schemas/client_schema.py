def client_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": str(user["email"]),
        "url": str(user["url"])
    }


def clients_schema(clients) -> list: 
    return [client_schema(client) for client in clients]