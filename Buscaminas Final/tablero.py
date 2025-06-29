import requests
import random
from casillas import Vacia, Mina

configuracion0 = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/config.json")
if configuracion0.status_code == 200:
    configuracion = configuracion0.json()
    print("configuracion obtenida correctamente.")


class Tablero():
    def __init__(self, cantidad_minas, cantidad_de_vacias, tamaño): #Tiene de atributos la cantidad de casillas vacias y de minas para acceder a estos datos facilmente posteriormente, como el tamaño para poder crear la matriz
        self.cantidad_minas = cantidad_minas
        self.cantidad_de_vacias = cantidad_de_vacias
        self.tamaño = tamaño


    def matriz0(self):  #Crea una matriz 8 x 8 según la configuración de la API con objetos de casillas vacias
        matriz = []
        for i in range(self.tamaño[0]):
            fila = []
            for j in range(self.tamaño[1]):
                fila.append({(i, j): Vacia(False, None)}) #Los objetos de la lista son diccionarios que contienen de key las coordenadas y de value la casilla para su facil llamado
            matriz.append(fila)
        return matriz

    def minas(self):  #Función que crea una lista de objetos tipo mina segun la cantidad de minas que hay que se obtiene mediante la seleccion de la dificultad
        minas = []
        for i in range(self.cantidad_minas):
            mina = Mina(False, None)
            minas.append(mina)
        return minas

    def indices_minas(self):   #Función que genera indices aleatorios e irrepetibles para las minas en forma de lista, con el fin de posteriormente ingresarlas a la matriz
        indices = []
        for i in range(self.cantidad_minas):
            fila = random.randint(0, self.tamaño[0] - 1)
            columna = random.randint(0, self.tamaño[1] - 1)
            if (fila, columna) not in indices:  #Condición que evita que dos minas tengan el mismo índice
                indices.append((fila, columna))
            else:
                while (fila, columna) in indices:   #Repite esta condición hasta que se consiga un índice único para la mina
                    fila = random.randint(0, self.tamaño[0] - 1)
                    columna = random.randint(0, self.tamaño[1] - 1)
                indices.append((fila, columna))
        return indices

    def matriz1(self):  #Función que crea la matriz del tablero con las minas ya colocadas a través del uso de las anteriores funciones
        matriz = self.matriz0()
        minas = self.minas()
        indices = self.indices_minas()

        for i, (fila, columna) in enumerate(indices): # Reemplaza el diccionario de vacía por uno de mina en la posición correspondiente
            matriz[fila][columna] = {(fila, columna): minas[i]}
        return matriz
    






