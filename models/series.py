
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi import Body



# Inicializar la app de FastAPI
app = FastAPI()
lista_series = []
series_vistas = []
lista_creada_por_el_usuario = []
favoritas = []

genero_validos = ["terror","drama"]


# logic/series.py

class Series:
    def __init__(self, nombre: str, genero: str, plataforma: str, anio: int, descripcion: str):
        self.nombre = nombre
        self.genero = genero
        self.plataforma = plataforma
        self.anio = anio
        self.descripcion = descripcion

# manejo de errores en la entrada de los datos con lista de errores

class SeriesModel(BaseModel):

# validacion de que el dato sea de tipo str que contenga almenos un caracter y maximo 100

    nombre : str = Field(min_length=1, max_length=100)

    genero : str = Field(min_length=1, max_length=100)

    plataforma: str = Field(default="Desconocida", min_length=1, max_length=100)

    anio : int = Field(..., ge=1920, le=2028)

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

# Creación del objeto y guardado del objeto serie
@app.post("/series", status_code=201)
def create_series(series: SeriesModel):

    # 🔍 VALIDACIÓN: nombre repetido
    for s in lista_series:
        if s["nombre"].lower() == series.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail=f"La serie '{series.nombre}' ya existe en el sistema."
            )

    # Crear objeto limpio
    nueva_serie = series.model_dump()

    # Guardarlo en la lista
    lista_series.append(nueva_serie)

    return {"mensaje": "Serie creada correctamente", "serie": nueva_serie}


# creacion de guardar una serie en una lista si el usuario la marca como vista

#mostrar todas las series de la aplicacion
@app.get("/series/todas")
def mostrar_todas_las_series():
    if not lista_series:
        raise HTTPException(status_code=404, detail="No hay series registradas")

    return {"total": len(lista_series), "series": lista_series}

# creacion del get para la busqueda por nombre

@app.get("/series/buscar/nombre")
def buscar_en_todas(nombre:str):
    for s in lista_series:
        if s["nombre"].lower() == nombre.lower():
            return {"resultado": s}
    raise HTTPException(status_code=404, detail="Serie no encontrada")

# bucar serie por año
@app.get("/series/buscar/anio")
def buscar_por_anio(anio: int):
    resultados = []

    for s in lista_series:
        if s["anio"] == anio:
            resultados.append(s)

    if not resultados:
        raise HTTPException(status_code=404, detail="No hay series de ese año")

    return {"series": resultados}

# buscar serie por genero
@app.get("/series/buscar/genero")
def buscar_genero(genero: str):
    genero = genero.strip().lower()

    resultados = []

    for s in lista_series:
        if "genero" in s and isinstance(s["genero"], str):
            if s["genero"].strip().lower() == genero:
                resultados.append(s)
    if not resultados:
        raise HTTPException(status_code=404,detail="No hay series de ese genero")
    return {"series": resultados}


@app.post("/series/vista", status_code=200)
def marcar_vista(nombre_serie: str = Body(...), calificacion: float = Body(..., ge=0, le=10)):
    serie = next((s for s in lista_series if s["nombre"].lower() == nombre_serie.lower()), None)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # agregar a series_vistas con calificación
    serie_usuario = serie.copy()
    serie_usuario["calificacion"] = calificacion

    if serie_usuario not in series_vistas:
        series_vistas.append(serie_usuario)
        return {"mensaje": f"Serie '{nombre_serie}' marcada como vista", "serie": serie_usuario}
    else:
        raise HTTPException(status_code=400, detail="Serie ya estaba marcada como vista")

# creacionde una clase completa para la creacion de listas de series

class listaModel(BaseModel):
    nombre : str = Field(min_length=1, max_length=50)

    @field_validator("nombre")
    def validar_nombre_lista(cls, v):
        v = v.strip()
        if v == "":
            raise ValueError("el nombre de la lista no puede ir vacio")
        return v


# buscar serie por nombre un una lista creada por el usuario
@app.post("/lista/crear",status_code=201, tags=["lista del usuario"])
def crear_lista(lista: listaModel):

    # validar que no exista lista con el mismo nombre
    for s in lista_creada_por_el_usuario:
        if s["nombre"].lower() == lista.nombre.lower():
            raise HTTPException(status_code=400, detail="ya existe una lista con ese nombre")

    nueva_lista = {
        "nombre": lista.nombre,
        "series": []
    }

    lista_creada_por_el_usuario.append(nueva_lista)

    return {
        "mensaje": "Lista creada correctamente",
        "lista": nueva_lista
    }
#con body lo que hacemos es indicar que busqeu los adato en la funcion del post no en la url
# con este post lo que se hace es agregar las series a las listas

@app.post("/lista/agregar", status_code=201, tags=["lista del usuario"])
def agregar_serie_a_lista(
    nombre_lista: str = Body(...),
    nombre_serie: str = Body(...)
):
    # Buscar la lista
    lista = next((l for l in lista_creada_por_el_usuario if l["nombre"].lower() == nombre_lista.lower()), None)
    if not lista:
        raise HTTPException(status_code=404, detail=f"No se encontró la lista '{nombre_lista}'")

    # Buscar la serie en lista_series
    serie = next((s for s in lista_series if s["nombre"].lower() == nombre_serie.lower()), None)
    if not serie:
        raise HTTPException(status_code=404, detail=f"No se encontró la serie '{nombre_serie}'")

    # Validar que no esté repetida en la lista
    if any(s["nombre"].lower() == nombre_serie.lower() for s in lista["series"]):
        raise HTTPException(status_code=400, detail=f"La serie '{nombre_serie}' ya está en esta lista")

    # Agregar serie
    lista["series"].append(serie)
    return {
        "mensaje": f"Serie '{nombre_serie}' agregada correctamente a la lista '{nombre_lista}'",
        "lista": lista
    }


@app.get("/listas/buscar/nombre")
def buscar_en_lista(nombre_lista: str, nombre_serie: str):

    for lista in lista_creada_por_el_usuario:
        if lista["nombre"].lower() == nombre_lista.lower():

            for s in lista["series"]:
                if s["nombre"].lower() == nombre_serie.lower():
                    return {"resultado": s}

            raise HTTPException(status_code=404, detail="La serie no está en esta lista")

    raise HTTPException(status_code=404, detail="Lista no encontrada")


# alamcenar en una lista las series favoritas por el usuario

@app.post("/lista/favorita", status_code=201, tags=["lista del usuario"])
def marcar_favoritas(
    nombre_serie: str = Body(...),
    calificacion: float = Body(..., ge=0, le=10)
):
    # Buscar la serie en lista_series
    serie = next((s for s in lista_series if s["nombre"].lower() == nombre_serie.lower()), None)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # Crear copia para el usuario y agregar calificación
    serie_usuario = serie.copy()
    serie_usuario["calificacion"] = calificacion

    if serie_usuario not in favoritas:
        favoritas.append(serie_usuario)
        return {"mensaje": f"Serie '{nombre_serie}' agregada a favoritos", "serie": serie_usuario}
    else:
        raise HTTPException(status_code=400, detail="Serie ya estaba en favoritos")

#eliminar una serie de la lista de favoritos

@app.delete("/borrar/favorita")
def eliminar_favoritas(nombre_serie: str):
    for s in favoritas:
        if s["nombre"].lower() == nombre_serie.lower():
            favoritas.remove(s)
            return {"mensaje": f"Serie '{nombre_serie}' eliminada de favoritos"}

    raise HTTPException(status_code=404, detail="Serie no esta en favoritas")

#eliminar serie de una lista creada por el usuario
@app.delete("/lista/eliminar", tags=["lista del usuario"])
def eliminar_serie(nombre_lista: str,nombre_serie: str):
    # 1. Buscar la lista
    lista = next(
        (l for l in lista_creada_por_el_usuario if l["nombre"].lower() == nombre_lista.lower()),
        None
    )
    if not lista:
        raise HTTPException(status_code=404,detail="lista no encontrada")

    # 2 buscar la serie dentro de la lista
    serie = next(
        (s for s in lista["series"] if s["nombre"].lower() == nombre_serie.lower()),
        None
    )
    if not serie:
        raise HTTPException(status_code=404, detail="la serie no esta en esta lista")

    # 3 eliminar seire

    lista["series"].remove(serie)
    return {"mensaje": f"Serie '{nombre_serie}' eliminada de la lista '{nombre_lista}'"}