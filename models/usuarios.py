
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field, field_validator, EmailStr
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
class LoginModel(BaseModel):
    correo: EmailStr
    contrasena: str

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
@app.post("/usuarios", status_code=201)
def create_usuario(usuario: Usuariomodel):
    # Validación 1: Edad mínima
    if usuario.edad < 14:
        raise HTTPException(
            status_code=400,
            detail="Debes tener al menos 14 años para registrarte"
        )
    
    # Validación 2: Correo único
    for s in lista_usuarios:
        if s["correo"].lower() == usuario.correo.lower():
            raise HTTPException(
                status_code=400,
                detail=f"El correo '{usuario.correo}' ya existe en el sistema"
            )

    # Convertir los datos ya validados a diccionario
    nuevo_usuario = usuario.model_dump()

    # Guardar los datos en la lista
    lista_usuarios.append(nuevo_usuario)

    return {"mensaje": "Usuario registrado correctamente", "usuario": nuevo_usuario}

# Endpoint de login
@app.post("/usuarios/login")
def login(datos_login: LoginModel):
    # Buscar usuario por correo
    usuario = None
    for u in lista_usuarios:
        if u["correo"].lower() == datos_login.correo.lower():
            usuario = u
            break
    
    # Si no existe el usuario
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    # Verificar contraseña
    if usuario["contrasena"] != datos_login.contrasena:
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )
    
    # Login exitoso
    return {
        "mensaje": "Login exitoso",
        "usuario": {
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "correo": usuario["correo"]
            # NO devuelve la contraseña por seguridad
        }
    }

# Ver todos los registros del usuario
@app.get("/usuarios/todos")
def todos_los_registros():
    if not lista_usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios registrados")

# cuando se muesten los registros de usuarios no se muestre la contrasena 
    usuarios_sin_pass = []
    for u in lista_usuarios:
        copia = u.copy()
        copia.pop("contrasena", None)
        usuarios_sin_pass.append(copia)

    return {"total": len(usuarios_sin_pass), "usuarios": usuarios_sin_pass}

# busqueda de usuarios por nombre sin retornar su contrasena

@app.get("/usuarios/buscar/nombre/{nombre}")
def busqeuda_nombre(nombre: str):
    nombre_limpio = nombre.strip().lower()

    if not nombre_limpio:
        raise HTTPException(status_code=400, detail="el nombre no puede estar vacio")

    resultado = []
    for u in lista_usuarios:
        if u["nombre"].lower() == nombre_limpio:
            resultado.append(u)

    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontro usuario con ese nombre")

    # cuando se muesten los registros de usuarios no se muestre la contrasena
    usuarios_sin_pass = []
    for u in resultado:
        copia = u.copy()
        copia.pop("contrasena", None)
        usuarios_sin_pass.append(copia)

    return {
        "total": len(usuarios_sin_pass),
        "usuarios": usuarios_sin_pass
    }
# busqueda de usuarios por correo sin retornar su contrasena
@app.get("/usuarios/buscar/correo/{correo}")
def buscar_correo(correo: str):
    correo_limpio = correo.strip().lower()
    if not correo_limpio:
        raise HTTPException(status_code=400, detail="el correo no puede estar vacio")

    resultado = []
    for u in lista_usuarios:
        if u["correo"].lower() == correo_limpio:
            resultado.append(u)

    # cuando se muesten los registros de usuarios no se muestre la contrasena
    usuarios_sin_pass = []
    for u in resultado:
        copia = u.copy()
        copia.pop("contrasena", None)
        usuarios_sin_pass.append(copia)

    return {
        "total": len(usuarios_sin_pass),
        "usuarios": usuarios_sin_pass
    }

# busqueda de usuario por correo por que es un valor unico para la acutlizacion de los datos

@app.put("/usuarios/{correo}")
def actualizar_usuario(correo: str, datos: dict):
    correo_limpio = correo.strip().lower()

    for u in lista_usuarios:
        if u["correo"].lower() == correo_limpio:

            if "nombre" in datos:
                u["nombre"] = datos["nombre"]

            if "apellido" in datos:
                u["apellido"] = datos["apellido"]

            if "edad" in datos:
                u["edad"] = datos["edad"]

            if "contrasena" in datos:
                u["contrasena"] = datos["contrasena"]

            return {"mensaje": "Usuario actualizado", "usuario": u}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


#eliminacion de usuario por correo

@app.delete("/usuarios/{correo}")
def eliminar_usuario(correo: str):
    correo_limpio = correo.strip().lower()

    for u in lista_usuarios:
        if u["correo"].lower() == correo_limpio:
            lista_usuarios.remove(u)
            return {"mensaje": "Usuario eliminado correctamente"}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")
