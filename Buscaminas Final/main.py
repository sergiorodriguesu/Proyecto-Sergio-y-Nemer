import requests
import time
import os
from casillas import Vacia, Mina
from Jugador import Jugador
from tablero import Tablero

configuracion0 = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/config.json")
if configuracion0.status_code == 200: #Convierte la configuración de la API en una variable solo si se obtubo correctamente
    configuracion = configuracion0.json()
    print("configuracion obtenida correctamente.")

def dificultad_valor(dificultad):  #Función que devuelve el órden de las dificultades para ordenar los records
    orden = {"-": 1, "easy": 2, "medium": 3, "hard": 3, "impossible": 4}
    return orden.get(dificultad, 99)

def cargar_records_local(filename="records.txt"):  #Función que guarda los records guardados en el archivo llamado records.txt en una variable en forma de lista para poder mostrarlo más fácilmente
    records = []
    if os.path.exists(filename):  #Solamente realiza la acción si este archivo existe para evitar errores
        with open(filename, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split()
                if len(partes) == 4:
                    nombre, apellido, tiempo, dificultad = partes
                    records.append({
                        "first_name": nombre,
                        "last_name": apellido,
                        "time": float(tiempo),
                        "difficulty": dificultad
                    })
    return records

def guardar_records_txt(records, filename="records.txt"): #Función que guarda en el archivo records.txt los records  
    records_ordenados = sorted(records, key=lambda r: (dificultad_valor(r["difficulty"]), r["time"])) #Ordena los records primero en base a la dificultad y luego en base al tiempo
    with open(filename, "w", encoding="utf-8") as f:
        for record in records_ordenados:
            linea = f"{record['first_name']} {record['last_name']} {record['time']} {record['difficulty']}\n"
            f.write(linea)

records = cargar_records_local() #Función que verifica primero si hay un archivo ya en el sistema que tiene los records, en dado caso de que no, se obtienen los records de la API y se crea un nuevo archivo records.txt donde los guarda
if not records:
    records0 = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/leaderboard.json")
    if records0.status_code == 200:
        records = records0.json()
        for record in records:
            if "difficulty" not in record:
                record["difficulty"] = "-"
        guardar_records_txt(records)  # Guarda los records descargados para futuras sesiones
        print("Records obtenidos correctamente.")

def actualizar_records(usuario, tiempo, dificultad, records, filename="records.txt"):
    nuevo_record = {
        "first_name": usuario.nombre,
        "last_name": usuario.apellido,
        "time": tiempo,
        "difficulty": dificultad
    }
    # Si hay menos de 3 records, simplemente agrega el nuevo
    if len(records) < 3:
        records.append(nuevo_record)
    else:
        # Ordena los records actuales
        records_ordenados = sorted(records, key=lambda r: (dificultad_valor(r["difficulty"]), r["time"]))
        peor = records_ordenados[-1]
        # Si el nuevo record es mejor que el peor, lo reemplaza
        if (dificultad_valor(dificultad), tiempo) > (dificultad_valor(peor["difficulty"]), peor["time"]):
            records.remove(peor)
            records.append(nuevo_record)
    # Guarda los 3 mejores records ordenados
    guardar_records_txt(sorted(records, key=lambda r: (dificultad_valor(r["difficulty"]), r["time"]))[:3], filename)

def usuario(): #Función que obtiene los datos del usuario y los guarda creando el objeto del jugador
    while True:  #Valida que se ingrese un valor real para evitar errores
        nombre = input("Ingrese su nombre: ")
        apellido = input("Ingrese su apellido: ")
        if nombre and apellido:
            start = time.time()
            return Jugador(nombre, apellido, start)
        else:
            print("Por favor, ingrese un nombre y un apellido válidos.")

def seleccion_dificultad(): #Función que define la dificultad y retorna la cantidad de minas para la dificultad seleccionada
    while True:   #Valida que se ingrese un valor real para evitar errores
        dificultad = input("Seleccione la dificultad:\n1. Facil\n2. Intermedio\n3. Dificil\n4. Imposible\n")
        if dificultad == "1":
            rattio = configuracion["global"]["quantity_of_mines"]["easy"]
            quantity_of_mines = (rattio * 64)
            return quantity_of_mines
        elif dificultad == "2":
            rattio = configuracion["global"]["quantity_of_mines"]["medium"]
            quantity_of_mines = (rattio * 64) 
            return quantity_of_mines
        elif dificultad == "3":
            rattio = configuracion["global"]["quantity_of_mines"]["hard"]
            quantity_of_mines = (rattio * 64) 
            return quantity_of_mines
        elif dificultad == "4":
            rattio = configuracion["global"]["quantity_of_mines"]["impossible"]
            quantity_of_mines = (rattio * 64)
            return quantity_of_mines
        else:
            print("Opción no válida. Intente de nuevo.")

def crear_tablero(minas, vacias, tamaño = configuracion["global"]["board_size"]):  #Función que crea el tablero al ingresarle el valor de la cantiddad de minas y de casillas vacias y retorna la matriz finalizada
    tablero = Tablero(minas, vacias, tamaño)
    matriz = tablero.matriz1()
    return matriz

def matriz_interfaz(tablero):  #Función que lee la matriz y devuelve una interfaz user-friendly para que el usuario observe sin ver que hay detrás
    vacias = 0
    print("        0     1     2     3     4     5     6     7 \n")  #índices de las columnas
    for i,fila in enumerate(tablero):
        linea = ""
        indice = f" {i}"  #Índice de cada fila
        for j, celda in enumerate(fila):
            obj = list(celda.values())[0]
            if hasattr(obj, "visibilidad") and obj.visibilidad is False:
                if hasattr(obj, "marca") and obj.marca == "🏳️":
                    linea += "  🏳️   "
                elif hasattr(obj, "marca") and obj.marca == " ? ":
                    linea += "   ?  "
                elif hasattr(obj, "marca") and obj.marca is None:
                    linea += "  ⬜  "
            if hasattr(obj, "visibilidad") and obj.visibilidad is True: #Prioriza la muestra de la visibilidad antes que de la marca
                if isinstance(obj, Mina):
                    linea += "  💣  "
                elif isinstance(obj, Vacia):  #Si la casilla esta revelada y es vacía muestra en pantalla cuantas minas tiene en su 3x3
                    minas_alrededor = obj.minas_alrededor(tablero, i, j)
                    linea += f"   {minas_alrededor}  "
                    vacias += 1    #Cuenta la cantidad de casillas vacias reveladas 
        print(f"\n{indice}   {linea}") #Imprime cada fila individual
    return vacias   #Devuelve como parametro la cantidad de casillas vacías reveladas para poder usar después como condición para ganar el juego al compararlo con la cantidad de casillas vacías que hay en el tablero

def revelar_cascada(tablero, fila, columna):  #Función que revela las casillas de alrededor de una casilla vacía que tiene 0 minas alrededor de forma recursiva
    filas = len(tablero)
    columnas = len(tablero[0])
    for i in range(fila - 1, fila + 2):
        for j in range(columna - 1, columna + 2):
            if (0 <= i < filas) and (0 <= j < columnas):  #Condición que evita que se salga del rango de la matriz
                obj = list(tablero[i][j].values())[0]
                if isinstance(obj, Vacia) and not obj.visibilidad:  #Verifica que la casilla no este ya revelada
                    obj.revelar()
                    minas_alrededor = obj.minas_alrededor(tablero, i, j)
                    if minas_alrededor == 0: #Si la casilla que se revelo también tiene alrededor 0 minas revela las casillas de alrededor
                        revelar_cascada(tablero, i, j) #Se vuelve a ejecutar la función con todos los valores i,j de casillas vacias alrededor de la original

def juego(tablero): #Función con todas las opciones para jugar en el tablero usando las funciones anteriores
    while True:  #Se repite todo el codigo hasta que se gane o pierda
        try:
            opcion0 = int(input("\nElija la acción: \n1 Revelar casilla \n2 Colocar una marca\n"))  #Primero se elije si se revela una casilla o si se va a marcar una casilla
        except ValueError:
            print("\n\n**********Por favor, ingrese un número válido**********\n\n")
            continue

        if opcion0 == 1:  #Función para revelar la casilla
            while True:
                try:
                    opcion1 = int(input("Coloque las coordenadas de la fila de la casilla que quiere seleccionar: \n"))
                    opcion2 = int(input("Coloque las coordenadas de la columna de la casilla que quiere seleccionar: \n"))
                    break
                except ValueError:
                    print("Por favor, ingrese números válidos para las coordenadas.")
            if opcion1 not in range(len(tablero)) or opcion2 not in range(len(tablero)):
                print("\n\n ****************************INGRESE UNA COORDENADA VÁLIDA****************************\n\n")
                matriz_interfaz(tablero)  #Vuelve a colocar la interfáz del buscaminas para poder visualizar bien las casillas y sus coordenadas
            else: 
                casilla = list(tablero[opcion1][opcion2].values())[0]
                casilla.revelar() #Revela la casilla
                if isinstance(casilla, Vacia):
                    minas_alrededor = casilla.minas_alrededor(tablero, opcion1, opcion2)
                    if minas_alrededor == 0: #Si la casilla revelada es vacía y además tiene 0 minas alrededor ejecuta el revelar en cascada para revelar las demás de alrededor
                        revelar_cascada(tablero, opcion1, opcion2)
                return casilla #Devulve cual es la casilla que se reveló, y en posteriormente verificar que si es una mina se perdió el juego
        elif opcion0 == 2:
            while True:
                try:
                    opcion1 = int(input("Coloque las coordenadas de la fila de la casilla que quiere seleccionar: \n"))
                    opcion2 = int(input("Coloque las coordenadas de la columna de la casilla que quiere seleccionar: \n"))
                    break
                except ValueError:
                    print("Por favor, ingrese números válidos para las coordenadas.")
            if opcion1 not in range(len(tablero)) or opcion2 not in range(len(tablero)):
                print("\n\n ****************************INGRESE UNA COORDENADA VÁLIDA****************************\n\n")
                matriz_interfaz(tablero)
            else:
                casilla = list(tablero[opcion1][opcion2].values())[0]
                casilla.marcar()   #Llama a la funcion marcar que pedira el tipo de marca y actualizara el atributo para que pueda ser mostrado después por mostrar_interfaz
                matriz_interfaz(tablero)


                
            
        
def partida(tablero, vacias):  #Función que indica cuando se gana la partida y cuando se pierde
    while True:
                blanks = matriz_interfaz(tablero)
                if blanks == vacias:
                    print("\n\n\n!!!!!!!!!!!!!!!HAS GANADO EL JUEGO!!!!!!!!!!!!!!!!!!!!\n\n\n")
                    return True
                else:
                    casilla = juego(tablero)
                    if isinstance(casilla, Mina) == True:
                        matriz_interfaz(tablero)
                        print("!!!!!La casilla era una mina, has perdido!!!!!")
                        return False 
                    else:
                        continue


def main():
    print("-------------------------------------------------\n-------------BIENVENIDO A BUSCAMINAS-------------\n-------------------------------------------------")
    usuario0 = usuario()
    while True:  #Permíte que el juego funcione hasta que se gane o se pierda
        opcion1 = input("Que desea hacer?\n1 Jugar una partida\n2 Ver los records\n3 Salir\n")
        if opcion1 == "1":
            minas = int(seleccion_dificultad())
            vacias = 64 - minas
            tablero = crear_tablero(minas, vacias)
            print(f"Minas en el tablero: {minas}")
            print("Las filas (cada linea horizontal) van del 0 al 7 al igual que las columnas(cada linea vertical), Ejemplo: La mina de abajo a la derecha es la 7:7")  #Guía para que el jugador entienda que es una fila y que es una columna y como funcionan las coordenadas
            usuario0.tiempo = time.time()  #Genera el tiempo en el que se inicio la partida
            ganador = partida(tablero, vacias)
            if ganador == True:  #Si se gano la partida
                usuario0.tiempo = time.time() - usuario0.tiempo #Resta el tiempo final con el incial en s para guardarlo en el atributo del usuario
                print(f"Tu tiempo fue de {usuario0.tiempo} segundos")
                dificultad_str = ""
                if minas == int(configuracion["global"]["quantity_of_mines"]["easy"] * 64):
                    dificultad_str = "easy"
                elif minas == int(configuracion["global"]["quantity_of_mines"]["medium"] * 64):
                    dificultad_str = "medium"
                elif minas == int(configuracion["global"]["quantity_of_mines"]["hard"] * 64):
                    dificultad_str = "hard"
                elif minas == int(configuracion["global"]["quantity_of_mines"]["impossible"] * 64):
                    dificultad_str = "impossible"
                actualizar_records(usuario0, usuario0.tiempo, dificultad_str, records)
                # Recarga records para mostrar los nuevos si el usuario elige verlos
                records[:] = cargar_records_local()
        elif opcion1 == "2": #imprime los records 
            print(f"Los records son: \n1 {records[0]["first_name"]} {records[0]["last_name"]} con un tiempo de {records[0]["time"]}s en la dificultad {records[0]["difficulty"]} \n2 {records[1]["first_name"]} {records[1]["last_name"]} con un tiempo de {records[1]["time"]}s  en la dificultad {records[1]["difficulty"]}\n3 {records[2]["first_name"]} {records[2]["last_name"]} con un tiempo de {records[2]["time"]}s  en la dificultad {records[2]["difficulty"]}\n")
        elif opcion1 == "3":
            break
        else:
            print("\n\n\n****************************INGRESE UNA OPCIÓN VÁLIDA****************************\n\n\n")
    
main()
