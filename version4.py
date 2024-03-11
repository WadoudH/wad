#PROGRAMA PARA TESTEAR EL PUERTO SERIE CON UN PIC

##################################################Importaciones necesarias##################################################
import tkinter as tk
import serial
from tkinter import ttk
from tkinter import *
from serial.tools import list_ports

################################################## Fin de importaciones ##################################################

################################################## Funciones ##################################################

def obtener_puertos_com():
    """
    Obtiene una lista de los puertos COM disponibles en el sistema.

    Returns:
        list: Una lista de cadenas que representan los puertos COM disponibles.
    """
    puertos_com = [port.device for port in list_ports.comports()]
    return puertos_com

def mostrar_puertos_com():
    """
    Muestra los puertos COM disponibles en un combo box.

    Esta función actualiza los valores del combo box 'combo_puertos' con los puertos COM disponibles.
    También establece el valor seleccionado en el combo box como vacío.

    Parámetros:
        Ninguno

    Retorna:
        Ninguno
    """
    combo_puertos['values'] = obtener_puertos_com()
    combo_puertos.set("")

def conectar_puerto(puerto):
    """
    Conecta al puerto especificado y devuelve el objeto de conexión.

    Args:
        puerto (str): El nombre o número del puerto al que se desea conectar.

    Returns:
        serial.Serial or None: El objeto de conexión serial si la conexión es exitosa, None en caso de error.

    Raises:
        serial.SerialException: Si ocurre un error al intentar establecer la conexión.

    """
    try:
        conectar = serial.Serial(puerto, baudrate=9600, stopbits=1, parity='N', bytesize=8)
        return conectar
    except serial.SerialException as e:
        return None

def desconectar_puerto(conectar):
    """
    Desconecta el puerto de conexión.

    Parámetros:
    conectar (objeto): El objeto de conexión que se desea cerrar.

    """
    if conectar:
        conectar.close()

def conectar_o_desconectar():
    """
    Esta función se utiliza para conectar o desconectar un puerto.
    Si el puerto está conectado, se desconectará. Si el puerto está desconectado, se conectará.
    """
    global conectar
    if conectar is None:
        puerto_seleccionado = combo_puertos.get()
        conectar  = conectar_puerto(puerto_seleccionado)
        if conectar:
            btn_conectar.config(text="Desconectar")
    else:
        desconectar_puerto(conectar)
        conectar = None
        btn_conectar.config(text='Conectar')

def datos_start():
    """
    Esta función se utiliza para enviar datos por el puerto serie.
    """
    if conectar:                                                                                                                        # Si el puerto está conectado,
        if datavaris.get() != "":                                                                                                       # Si la entrada de datos no está vacía, 
            inicio_header = ["0a", "0A"]                                                                                                # Encabezado de la trama.
            if datavaris.get()[0:2] not in inicio_header:                                                                               # Si el primer byte no es 0x0A, entonces
                #print("Error: El primer byte no es correcto")                                                                           # Mostramos un mensaje de error.
                cuadro_texto.delete(1.0, tk.END)                                                                                        # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
            else:                                                                                                                       # Si el primer byte es 0x0A, entonces
                fin_header = ["a0", "A0"]                                                                                               # Fin de la trama.
                if datavaris.get()[2:4] not in fin_header:                                                                              # Si el segundo byte no es 0xA0, entonces
                    #print("Error: El segundo byte no es correcto")                                                                      # Mostramos un mensaje de error.
                    cuadro_texto.delete(1.0, tk.END)                                                                                    # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                else:                                                                                                                   # Si el segundo byte es 0xA0, entonces
                    if ((len(datavaris.get())/2) != int(datavaris.get()[4:6], 16) + 4):                                                 # Si la longitud del mensaje es diferente a la cantidad esperada + 4, entonces
                        #print(int(datavaris.get()[4:6],16))                                                                             # Mostramos la cantidad esperada.    
                        #print("Mensaje entrante: ", datavaris.get())                                                                    # Mostramos el mensaje entrante.
                        #print("cantidad esperada: ", int(datavaris.get()[4:6], 16) + 8)                                                 # Mostramos la cantidad esperada.
                        #print("longitud del mensaje: ", len(datavaris.get()))                                                           # Mostramos la longitud del mensaje.
                        #print("Error: La longitud del mensaje es diferente!!")                                                          # Mostramos un mensaje de error.
                        cuadro_texto.delete(1.0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                    else:                                                                                                               # Si la longitud del mensaje es igual a la cantidad esperada + 4, entonces
                        tipos_aceptados = ["0b", "0B"]                                                                                  # Tipos de datos aceptados.
                        if datavaris.get()[6:8] not in tipos_aceptados:                                                                 # Si el tipo de dato no es 0x0B, entonces
                            print("Error: El tipo de dato no es acceptado")                                                             # Mostramos un mensaje de error.
                            cuadro_texto.delete(1.0, tk.END)                                                                            # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        else:                                                                                                           # Si el tipo de dato es 0x0B, entonces
                            conectar.write(bytearray.fromhex(datavaris.get()))                                                          # Enviamos el mensaje por el puerto serie.
                            print(f"Mensaje enviado: {datavaris.get()}")                                                                # Mostramos el mensaje enviado.
                            cuadro_texto.delete(1.0, tk.END)                                                                            # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.

def recibir_datos():
    """
    Esta función se utiliza para recibir datos por el puerto serie.
    """
    cuadro_texto.delete(1.0, tk.END)                                                                                                    # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.                
    if conectar:                                                                                                                        # Si el puerto está conectado, entonces
        #time.sleep(0.5)
        if conectar.in_waiting:                                                                                                         # Si hay datos en el puerto serie, entonces
            datos = bytearray()                                                                                                         # Creamos un objeto de tipo bytearray para almacenar los datos recibidos por el puerto serie.
            trama = Trama(0, 0, 0, 0, [])                                                                                               # Creamos un objeto de tipo Trama para almacenar la trama recibida por el puerto serie que sera el mensaje final.
            while conectar.in_waiting:                                                                                                  # Mientras haya datos en el puerto serie, entonces
                byte = conectar.read(1)                                                                                                 # Leemos un byte del puerto serie.
                datos.append(byte[0])                                                                                                   # Añadimos el byte leído al objeto de tipo bytearray.
                cuadro_texto.delete(1.0, tk.END)                                                                                       # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                cuadro_texto.insert(tk.END, datos.hex())                                                                                # Mostramos los datos recibidos por el puerto serie en el cuadro de texto.
                if len(datos) == 1:                                                                                                     # Si la longitud de los datos es igual a 1, entonces
                    if datos[0] != 0x0A:                                                                                                # Verificamos si el primer byte no es 0x0A. Si no es 0x0A, entonces
                        #print("Error: El primer byte no es 0A")                                                                         # Mostramos un mensaje de error.
                        cuadro_texto.delete(1.0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        break                                                                                                           # Salimos del bucle.
                    else:                                                                                                               # Si el primer byte es 0x0A, entonces
                        trama.entrada(datos[0], 0, 0, 0, [])                                                                            # Añadimos el primer byte al objeto de tipo Trama.
                elif len(datos) == 2:                                                                                                   # Si la longitud de los datos es igual a 2, entonces
                    if datos[1] != 0xA0:                                                                                                # Verificamos si el segundo byte no es 0xA0. Si no es 0xA0, entonces
                        #print("Error: El segundo byte no es A0")                                                                        # Mostramos un mensaje de error.
                        cuadro_texto.delete(1.0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        break                                                                                                           # Salimos del bucle.
                    else:                                                                                                               # Si el segundo byte es 0xA0, entonces
                        trama.entrada(trama.inicio, datos[1], 0, 0, [])                                                                 # Añadimos el segundo byte al objeto de tipo Trama.
                elif len(datos) == 3:                                                                                                   # Si la longitud de los datos es igual a 3, entonces
                    #añadir el contro de datos esperados        
                    cantidad_esperada = datos[2]                                                                                        # Guardamos la cantidad de datos esperados.
                    trama.entrada(trama.inicio, trama.fin, cantidad_esperada, 0, [])                                                    # Añadimos la cantidad de datos esperados al objeto de tipo Trama.
                    #print(f"La longitud de la trama esperada del mensaje entrante es de {cantidad_esperada} bytes")                     # Mostramos la cantidad de datos esperados.
                elif len(datos) == 4:                                                                                                   # Si la longitud de los datos es igual a 4, entonces
                    tipo_dato = datos[3]                                                                                                # Guardamos el tipo de dato.
                    trama.entrada(trama.inicio, trama.fin, trama.cantidad, tipo_dato, [])                                               # Añadimos el tipo de dato al objeto de tipo Trama.
                    #print(f"El tipo de dato entrante es {tipo_dato}")                                                                   # Mostramos el tipo de dato.
                elif len(datos) >= 5:                                                                                                   # Si la longitud de los datos es mayor o igual a 5, entonces
                    trama.entrada(trama.inicio, trama.fin, trama.cantidad, trama.tipo, datos[4:])                                       # Añadimos los datos al objeto de tipo Trama.
                    if len(datos) > cantidad_esperada + 4:                                                                              # Si la longitud de los datos es mayor a la cantidad esperada + 4, entonces
                        #print("Error: La longitud de la trama es mayor a la cantidad esperada")                                         # Mostramos un mensaje de error.
                        cuadro_texto.delete(1.0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        trama.entrada(0, 0, 0, 0, [])                                                                                   # Limpiamos el objeto de tipo Trama.
                        break                                                                                                           # Salimos del bucle.
                    elif len(datos) == cantidad_esperada + 4:                                                                           # Si la longitud de los datos es igual a la cantidad esperada + 4, entonces    
                        if conectar.in_waiting == 0:                                                                                    # Si no hay datos en el puerto serie, entonces
                            trama.entrada(trama.inicio, trama.fin, trama.cantidad, trama.tipo, datos[4:])                               # Añadimos los datos al objeto de tipo Trama.
                            #print(f"Mensaje entrante: {datos.hex()}")                                                                   # Mostramos los datos recibidos por el puerto serie.
                            #print(f"Trama entrante: {trama}")                                                                           # Mostramos la trama recibida por el puerto serie.
                            trama.entrada(0, 0, 0, 0, [])                                                                               # Limpiamos el objeto de tipo Trama.
                            break                                                                                                       # Salimos del bucle.
                    else:                                                                                                               # Si la longitud de los datos es menor a la cantidad esperada + 4, entonces
                        if conectar.in_waiting == 0:                                                                                    # Si no hay datos en el puerto serie, entonces
                            #print("Error: La longitud del mensaje es menor a la cantidad esperada")                                     # Mostramos un mensaje de error.
                            cuadro_texto.delete(1.0, tk.END)                                                                            # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                            trama.entrada(0, 0, 0, 0, [])                                                                               # Limpiamos el objeto de tipo Trama.
                            break                                                                                                       # Salimos del bucle.
                elif len(datos) >= 15:                                                                                                  # Si la longitud de los datos es mayor o igual a 15, entonces
                    #print("Error: La longitud de la trama es mayor a 15 bytes")                                                         # Mostramos un mensaje de error.
                    cuadro_texto.delete(1.0, tk.END)                                                                                    # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                    trama.entrada(0, 0, 0, 0, [])                                                                                       # Limpiamos el objeto de tipo Trama.
                    break                                                                                                               # Salimos del bucle.
    else:                                                                                                                               # Si el puerto no está conectado, entonces
        cuadro_texto.delete(1.0, tk.END)                                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.

   
        





########################################## Fin de funciones ##################################################


################################################## Variables globales ##################################################
conectar = None     
# Parte de la interfaz gráfica
ventana = tk.Tk(className=" TestPort")
ventana.geometry("305x350")
ventana.config(bg="grey")
datavaris = tk.StringVar() #Variable para enviar datos por el puerto serie 
vdatos = ttk.Entry(ventana, textvariable=datavaris, width="40") #Entrada de datos
vdatos.place(x=22, y=140) #Posición de la entrada de datos

#cambiamos icon
ventana.iconbitmap("mvp.ico")

#Ahora vamos a poner una etiqueta de titulo de nuestro programa
etiqueta = tk.Label(ventana, text=" TEST DE PUERTO SERIE", font=("Arial",14),bg="red",fg="white")
etiqueta.pack(side=tk.TOP, fill="both")

#Creamos combobox para mostrar los puertos COM disponibles.
combo_puertos = ttk.Combobox(ventana, state='readonly')
combo_puertos.place(x=5, y=35)

#Ahora creamos un boton para actualizar la lista de puertos COM disponibles.
btn_actualizar = tk.Button(ventana, text="Actualizar", command=mostrar_puertos_com)
btn_actualizar.place(x=235, y=30)

#Ahora creamos un botón para conectar al puerto COM que hemos selecionado.
btn_conectar = tk.Button(ventana, text="Conectar", command=conectar_o_desconectar)
btn_conectar.place(x=155, y=30)

#Etiqueta para mostrar ENVIAR DATOS
etiqueta_datos = tk.Label(ventana, text="ENVIAR DATOS", font=("Arial",15), padx=1, pady=10, bg="brown", fg="white")
etiqueta_datos.place(x=10, y=80)
   
#Boton de inicio envia de la trama
boton_start = tk.Button(ventana, text="START", font=("Arial",15), padx=1, pady=1, bg="green4", fg="white",activebackground="green2", activeforeground="black", command=datos_start)
boton_start.place(x=180, y =80)

# Etiqueta para mostrar RECIBIR DATOS
etiqueta_datos = tk.Label(ventana, text="RECIBIR DATOS", font=("Arial",15), padx=1, pady=1, bg="brown", fg="white")
etiqueta_datos.place(x=10, y=200)
    
#Boton de inicio envia de la trama
boton_start = tk.Button(ventana, text="RECIBIR", font=("Arial",15), padx=1, pady=1, bg="green4", fg="white",activebackground="green2", activeforeground="black", command=recibir_datos)
boton_start.place(x=180, y =200)

#Creamos un cuadro de texto para mostrar los datos recibidos
cuadro_texto = tk.Text(ventana, width=30, height=1)
cuadro_texto.place(x=22, y=240)

########################################## Fin de variables globales ##################################################

########################################## Estructura de la trama que vamos a enviar por el puerto serie ##############################################

# Estructura de la trama que vamos a enviar por el puerto serie.
'''
La trama que vamos a enviar por el puerto serie tiene la siguiente estructura:
[a], [b], [c], [d], [e] teniendo en cuenta que
[a] es un byte que nos permite identificar el inicio de la trama.
[b] es un byte que nos permite identificar el final de la trama.
[c] es un byte que nos permite identificar la cantidad de datos que vamos a enviar.
[d] es un byte que nos permite identificar el tipo de dato que vamos a enviar.
[e] es variable (entre 0 y 15 bytes) que nos permite enviar los datos.

Ejemplo:
0A A0 02 0B 05 14
'''
class Trama:
    def __init__(self, inicio, fin, cantidad, tipo, datos):
        """
        Inicializa una instancia de la clase.

        Parámetros:
        - inicio: El valor de inicio.
        - fin: El valor de fin.
        - cantidad: La cantidad de elementos.
        - tipo: El tipo de dato.
        - datos: Una lista de datos.

        """
        self.inicio = inicio
        self.fin = fin
        self.cantidad = cantidad
        self.tipo = tipo
        self.datos = datos[:15]

    def entrada(self, inicio, fin, cantidad, tipo, datos):
        """
        Esta función se encarga de procesar la entrada de datos.

        Parámetros:
        - inicio (int): El valor de inicio.
        - fin (int): El valor de fin.
        - cantidad (int): La cantidad de elementos.
        - tipo (str): El tipo de datos.
        - datos (list): La lista de datos.

        Retorna:
        None
        """
        self.inicio = inicio
        self.fin = fin
        self.cantidad = cantidad
        self.tipo = tipo
        self.datos = datos[:15]


    # Función para convertir la trama en bytes.
    def __bytes__(self):
        return bytes([self.inicio, self.fin, self.cantidad, self.tipo]) + self.datos
    
    # Función para convertir la trama en string.
    def __str__(self):
        return f"{self.inicio:02X} {self.fin:02X} {self.cantidad:02X} {self.tipo:02X} {' '.join(f'{b:02X}' for b in self.datos)}"
    
    # Función para recuperar la cantidad de datos que vamos a enviar.
    def __len__(self):
        return len(self.datos)
    
    # Función para recuperar el mensaje que vamos a enviar.
    def __getitem__(self, index):
        return self.datos[index]
    
    # Función para recuperar el tipo de dato que vamos a enviar.
    def __iter__(self):
        return iter(self.datos)
    
########################################## Fin de la estructura de la trama que vamos a enviar por el puerto serie ##############################################


##################################################### PROGRAMA PRINCIPAL ######################################################
mostrar_puertos_com()
ventana.mainloop()
##################################################### FIN DEL PROGRAMA PRINCIPAL ######################################################
