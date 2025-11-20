
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# Inicializar la app de FastAPI
app = FastAPI()
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

    nombre : str = Field(min_length=1, max_length=100)

    genero : str = Field(min_length=1, max_length=100)

    plataforma: str = Field(default="Desconocida", min_length=1, max_length=100)

    año : int = Field(..., ge=1920, le=2028)

    descripcion : str = Field(min_length=100, max_length=1000)



    @field_validator('nombre', mode= "before")
    def validate_nombre(cls, v):
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("este campo no puede ir vacio")
        return cleaned.title()

    @field_validator('genero',mode= "before")
    def validate_genero(cls, v):
        cleaned = v.strip().lower()

        if cleaned not in genero_validos:
            raise ValueError(
                f"genero {v} no permitido generos invalidos {' '.join(genero_validos)}"
            )
        return cleaned

    @field_validator('descripcion', mode= "before")
    def validate_descripcion(cls, v):
        cleaned = v.strip().title()
        if not cleaned:
            raise ValueError("no puede conteenr solo espacios vacios")
        return cleaned

@app.post("/series",status_code=201)

def create_series(series: SeriesModel):
    nueva_serie = series.model_dump()

    lista_series.append(nueva_serie)

    return {"mensaje": "Serie creada correctamente", "serie": nueva_serie}


