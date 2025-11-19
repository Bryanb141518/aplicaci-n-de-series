from datetime import datetime
from http.client import HTTPException
from wsgiref.validate import validator

from fastapi import FastAPI
from pydantic import BaseModel, Field, constr, conint

lista_series = []

genero_validos = ["terror","drama"]

class Series:
    def __init__(self, nombre, genero, plataforma,  año,  descripcion ):
        # Nada es opcional - todo obligatorio

        self.nombre = nombre
        self.genero = genero
        self.plataforma = plataforma
        self.año = año
        self.descripcion = descripcion

# manejo de errores en la entrada de los datos con lista de errores

class SeriesModel(BaseModel):

# validacion de que el dato sea de tipo str que contenga almenos un caracter y maximo 100

    nombre : constr(min_length=1, max_length=100)

    genero : constr(min_length=1, max_length=100)

    plataforma : constr(min_length=1, max_length=100) = "Desconocida"



    @validator('nombre')
    def validate_nombre(cls, v):
        return v.strip().title()

    @validator('genero')
    def validate_genero(cls, v):
        if v.lower() not in genero_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Género '{v}' no permitido. Géneros válidos: {genero_validos}"
            )
        return v.strip().lower()