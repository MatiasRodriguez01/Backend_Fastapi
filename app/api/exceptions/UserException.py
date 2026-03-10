from fastapi import status, HTTPException

EXCEPTION_USER = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="Usuario no encontrado",
    headers={"WWW-Authenticate": "Bearer"}
)

EXCEPTION_USER_UPDATE = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail={
        "update": False,
        "detail": "El usuario no se pudo actualizar"
        },
    headers={"WWW-Authenticate": "Bearer"}
) 

EXCEPTION_USER_DELETE = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail={
        "update": False,
        "detail": "El usuario no se pudo eliminar"
        },
    headers={"WWW-Authenticate": "Bearer"}
) 

EXCEPTION_UPDATE_PASSWORD = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail={
        "update": False,
        "detail": "La contraseña no se pudo actualizar"
        },
    headers={"WWW-Authenticate": "Bearer"}

) 