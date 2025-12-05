from datetime import datetime
from fastapi import FastAPI, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator, EmailStr

# Importar configuración de base de datos y modelos
from .database import get_db
from .db_models import SerieDB, SerieVistaDB, FavoritaDB, ListaUsuarioDB, UsuarioDB

# Inicializar la app de FastAPI
app = FastAPI()

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

class listaModel(BaseModel):
    nombre : str = Field(min_length=1, max_length=50)

    @field_validator("nombre")
    def validar_nombre_lista(cls, v):
        v = v.strip()
        if v == "":
            raise ValueError("el nombre de la lista no puede ir vacio")
        return v

# ==================== ENDPOINTS CON SQLALCHEMY ====================

# CREAR SERIE
@app.post("/series", status_code=201)
def create_series(series: SeriesModel, db: Session = Depends(get_db)):

    # VALIDACIÓN: nombre repetido
    existe = db.query(SerieDB).filter(SerieDB.nombre == series.nombre).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail=f"La serie '{series.nombre}' ya existe en el sistema."
        )

    # Crear serie en la base de datos
    nueva_serie = SerieDB(
        nombre=series.nombre,
        genero=series.genero,
        plataforma=series.plataforma,
        anio=series.anio,
        descripcion=series.descripcion
    )

    db.add(nueva_serie)
    db.commit()
    db.refresh(nueva_serie)

    return {
        "mensaje": "Serie creada correctamente",
        "serie": {
            "id": nueva_serie.id,
            "nombre": nueva_serie.nombre,
            "genero": nueva_serie.genero,
            "plataforma": nueva_serie.plataforma,
            "anio": nueva_serie.anio,
            "descripcion": nueva_serie.descripcion
        }
    }

# MOSTRAR TODAS LAS SERIES
@app.get("/series/todas")
def mostrar_todas_las_series(db: Session = Depends(get_db)):
    series = db.query(SerieDB).all()
    
    if not series:
        raise HTTPException(status_code=404, detail="No hay series registradas")

    series_list = [
        {
            "id": s.id,
            "nombre": s.nombre,
            "genero": s.genero,
            "plataforma": s.plataforma,
            "anio": s.anio,
            "descripcion": s.descripcion
        }
        for s in series
    ]

    return {"total": len(series_list), "series": series_list}

# BUSCAR SERIE POR NOMBRE
@app.get("/series/buscar/nombre")
def buscar_en_todas(nombre: str, db: Session = Depends(get_db)):
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre)).first()
    
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    
    return {
        "resultado": {
            "id": serie.id,
            "nombre": serie.nombre,
            "genero": serie.genero,
            "plataforma": serie.plataforma,
            "anio": serie.anio,
            "descripcion": serie.descripcion
        }
    }

# BUSCAR SERIE POR AÑO
@app.get("/series/buscar/anio")
def buscar_por_anio(anio: int, db: Session = Depends(get_db)):
    series = db.query(SerieDB).filter(SerieDB.anio == anio).all()

    if not series:
        raise HTTPException(status_code=404, detail="No hay series de ese año")

    series_list = [
        {
            "id": s.id,
            "nombre": s.nombre,
            "genero": s.genero,
            "plataforma": s.plataforma,
            "anio": s.anio,
            "descripcion": s.descripcion
        }
        for s in series
    ]

    return {"series": series_list}

# BUSCAR SERIE POR GÉNERO
@app.get("/series/buscar/genero")
def buscar_genero(genero: str, db: Session = Depends(get_db)):
    genero_limpio = genero.strip().lower()

    series = db.query(SerieDB).filter(SerieDB.genero.ilike(genero_limpio)).all()
    
    if not series:
        raise HTTPException(status_code=404, detail="No hay series de ese genero")
    
    series_list = [
        {
            "id": s.id,
            "nombre": s.nombre,
            "genero": s.genero,
            "plataforma": s.plataforma,
            "anio": s.anio,
            "descripcion": s.descripcion
        }
        for s in series
    ]
    
    return {"series": series_list}

# MARCAR SERIE COMO VISTA
@app.post("/series/vista", status_code=200)
def marcar_vista(
    usuario_id: int = Body(...),
    nombre_serie: str = Body(...),
    calificacion: float = Body(..., ge=0, le=10),
    db: Session = Depends(get_db)
):
    # Buscar la serie
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre_serie)).first()
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # Verificar si ya está marcada como vista
    ya_vista = db.query(SerieVistaDB).filter(
        SerieVistaDB.usuario_id == usuario_id,
        SerieVistaDB.serie_id == serie.id
    ).first()
    
    if ya_vista:
        raise HTTPException(status_code=400, detail="Serie ya estaba marcada como vista")

    # Crear registro de serie vista
    nueva_vista = SerieVistaDB(
        usuario_id=usuario_id,
        serie_id=serie.id,
        calificacion=calificacion
    )
    
    db.add(nueva_vista)
    db.commit()
    db.refresh(nueva_vista)

    return {
        "mensaje": f"Serie '{nombre_serie}' marcada como vista",
        "serie": {
            "id": serie.id,
            "nombre": serie.nombre,
            "calificacion": calificacion
        }
    }

# MARCAR SERIE COMO FAVORITA
@app.post("/lista/favorita", status_code=201, tags=["lista del usuario"])
def marcar_favoritas(
    usuario_id: int = Body(...),
    nombre_serie: str = Body(...),
    db: Session = Depends(get_db)
):
    # Buscar la serie
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre_serie)).first()
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # Verificar si ya está en favoritos
    ya_favorita = db.query(FavoritaDB).filter(
        FavoritaDB.usuario_id == usuario_id,
        FavoritaDB.serie_id == serie.id
    ).first()
    
    if ya_favorita:
        raise HTTPException(status_code=400, detail="Serie ya estaba en favoritos")

    # Crear registro de favorita
    nueva_favorita = FavoritaDB(
        usuario_id=usuario_id,
        serie_id=serie.id
    )
    
    db.add(nueva_favorita)
    db.commit()

    return {
        "mensaje": f"Serie '{nombre_serie}' agregada a favoritos",
        "serie": {
            "id": serie.id,
            "nombre": serie.nombre
        }
    }

# ELIMINAR SERIE DE FAVORITOS
@app.delete("/borrar/favorita")
def eliminar_favoritas(
    usuario_id: int = Body(...),
    nombre_serie: str = Body(...),
    db: Session = Depends(get_db)
):
    # Buscar la serie
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre_serie)).first()
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # Buscar en favoritos
    favorita = db.query(FavoritaDB).filter(
        FavoritaDB.usuario_id == usuario_id,
        FavoritaDB.serie_id == serie.id
    ).first()
    
    if not favorita:
        raise HTTPException(status_code=404, detail="Serie no esta en favoritas")

    db.delete(favorita)
    db.commit()

    return {"mensaje": f"Serie '{nombre_serie}' eliminada de favoritos"}

# CREAR LISTA PERSONALIZADA
@app.post("/lista/crear", status_code=201, tags=["lista del usuario"])
def crear_lista(
    usuario_id: int = Body(...),
    lista: listaModel = Body(...),
    db: Session = Depends(get_db)
):
    # Validar que no exista lista con el mismo nombre para ese usuario
    existe = db.query(ListaUsuarioDB).filter(
        ListaUsuarioDB.usuario_id == usuario_id,
        ListaUsuarioDB.nombre_lista.ilike(lista.nombre)
    ).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="ya existe una lista con ese nombre")

    return {
        "mensaje": "Lista creada correctamente. Usa /lista/agregar para añadir series",
        "nombre_lista": lista.nombre
    }

# AGREGAR SERIE A LISTA PERSONALIZADA
@app.post("/lista/agregar", status_code=201, tags=["lista del usuario"])
def agregar_serie_a_lista(
    usuario_id: int = Body(...),
    nombre_lista: str = Body(...),
    nombre_serie: str = Body(...),
    db: Session = Depends(get_db)
):
    # Buscar la serie
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre_serie)).first()
    if not serie:
        raise HTTPException(status_code=404, detail=f"No se encontró la serie '{nombre_serie}'")

    # Validar que no esté repetida en la lista
    existe = db.query(ListaUsuarioDB).filter(
        ListaUsuarioDB.usuario_id == usuario_id,
        ListaUsuarioDB.nombre_lista.ilike(nombre_lista),
        ListaUsuarioDB.serie_id == serie.id
    ).first()
    
    if existe:
        raise HTTPException(status_code=400, detail=f"La serie '{nombre_serie}' ya está en esta lista")

    # Agregar a la lista
    nueva_entrada = ListaUsuarioDB(
        usuario_id=usuario_id,
        nombre_lista=nombre_lista,
        serie_id=serie.id
    )
    
    db.add(nueva_entrada)
    db.commit()

    return {
        "mensaje": f"Serie '{nombre_serie}' agregada correctamente a la lista '{nombre_lista}'"
    }

# BUSCAR SERIE EN LISTA PERSONALIZADA
@app.get("/listas/buscar/nombre")
def buscar_en_lista(
    usuario_id: int,
    nombre_lista: str,
    nombre_serie: str,
    db: Session = Depends(get_db)
):
    # Buscar la serie
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre_serie)).first()
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # Buscar en la lista del usuario
    entrada = db.query(ListaUsuarioDB).filter(
        ListaUsuarioDB.usuario_id == usuario_id,
        ListaUsuarioDB.nombre_lista.ilike(nombre_lista),
        ListaUsuarioDB.serie_id == serie.id
    ).first()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="La serie no está en esta lista")

    return {
        "resultado": {
            "id": serie.id,
            "nombre": serie.nombre,
            "genero": serie.genero,
            "plataforma": serie.plataforma,
            "anio": serie.anio,
            "descripcion": serie.descripcion
        }
    }

# ELIMINAR SERIE DE LISTA PERSONALIZADA
@app.delete("/lista/eliminar", tags=["lista del usuario"])
def eliminar_serie(
    usuario_id: int = Body(...),
    nombre_lista: str = Body(...),
    nombre_serie: str = Body(...),
    db: Session = Depends(get_db)
):
    # Buscar la serie
    serie = db.query(SerieDB).filter(SerieDB.nombre.ilike(nombre_serie)).first()
    if not serie:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    # Buscar en la lista
    entrada = db.query(ListaUsuarioDB).filter(
        ListaUsuarioDB.usuario_id == usuario_id,
        ListaUsuarioDB.nombre_lista.ilike(nombre_lista),
        ListaUsuarioDB.serie_id == serie.id
    ).first()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="la serie no esta en esta lista")

    db.delete(entrada)
    db.commit()

    return {"mensaje": f"Serie '{nombre_serie}' eliminada de la lista '{nombre_lista}'"}
