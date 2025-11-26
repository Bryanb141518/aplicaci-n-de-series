from fastapi import FastAPI, HTTPException, Body
from models.series import SeriesModel
# from models.usuarios import UsuarioModel  # Solo si necesitas trabajar con usuarios
# from logic.serie import Series             # Solo si necesitas la lógica aparte
# from logic.usuario import Usuario          # Solo si necesitas la lógica aparte

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "Hola FastAPI"}

# Ejemplo de rutas básicas con SeriesModel
@app.post("/series")
def crear_serie(serie: SeriesModel):
    return {"mensaje": "Serie creada", "data": serie}

@app.get("/series/todas")
def mostrar_series():
    return {"mensaje": "Aquí van todas las series"}

@app.get("/series/buscar/nombre")
def buscar_por_nombre(nombre: str):
    return {"resultado": f"Buscando {nombre}"}
