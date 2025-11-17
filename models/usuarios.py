from re import fullmatch
from datetime import datetime

from datetime import datetime


class Usuario:
    def __init__(self, nombre: str, apellido: str, edad: int, correo:str, contrasena:str):

        self._nombre = nombre
        self._apellido = apellido
        self._edad = edad
        self.__correo = correo
        self.__contrasena = contrasena

#esta funcion es la puerta para mostra el atributo nombre

    @property
    def nombre(self):
        return self._nombre

# con este set lo que hacemos es validar y darle instrucciones a nombre
    @nombre.setter
    def nombre(self, nuevo_nombre):

        if not isinstance(nuevo_nombre, str):
            raise TypeError("El nombre debe ser texto.")

        if not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if len(nuevo_nombre.strip()) < 3:
            raise ValueError("El nombre debe tener 3 caracteres como minimo.")

        self._nombre = nuevo_nombre.strip().capitalize()


    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, nuevo_apellido):
        if not isinstance(nuevo_apellido, str):
            raise TypeError("El apellido debe ser texto.")

        if not nuevo_apellido.strip():
            raise ValueError("el  apellido no puede estar vacio ")

        if len(nuevo_apellido.strip()) < 3:
            raise ValueError("El apellido debe tener 3 caracteres como minimo.")

        self._apellido = nuevo_apellido.strip().capitalize()


    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, nueva_edad):
        if not isinstance(nueva_edad, int):
            raise TypeError("El edad debe ser un numero entero.")

        if nueva_edad < 16 :
            raise ValueError("la persona tiene que tener mas de 16 anos para poder registrarse .")

        if nueva_edad > 100 :
            raise ValueError("numero ingresado para la edad invalido")

        self._edad = nueva_edad

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):

        if not isinstance(nuevo_correo, str):
            raise TypeError("El correo debe ser de tipo texto.")

        if not nuevo_correo.strip():
            raise ValueError("el correo no puede ir vacio")

# con ese import validamos el formato del correo

        if not fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", nuevo_correo):
            raise ValueError(" Formato de correo @gmail.com inválido")

        if " " in nuevo_correo:
            raise ValueError("El correo no puede contener espacios.")

        self.__correo = nuevo_correo

    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, nueva_contrasena):

        if not isinstance(nueva_contrasena, str):
            raise TypeError("El contrasena debe ser de tipo texto.")

        if not nueva_contrasena.strip():
            raise ValueError("el campo de contrasena no puede ir vacio")

        if not fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", nueva_contrasena):
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.")
        if " " in nueva_contrasena:
            raise ValueError("La contraseña no puede contener espacios.")

        self.__contrasena = nueva_contrasena






