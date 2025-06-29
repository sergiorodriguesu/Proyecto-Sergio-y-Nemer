from abc import ABC, abstractmethod

class Casilla(ABC): #Clase abstracta con los metodos y atributos que deben de tener las 2 clases hijas 
    def __init__(self, visibilidad, marca ):
        self.visibilidad = visibilidad
        self.marca = marca
        
    def revelar(self):
        if self.visibilidad == False:
            self.visibilidad = True
    
    def marcar(self):
        while True:  #Bucle que repite la acción hasta que el usuario marque una opción válida
            try:
                opcion = int(input(" Selecciona la marca a poner: \n1 Bandera\n2 Interrogante\n"))
            except ValueError:
                print("Por favor, ingrese una opción válida.")
            if opcion == 1:
                self.marca = "🏳️"
                break
            elif opcion == 2:
                self.marca = " ? "
                break
            else:
                print("\n\n**********Ingrese una opcion valida**********\n\n")



class Vacia(Casilla):
    def __init__(self, visibilidad, marca):
        super().__init__(visibilidad, marca)


    def minas_alrededor(self, matriz, fila, columna):
        minas_adyacentes = 0
        filas = len(matriz)
        columnas = len(matriz[0])
        for i in range(fila - 1, fila + 2):
            for j in range(columna - 1, columna + 2):
                if (0 <= i < filas) and (0 <= j < columnas) and not (i == fila and j == columna): #Condición que primero evita salirse del rango de la matriz y luego evita que se cuente a si misma
                    obj = list(matriz[i][j].values())[0]   #Obtiene el objeto que se encuentra en las coordenadas de la matriz y lo convierte en una lista para poder acceder facilmente al objeto
                    if isinstance(obj, Mina):    #Si el objeto es una mina se sumará 1 a la variable minas_adyacentes
                        minas_adyacentes += 1
        return minas_adyacentes
            
class Mina(Casilla):
    def __init__(self, visibilidad, marca,):
        super().__init__(visibilidad, marca)


    
        
