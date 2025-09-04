def info():
    """informacion registro de series vistas
        con muenu de opcciones
    1 = agregar una serie
    2 = buscar serie por calificacion
    3 = buscar serie por nombre
    4 = mostrar todas las serie vistas
    5 = lista de series que quiero ver
    6 = eliminar serie
    7 = salir"""

"""se crea un def para la validacion solo print que muestran las opcciones a escoger
   primero se cre un def solo con la informacion el segundo print dentro del while es el que 
    va a validar con el diccionario de abajo segun lo que se coloque """

def menu_de_opcciones():
    while True:
        print("        SISTEMA DE CALIFICACION Y ALAMACENAMIENTO DE SERIES Y SU PUNTUACION")
        print("1. Agregar una serie")
        print("2. Buscar serie por calificacion")
        print("3. buscar serie por nombre")
        print("4. Mostrar todas las serie vistas ")
        print("5. lista de serie que quiero ver")
        print("6. Eliminar serie ")
        print("7. Salir")

# validacion de el primer input del usuario
        try:
            seleccion = input("ingrese una opccion entre (1-5)").strip() # el strip lo que hace es eliminar espacios

            if not seleccion.isdigit(): # validar que solo tenga numeros del 0 al 9
                print("error debe ingresar un numero")
                continue
            seleccion = int(seleccion)

            if seleccion < 1 or seleccion > 7:
                print("error debe ingresar un numero entre 1 y 7")
                continue
            opciones = {
                1: "Agregar una serie",
                2: "Buscar serie por calificacion",
                3: "Buscar serie por nombre",
                4: "Mostrar todas las serie vistas",
                5: "Lista de serie que quiero ver",
                6: "Eliminar serie ",
                7: lambda: print("saliendo del programa") # se hace con lambda para no tener que crear un def para salir

            }

            if seleccion == 7:
                break
        except ValueError:
            print("error entrada invalida")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


lista_de_serie  = []
series_vistas = []

def Agregar_serie():
    while True:
        nombre = input("ingrese el nombre de la seire que desea agregar").strip()
        if not nombre.strip(): # strip elimina espacios en blanco al inicio y al final y verifica de que nombre no este vacio
            print("error el nombre no puede esta vacio ")
            continue
#    aca recorremos con for para revisar que cada caracter no tenga numeros
        if any(char.isdigit() for char in nombre):
            print("Error: el nombre no puede tener números")
            continue
#    aca validamso que no se repita el nombre de la serie cuando la ingres eel usuario
        if not nombre in lista_de_serie:
            print("ya tienes esa serie en vistas no la puedes repetir")
            continue
        try:
            calificacion = float(input("ingrese la calificacion de la serie un numero de 1 al 10"
                                       "donde de 1 a 4 es muy mala de 4 a 8 es regual y mas de 8 es exelente"))
        except ValueError:
            print("error entrada invalida ingresa un numero entre 1 y 10")
            continue





















