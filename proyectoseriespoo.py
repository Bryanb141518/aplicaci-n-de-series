class Series:
    def __init__(self, nombre, genero: str,calificacion:float = None,estado:str ="pendiente",
                 plataforma:str = None,año:int = None,descripcion:str = None):

        self.nombre = nombre
        self.genero = genero
        self.calificacion = calificacion
        self.estado = estado
        self.plataforma = plataforma
        self.año = año
        self.descripcion = descripcion

# manejo de errores en la entrada de los datos con lista de errores
    def Validar_datos(self):
        while True:
            errores = []
#validar el nombre de la serie
            if not isinstance(self.nombre, str) or not self.nombre.strip():
                errores.append("el nombre debe ser texto y no puede estar vacio")
#validar el genero de la serie
            if not isinstance(self.genero, str) or not self.genero.strip():
                errores.append("el genero debe ser texto y no puede ser vacio")
# validar la clasificacion
            if self.calificacion is not None:
                try:
                    calificacion = float(self.calificacion)

