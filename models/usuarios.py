
from datetime import datetime
from http.client import HTTPException

from fastapi import FastAPI
from fastapi.openapi.utils import status_code_ranges
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
# util cuando se nececita validar texto y constrasenas
import string
import re

app = FastAPI()
lista_usuarios = []
class Usuario:
    def __init__(self, nombre: str, apellido: str,  edad: int, correo:str, contrasena:str):

        self._nombre = nombre
        self._apellido = apellido
        self._edad = edad
        self.__correo = correo
        self.__contrasena = contrasena

#funcion para validar de una vez nombre y apellido
def validar_nombre_apellido(valor: str,campo: str) -> str:
    limpiar = valor.strip()

    if not limpiar:
        raise ValueError(f"este {campo} no puede ir vacio")

    if any(char.isdigit() for char in limpiar):
        raise ValueError(f"el {campo} no puede contener numeros")

    if not limpiar.replace(" ", "").isalpha():
        raise ValueError(f"el {campo} solo puede contener letras y espacios")

    if not (2 <= len(limpiar) <= 50):
        raise ValueError(f"el {campo} debe tener entre 2 y 50 caracteres")

    if " " in limpiar:
        raise ValueError(f"el {campo} debe ser una sola palabra sin espacios")

    return limpiar.title()

#clase model es la que tomara como referencia flastapi

# esta variable contiene todos los caracteres especiales del string para la validacion de constrasena
caracter_especial = string.punctuation
class Usuariomodel(BaseModel):

    nombre : str = Field(min_length=1, max_length=100)

    apellido : str = Field(min_length=1, max_length=100)

    edad : int = Field(..., ge=5, le=120)

    correo: EmailStr = Field(min_length=1, max_length=100)

    contrasena : str = Field(min_length=1, max_length=100)


    @field_validator("nombre",mode="before")
    def validar_nombre(cls, v):
        return validar_nombre_apellido(v,"nombre")

    @field_validator("apellido",mode="before")
    def validar_apellido(cls, v):
        return validar_nombre_apellido(v,"apellido")

    @field_validator("edad",mode="before")
    def validar_edad(cls, v):
        # Si viene como entero, solo retornarlo
        if isinstance(v, int):
            return v

        # Si viene como string
        if isinstance(v, str):
            limpio = v.strip()

            if not limpio:
                raise ValueError("El campo edad no puede ir vacío")

            if not limpio.isdigit():
                raise ValueError("La edad debe ser un número entero")

            return int(limpio)

        # Si viene cualquier otro tipo
        raise ValueError("La edad debe ser un número entero válido")


    @field_validator("contrasena",mode="before")

    def validar_contrasena(cls, v):
        if not isinstance(v, str):
            raise ValueError("la contrasena debe ser un texto")

        if len (v) < 6:
            raise ValueError("la contrasena debe tener al menos 6 caracteres")

        # Al menos un número
        if not re.search(r"\d", v):
            raise ValueError("la contrasena debe tener al menos un número")

        # Al menos un carácter especial
        if not re.search(f"[{re.escape(caracter_especial)}]", v):
            raise ValueError("la contrasena debe tener al menos un caracter especial")

        # debe tener al menos una mayuscula
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
        # no puede contener espacios
        if " " in v:
            raise ValueError("La contraseña no debe contener espacios")

         # Al menos una minúscula
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")

        return v

# validacion con endpoint las validaciones del negocio y guardado de datos
@app.post("/usuarios" ,status_code=201)
def create_usuario(usuario: Usuariomodel):
    # Validar que el correo no sea el mismo
    for s in lista_usuarios:
        if s["correo"].lower() == usuario.correo.lower():
            raise HTTPException(
                status_code=400,
                detail=f"el correo '{usuario.correo}' ya existe en el sistema"
            )

    #convertir los datos ya validados a una lista con los datos en diccioanrio
    nuevo_usuario = usuario.model_dump()

    #guardar los datos en una lista
    lista_usuarios.append(nuevo_usuario)

    return {"mensaje": "usuario registrado correctamente", "serie": lista_usuarios}






