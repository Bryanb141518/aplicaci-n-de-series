from re import fullmatch
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class Usuario:
    def __init__(self, nombre: str, apellido: str, edad: int, correo:str, contrasena:str):

        self._nombre = nombre
        self._apellido = apellido
        self._edad = edad
        self.__correo = correo
        self.__contrasena = contrasena

#clase model es la que tomara como referencia flastapi

class Usuariomodel(BaseModel):

    nombre : str = Field(min_length=1, max_length=100)

    apellido : str = Field(min_length=1, max_length=100)

    edad : int = Field(..., ge=5, le=120)

    correo : str = Field(min_length=1, max_length=100)

    contrasena : str = Field(min_length=1, max_length=100)


   





