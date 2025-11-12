def info():
    """informacion registro de series vistas
        con muenu de opcciones
    1 = agregar una serie
    2 = buscar serie por calificacion
    3 = buscar serie por nombre
    4 = buscar serie por genero
    5 = mostrar todas las serie vistas
    6 = guardar una serie para ver despues
    7 = lista de series pendientes
    8 = eliminar serie
    9 = salir"""

"""se crea un def para la validacion solo print que muestran las opcciones a escoger
   primero se cre un def solo con la informacion el segundo print dentro del while es el que 
    va a validar con el diccionario de abajo segun lo que se coloque """
class menu:
    def menu_de_opcciones(self):
        while True:
            print("        SISTEMA DE CALIFICACION Y ALAMACENAMIENTO DE SERIES Y SU PUNTUACION")
            print("1. Agregar una serie")
            print("2. Buscar serie guardada por calificacion")
            print("3. buscar serie guardada por nombre")
            print("4. buscar  serie guardada por genero")
            print("5. Mostrar todas las serie vistas ")
            print("6. guardar una serie para ver despues")
            print("7. lista de series pendientes")
            print("8. eliminar serie")
            print("9. Salir")

    # validacion de el primer input del usuario
            try:
                seleccion = input("ingrese una opccion entre (1-9)").strip() # el strip lo que hace es eliminar espacios

                if not seleccion.isdigit(): # validar que solo tenga numeros del 0 al 9
                    print("error debe ingresar un numero")
                    continue
                seleccion = int(seleccion)

                if seleccion < 1 or seleccion > 9:
                    print("error debe ingresar un numero entre 1 y 9")
                    continue
                opciones = {
                    1: "Agregar una serie",
                    2: "Buscar serie guardada por calificacion",
                    3: "Buscar serie guardada por nombre",
                    4: "buscar serie guardada por genero",
                    5: "Mostrar todas las serie vistas",
                    6: "guardar una serie para ver despues",
                    7: "lista de series pendientes",
                    8: "Eliminar serie ",
                    9: lambda: print("saliendo del programa") # se hace con lambda para no tener que crear un def para salir

                }
                if seleccion == 1:
                    Agregar_serie()
                elif seleccion == 2:
                    Buscar_serie()
                elif seleccion == 3:
                    Buscar_serie()
                elif seleccion == 4:
                    Buscar_serie()
                elif seleccion == 5:
                    Mostrar_series()
                elif seleccion == 6:
                    Series_pendientes()
                elif seleccion == 7:
                    Series_pendientes()
                elif seleccion == 8:
                    Eliminar_series()
                elif seleccion == 9:
                    break
            except ValueError:
                print("error entrada invalida")
            except Exception as e:
                print(f"❌ Error inesperado: {e}")


lista_de_serie  = []
series_vistas = []
ver_mas_tarde = []

    def Agregar_serie():
        while True:
            nombre = input("ingrese el nombre de la seire que desea agregar").strip()
            if not nombre.strip(): # strip elimina espacios en blanco al inicio y al final y verifica de que nombre no este vacio
                print("error el nombre no puede esta vacio ")
                continue
#       aca recorremos con for para revisar que cada caracter no tenga numeros
            if any(char.isdigit() for char in nombre):
                print("Error: el nombre no puede tener números")
                continue
#    aca validamso que no se repita el nombre de la serie cuando la ingres eel usuario
            if  nombre in series_vistas:
                print("ya tienes esa serie en vistas no la puedes repetir")
                continue
# validacion de opcciones para gurdar en ver mas tarde o guardar en vista
            try:
                opccion = int(input("ingrese una opccion (1 o 2) donde 1 es para guardar la serie en vistas y dos es para guardar en ver mas tarde"))
                if opccion >=1 and opccion <=2:

                    if opccion == 1:
                        genero = input("ingrese el genero de la serie").strip()
                        if  not genero:
                            print("error: el genero no puede ir vacio")
                            continue
                        try:
                            calificacion = float(input("ingrese la calificacion de la serie un numero de 1 al 10"
                                               "donde de 1 a 4 es muy mala de 4 a 8 es regual y mas de 8 es exelente"))
                            if calificacion < 1 or calificacion > 10:
                                print("debe ingresar un numero entre 1 y 10")
                                continue

                        except ValueError:
                            print("error entrada invalida ingresa un numero entre 1 y 10")
                            continue

                        series_vistas.append({"nombre": nombre, "calificacion": calificacion, "genero": genero})
                        print(f"✅ Serie '{nombre}' agregada a Vistas con calificación {calificacion}")

                    elif opccion == 2:
                        genero = input("ingrese la genero de la serie").strip()
                        if not genero:
                            print("error: el genero no puede ir vacio")
                            continue
                        ver_mas_tarde.append({"nombre": nombre ,"genero": genero})
                        print(f"✅ Serie '{nombre}' agregada a Ver más tarde")

                    else:
                        print("error invalido ingrese una opccion entre 1 y 2")

            except ValueError:
                print("error entrada ingrese una opccion entre 1 y 2")

    def Buscar_serie():
        while True:

            print("ingrese una de las opcciones de busqeuda que tenemos 1 es por calificacion 2 es por nombre 3 es por genero ")
            try:

                ingreso = int(input("ingrese una opccion entre 1 y 3"))

                if not ingreso:
                    print("error invalido no puede esta vacio ")
                    continue

                if ingreso < 1 or ingreso > 3:
                    print("error invalido ingrese una opccion entre 1 y 3")
                    continue

                if ingreso == 1:
                    genero = int(input("ingrese la calificacion de la serie").strip())

                    if not genero:
                        print("error: el genero no puede ir vacio")
                        continue

                    if genero <1 or genero > 10:
                        print("error invalido ingrese una calificacion entre 1 y 10")
                        continue

                    encontradas = []

                    for serie in series_vistas:
                        if  serie["calificacion"] == genero:
                            encontradas.append(serie)

                    if encontradas:

                        print("series encontradas con esta calificacion")
                        for s in encontradas:
                            print(f"- {s['nombre']} ({s['genero']}) ⭐ {s['calificacion']}")

                    else:
                        print("series no encontrada con esta calificacion")


                elif ingreso == 2:

                    nombre = input("ingrese el nombre de la serie")

                    if not nombre:
                        print("error: el nombre no puede ser vacio")
                        continue

                    encontradas = []

                    for n in series_vistas:
                        if  n["nombre"] == nombre:
                            encontradas.append(n)

                    if encontradas:
                        print("series encontradas con este nombre")
                        for s in encontradas:
                            print(f"- {s['nombre']} ({s['genero']}) ⭐ {s['calificacion']}")

                    else:
                        print("series no encontrada con ese nombre")



                elif ingreso == 3:
                    print("ingrese el genero de la serie que esta buscando")

                    genero = input("ingrese el genero de la serie").strip()

                    if not genero:
                        print("error: el genero no puede ir vacio")
                        continue

                    encontradas = []
                    for g in series_vistas:
                        if g["genero"] == genero:
                            encontradas.append(g)

                    if encontradas:
                        print("series encontradas con ese genero")
                        for s in encontradas:
                            print(f"- {s['nombre']} ({s['genero']}) ⭐ {s['calificacion']}")

                    else:
                        print("series no encontrada con ese genero")

            except ValueError:
                print("error entrada ingrese una opccion entre 1 y 3")



    def Mostrar_series():
        while True:
            print("ingrese una de las dos opcciones 1 para ver todas las series vistas y 2 para ver todas las series guardadas para ver mas tarde")
            try:
                ingreso = int(input("ingrese una opccion entre 1 y 2"))
                if not ingreso:
                    print("error invalido no puede esta vacio el campo")
                    continue
                if ingreso == 1:
                    for series in series_vistas:
                        print(f"- {series['nombre']} ({series['genero']}) ⭐ {series['calificacion']}")
                elif ingreso == 2:
                    for series in ver_mas_tarde:
                        print(f"- {series['nombre']} ({series['genero']})")
                else:
                    print("error invalido ")
            except ValueError:
                print("error entrada ingrese una opccion entre 1 y 2")


    def Series_pendientes():
        while True:
            print("ingrese el nombre y genero para guardar la serie para ver despues")

            nombre = input("ingrese el nombre de la serie que se guardara en ver mas tarde").strip()

            if not nombre:
                print("error invalido no puede ser vacio el campo")
                continue

            genero = input("ingrese el genero de la serie").strip()

            if not genero:
                print("error invalido no puede ser vacio el campo")
                continue

            if any(serie["nombre"].lower() == nombre.lower() for serie in ver_mas_tarde):
                print("esta serie ya esta guardada en ver mas tarde")
                continue

            ver_mas_tarde.append({"nombre": nombre, "genero": genero})
            print(f"✅ Serie '{nombre}' guardada correctamente en 'ver más tarde'.")
            break


    def Lista_de_series_pendientes():
        if not ver_mas_tarde:
            print("no tienes seires guardadas en ver mas tarde")
        else:
            print("series pendientes guardadas")
            for i, serie in enumerate(ver_mas_tarde, start=1):
                print(f"{i}. {serie['nombre']} - 🎭 Género: {serie['genero']}")


    def Eliminar_series():
        while True:

            print("\n--- Eliminar Series ---")
            print("1. Eliminar de series vistas")
            print("2. Eliminar de series pendientes por ver")
            print("3. Regresar al menú")

            print("ingrese primero una opccion de donde se encuatra la serie que desea eliminar 1 en series vistas y 2 en pendientes por ver 3 para regresar")
            try:
                opcciones = int(input("ingrese una opccion 1 2 o 3"))
            except ValueError:
                print("error entrada ingrese una opccion entre 1 2 y 3")
                continue
            if opcciones == 1:
                nombre = input("ingrese el nombre de la serie que desea eliminar").strip()
                if not nombre:
                    print("error invalido no puede ser vacio el campo")
                    continue
                encontrada = False  # asumimos que no está

                for serie in series_vistas:
                    if serie["nombre"].lower() == nombre.lower():
                        series_vistas.remove(serie)
                        print(f"La serie {nombre} fue eliminada correctamente.")
                        encontrada = True  # ya la encontramos
                        break

                if not encontrada:  # sigue en False
                    print("La serie no se encuentra en series vistas.")

            elif opcciones == 2:
                nombre = input("ingrese el nombre de la serie que desea eliminar").strip()
                if not nombre:
                    print("error invalido no puede ser vacio el campo")
                    continue
                encontrada = False  # asumimos que no está

                for serie in ver_mas_tarde:
                    if serie["nombre"].lower() == nombre.lower():
                        ver_mas_tarde.remove(serie)
                        print(f"La serie {nombre} fue eliminada correctamente.")
                        encontrada = True  # ya la encontramos
                        break

                if not encontrada:  # sigue en False
                    print("La serie no se encuentra en series vistas.")
            elif opcciones == 3:
                print("saliendo....")
                break


    def funcion(num , num1):
        suma = num + num1


    def funcion1(a,b):
        c = a + b
        return















