from db.modules.base_module import Base 

def show_fields(obj) -> list[str]:
    return [key for key in obj.keys() if key != "_id"]


def show_schema(obj) -> dict:

    result: Base = { "id": str(obj["_id"])}
    fields: list[str] = show_fields(obj)

    for f in fields:
        value = obj[f]
        result[f] = value
    return result

def show_schemas(objects) -> list[dict]:   
    result: list[dict] = []
    for obj in objects:
        fields: list[str] = show_fields(obj)
        result.append(show_schema(obj))  
    return result
    #return [to_schema(obj, show_fields(obj)) for obj in objects]