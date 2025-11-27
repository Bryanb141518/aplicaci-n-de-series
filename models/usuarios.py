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


    @field_validator("nombre", mode="before")
    def validate_nombre(cls, v):
        limpiar = v.strip()
        if not limpiar:
            raise ValueError("este campo no puede ir vacio")
        # recorremos el el texto con un for validando carater por carater para que no tenga numero
        #con any lo que hace es validar si almenos uno es True

        if any(char.isdigit() for char in limpiar):
            raise ValueError("el nombre no puede contener numeros")

        #no se permite simbolos ni carateres raros
        if not limpiar.replace(" ", "").isalpha():
            raise ValueError("el nombre solo puede contener letras y espacios")

        #el  nombre no puede contener menos de dops caracteres ni mas de 50
        if not (2 <= len(limpiar) <= 50):
            raise ValueError("el nombre debe tener entre 2 y 50 caracteres")

         # No permitir espacios internos por que solo es una palabra
        if " " in limpiar:
            raise ValueError("el nombre debe ser una sola palabra (sin espacios)")

        return limpiar.title()






