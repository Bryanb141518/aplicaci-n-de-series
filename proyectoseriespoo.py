from re import fullmatch
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

class Series:
    def __init__(self, nombre: str, genero: str, plataforma: str, año: int, descripcion: str):
        # Nada es opcional - todo obligatorio

        self.nombre = nombre
        self.genero = genero
        self.plataforma = plataforma
        self.año = año
        self.descripcion = descripcion

# manejo de errores en la entrada de los datos con lista de errores

    def Validar_datos(self):

            errores = []

#validar el nombre de la serie

            if not isinstance(self.nombre, str):
                errores.append("el nombre debe ser texto")
            if not  self.nombre.strip():
                errores.append("el nombre no puede ir vacio")
            if self.nombre.isdigit():
                errores.append("el nombre no puede tener solo numeros")
            if self.nombre.isupper():
                errores.append("el titulo no puede estar todo en mayusculas")



#validar el genero de la serie

            if not isinstance(self.genero, str):
                errores.append("el genero debe ser texto")
            if not self.genero.strip():
                errores.append("el genero no puede ir vacio")
            if self.genero.isdigit():
                errores.append("el genero no puede tener solo numeros")
            if self.genero.isupper():
                errores.append("el genero no puede estar todo en mayusculas")


#validar plataforma
            if not isinstance(self.plataforma, str):
                errores.append("el texto de plataforma debe ser texto")
            if not self.plataforma.strip():
                errores.append("la plataforma no puede ir vacio")
            if self.plataforma.isdigit():
                errores.append("la plataforma no puede tener solo numeros")
            if self.plataforma.isupper():
                errores.append("la plataforma no puede estar todo en mayusculas")

#validar el año de la series
            if not isinstance(self.año, int):
                errores.append("el año tiene que ser un numero entero.")
            else:
                if self.año < 1920 :
                    errores.append("el año de estreno de la pelula no puede ser menor a al era del televisor")
                año_actual = datetime.now().year
        # con esto validamos que no se pued eingresar un año mayor  dos en el futuro
                if self.año > año_actual + 2:
                    errores.append("el año no puede ser mayor a dos año en el futuro")

# validar la descripccion de la pelicula

            if not isinstance(self.descripcion, str):
                errores.append("el descripcion debe ser texto")

            if not self.descripcion.strip():
                errores.append("el descripcion no puede ir vacio")

            if self.descripcion.isdigit():
                errores.append("el descripcion no puede tener solo numeros")

            if self.descripcion.isupper():
                errores.append("el descripcion no puede estar todo en mayusculas")

            if len(self.descripcion.strip()) < 10:
                errores.append("La descripción debe tener al menos 10 caracteres")

            if len(self.descripcion.strip()) > 1000:
                errores.append("La descripción no puede exceder 1000 caracteres")


            if any(patron in self.descripcion for patron in ["http://", "https://", "www.", "@"]):
                errores.append("La descripción no puede contener URLs o emails")

 # ✅ SOLO SI NO HAY ERRORES, formateamos los datos (TODO JUNTO AL FINAL)
            if not errores:
                self.nombre = self.nombre.strip().title()
                self.genero = self.genero.strip().capitalize()
                self.plataforma = self.plataforma.strip().capitalize()  # ✅ Directo, sin is not None
                self.descripcion = self.descripcion.strip()  # ✅ Directo, sin is not None

            return errores