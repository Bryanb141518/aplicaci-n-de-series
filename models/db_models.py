from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

# Tabla usuarios
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)

# Tabla series
class SerieDB(Base):
    __tablename__ = "series"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    genero = Column(String, nullable=False)
    plataforma = Column(String)
    anio = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=False)

# Tabla series_vistas
class SerieVistaDB(Base):
    __tablename__ = "series_vistas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    serie_id = Column(Integer, ForeignKey("series.id"))
    calificacion = Column(Float)

# Tabla favoritas
class FavoritaDB(Base):
    __tablename__ = "favoritas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    serie_id = Column(Integer, ForeignKey("series.id"))

# Tabla lista_de_usuarios
class ListaUsuarioDB(Base):
    __tablename__ = "lista_de_usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nombre_lista = Column(String, nullable=False)
    serie_id = Column(Integer, ForeignKey("series.id"))
