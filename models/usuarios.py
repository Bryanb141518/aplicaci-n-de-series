from re import fullmatch
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


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


class Usuariomodel(BaseModel):

    nombre : str = Field(min_length=1, max_length=100)

    apellido : str = Field(min_length=1, max_length=100)

    ciudad : str = Field(min_length=1, max_length=100)

    edad : int = Field(..., ge=5, le=120)

    correo : str = Field(min_length=1, max_length=100)

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








