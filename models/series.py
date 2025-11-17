from datetime import datetime


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