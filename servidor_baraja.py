#!/usr/bin/python3
# Integrantes del equipo:
#   Alcaraz Biebrich Manuel Alejandro
#   Encinas Alegre Jorge Carlos
#   Romero Andrade Paula Cristina
# Fecha: 5 de Abril de 2020
#  
#   ./servidor_baraja.py -d 127.0.0.1 -p 9000 -m 5
#   -d --direccion  Es la dirección IP que escuchará. Default: 0.0.0.0 
#   -p --puerto     Puerto donde se dará la comunicación. 
#   (NOTA: Redirigir el puerto en el Firewall del módem a la dirección
#   que tendrá servidor_baraja.py ejecutándose)
#   -m --mano       Indica el número de cartas a repartir en la mano.
#   (NOTA: ¡Filtro que no pase de 52 cartas!)

import tarjetas
from xmlrpc.server import SimpleXMLRPCServer
import logging
import random
import pares

class Juego: #adaptar esto para que sea la baraja.
    baraja = None
    numero_cartas = None
    en_proceso = False
    marcador = None
    dict_jugadores = None
    #baraja.lista_jugadores = [("nombre_j1", [C1, C2, C3, C4, C5]), ("nombre_j2", [C1, C2, C3, C4, C5])]

    def __init__(self):
        self.baraja = tarjetas.Baraja()
        self.numero_cartas = 0
        self.marcador = dict()
        self.dict_jugadores = dict()

    def mano(self, jugador, numero):
        if numero_cartas > 0:
            print("Alguien ha definido ya un número de cartas: {}".format(numero_cartas))
        else: #numero_cartas == 0:
            self.numero_cartas = max_cap( numero, len(baraja.dict_jugadores))
        mano_jugador = baraja.genera_mano( numero_cartas )
        guarda_jugador( jugador, mano_jugador )
        return mano_jugador
    
    def guarda_jugador( self, jugador, mano_jugador ):
        self.dict_jugadores[jugador] = mano_jugador
            
    def max_cap( self, num_cartas, jugadores ):
        if len(jugadores) > 0:
            if num_cartas > math.floor(52/(len(jugadores))):
                print("Se ha seleccionado un número de cartas para las cuales \n \
                no se puede repartir la mano equitativamente. \n \
                Se reducirá la cantidad de cartas al número máximo posible.")
                num_cartas = math.floor(52/(len(jugadores)))
        else:
            if num_cartas > 26:
                print("Con ese número de cartas no es posible jugar siquiera de dos jugadores. \n \
                Se reducirá el número a 26.")
                num_cartas = 26
        if num_cartas < 1:
            print("Con ese número de cartas no es posible jugar. \n \
            Se le asignarán 5 cartas a su mano")
            num_cartas = 5
    return num_cartas 

    def get_jugadores():
        return [key for key in dict_jugadores.keys()] # Maybe .keys() not necessary

#El servidor asigna una mano aleatoria al jugador, quitándolas de la baraja.
#Devuelve la mano.
#Se imprime el nombre del cliente, rayitas, y luego la mano ordenada de menor a mayor
def mano( jugador ):
    return j.mano( jugador, j.numero_cartas )

def guardar_marcador( ganador ):
    if ganador in j.marcador:
        marcador[ganador] = 1
    else:
        marcador[ganador] += 1

def mostrar_jugadores():
    return j.get_jugadores()

def mostrar_manos():
    #debe regresar un diccionario con los jugadores y sus manos.
    return j.dict_jugadores

def mostrar_mano():
    #ni idea xd supongo que mostrar la mano de un jugador pero sabe pq aquí xd
    return 1

def mostrar_marcador():
    return j.marcador

def main( direccion, puerto, manox ):
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)

    server = SimpleXMLRPCServer(
    (direccion, puerto),
    logRequests=True,
    )
    j = Juego()
    j.numero_cartas = max_cap( manox, "" )
    server.register_function(mano)
    server.register_function(mostrar_jugadores)
    server.register_function(mostrar_mano)
    server.register_function(mostrar_manos)
    server.register_function(mostrar_marcador)
    # Start the server
    try:
        print('Usa Control-C para salir')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')

if __name__ == "__main__":
    parse =argparse.ArgumentParser()
    parse.add_argument("-d","--direccion", dest="direccion", required=False, default="0.0.0.0")
    parse.add_argument("-p","--puerto", dest="puerto", required=False, type=int, default=9000)
    parse.add_argument("-m", "--mano", dest="mano", required=False, type=int, default=5)
    args = parse.parse_args()
    direccion = args.direccion
    puerto = args.puerto
    mano = args.mano
    main( direccion, puerto, mano )

