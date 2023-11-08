def leer_fichero(fichero):
	


	#lectura de fichero
	with open(fichero, 'r') as file:
		
		lista=[]

		for linea in file:

			#remueve los saltos de linea en cada linea leida.
			linea = linea.strip('\n')
			cadena = linea
			#print(cadena)
			linea = cadena.split(";")
			#separa los espacios
			#print(linea)
			#agrega la lista a la lista.
			lista.append(linea)

			

		#retorna la lista de listas.
		print(len(lista), "largo de la lista")

		return lista
"""
def obtener_largo(fichero):

	print("fichero", fichero)
	print("entra la funcion obtener largo")
    contador = 0

    with open(fichero, 'r') as file:

        for linea in file:

            for caracter in linea:

                if caracter == '\n' and linea != '\n':

                    contador = contador + 1
    
    return contador 
"""