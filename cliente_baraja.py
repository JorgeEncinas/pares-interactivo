#!/usr/bin/python3
# Integrantes del equipo:
#   Alcaraz Biebrich Manuel Alejandro
#   Encinas Alegre Jorge Carlos
#   Romero Andrade Paula Cristina
# Fecha: 5 de Abril de 2020
#  
#   ./cliente_baraja.py -j nombre_jugador -d 127.0.0.1 -p 9000
#   -j --jugador    Nombre del jugador
#   -d --direccion  Es la dirección IP del servidor.
#   -p --puerto     Puerto donde se dará la comunicación. 
#   (NOTA: Redirigir el puerto en el Firewall del módem a la dirección
#   que tendrá servidor_baraja.py ejecutándose)

#Debe mostrar un menú

import pares
import tarjetas
import xmlrpc.client
import argparse
#Métodos útiles de pares.py:
#   comparar_manos( jugadores, dict_cartas ): Regresa ganador, dict_ganador
#   motivo_victoria( dt ): regresa el motivo por el que ganó

def menu():
    print("1. Pedir Mano")              #El servidor asigna una mano aleatoria al jugador, quitándolas de la baraja. devuelve la mano. Se imprime el nombre del cliente, rayitas, y luego la mano ordenada de menor a mayor
    print("2. Mostrar jugadores")       #El servidor devuelve una lista con los nombres de los jugadores. Cuántos son y luego numerados los nombres
    print("3. Mostrar manos de todos")  #El servidor devuelve un diccionario con los jugadores y sus manos. El cliente muestra cada uno como el 1 los imprime. Devolver el ganador para que el servidor guarde en su diccionario cuántos juegos ha ganado cada jugador. Sólo cuentan los pares y los tríos de cartas
    print("4. Volver a Jugar")          #Se conecta al servidor y se reinicia la baraja. Se limpian las manos
    print("5. Mostrar Marcador")        #El cliente pide al servidor el diccionario de marcador. Al recibirlo, lo muestra, así como la cantidad de juegos jugados.
    print("0. Salir")                   #El cliente se desconecta del servidor y sale.
    print("")
    return safe_int("Escriba el número de la opción que desee y presione Enter \n", 5)


def safe_int( mensaje, opcion_max ):
    ''' Método para recibir una respuesta de varias, mandas el mensaje y las opciones máximas, evitando errores.'''
    while True:
        respuesta = -1
        while respuesta < 0 or respuesta > opcion_max:
            try:
                respuesta = int(input(mensaje))
            except ValueError:
                print("Eso no es un número")
        return respuesta

def mostrar_jugadores( proxy ):
    print("")
    players = proxy.mostrar_jugadores()
    if len(players) > 0:
        print("Jugadores: {}".format(len(players)))
        for i, player in enumerate(players):
            print("Jugador {}: {}".format(i+1, player))
    else:
        print("No hay jugadores aún.")
    print("")

def mostrar_manos( proxy ):
    print("")
    jugadores=proxy.mostrar_manos()
    ganador, dict_ganador = pares.comparar_manos( jugadores )
    if ganador is None:
        print("Empate")
    else:
        print("El ganador es {}!".format(ganador))
        print(pares.motivoVictoria(dict_ganador))
    if ganador is not None:
        proxy.guardar_marcador( ganador )
    print("")

def reset( proxy ):
    proxy.sreset()

def main( jugador, direccion, puerto ):
    print("Iniciamos! \n")
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000', allow_none=True)
    proxy.guardar_nuevo( jugador )
    ya_pidio = False
    try:
        opcion = 99
        while opcion != 0:
            opcion = menu()
            if opcion == 0: #Salir
                break
            if opcion == 1: #Pedir Mano
                print("")
                mi_mano = proxy.hmano( jugador )
                pares.mostrar_mano(jugador, mi_mano)
                ya_pidio = True
            if opcion == 2: #Mostrar Jugadores
                mostrar_jugadores( proxy )
            if opcion == 3: #Mostrar manos de todos
                if ya_pidio == True:
                    mostrar_manos(proxy)
                    ya_pidio = False
                else:
                    print(" \n No has pedido mano. \n ")
            if opcion == 4: #Volver a jugar
                reset( proxy )
                print("Se han revuelto las cartas.")
            if opcion == 5: #Mostrar Marcador
                marcador=proxy.mostrar_marcador()
                items=marcador.items()
                print("HIGH-SCORE")
                print("------------------")
                if len(jugador) > 0:    
                    for jugador in items:
                        print(jugador[0],": ",jugador[1],"pts")
                print("")
        print("Saliendo")

    except ConnectionError:
        print("Se desconecto el Server")
    except KeyboardInterrupt:
        print("Usuario cancela programa")

#   (NOTA: Redirigir el puerto en el Firewall del módem a la dirección
#   que tendrá servidor_baraja.py ejecutándose)
if __name__ == "__main__":
    parse =argparse.ArgumentParser()
    parse.add_argument("-j","--jugador",dest="jugador",required=False,default="El-Cacas")
    parse.add_argument("-d", "--direccion", dest="direccion", required=False, default="0.0.0.0")
    parse.add_argument("-p", "--puerto", dest="puerto", required=False, type=int, default=9000)
    args = parse.parse_args()
    jugador = args.jugador
    direccion = args.direccion
    puerto = args.puerto
    main( jugador, direccion, puerto )