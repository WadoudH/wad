#PROGRAMA PARA TESTEAR EL PUERTO SERIE CON UN PIC

##################################################Importaciones necesarias##################################################
import tkinter as tk                                                                                                             # Importamos la librería tkinter para crear la interfaz gráfica.
import serial                                                                                                                    # Importamos la librería serial para la comunicación con el puerto serie.
from tkinter import ttk 
from tkinter import *
from serial.tools import list_ports
import time
import csv
import os
import os
import csv
import time
import tkinter as tk
from tkinter import ttk

################################################## Fin de importaciones ##################################################

##################################################     Funciones     ##################################################

def insertar_texto(variable, texto):
    variable.insert(tk.END, texto) 

def limpiar_texto(variable):
    variable.delete(1.0, tk.END)

def limpiar_insertar_texto(variable, texto):
    limpiar_texto(variable)
    insertar_texto(variable, texto)

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
        limpiar_insertar_texto(text_estado_envio, "Esperando datos..")
        limpiar_insertar_texto(text_estado_recibido, "Esperando datos..")
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
        limpiar_insertar_texto(text_estado_envio, "Esperando conexion..")
        limpiar_insertar_texto(text_estado_recibido, "Esperando conexion..")
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

def datos_start(args=None):
    """
    Esta función se utiliza para enviar datos por el puerto serie.
    """
    if not conectar:                                                                                                                # Si el puerto no está conectado, entonces
        print("Error: El puerto no está conectado")                                                                                 # Mostramos un mensaje de error.                                                                                  
        limpiar_insertar_texto(text_estado_envio, "Error: Puerto desconectado")                                                     # Limpiamos el cuadro de texto para mostrar el estado de la recepción.
        vdatos.delete(0, tk.END)                                                                                                    # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.    
        return                                                                                                                      # Salimos de la función.       
    else:                                                                                                                           # Si el puerto está conectado, entonces                                         
        if datavaris.get() == "":                                                                                                   # Si la entrada de datos está vacía, entonces  
            if args != None:                                                                                                        # Verificamos si la entrada de argumentos no está vacía, entonces
                datavaris.set(args)                                                                                                 # Establecemos la entrada de datos con los argumentos.tos.
                datos_start()
                return                                                                                                       # Llamamos a la función de nuevo.
            else:                                                                                                                   # Si la entrada de argumentos está vacía, entonces
                print("Error: La entrada de datos está vacía")                                                                      # Mostramos un mensaje de error.
                return                                                                                                              # Salimos de la función.
        else:                                                                                                                       # Si la entrada de datos no está vacía, entonces
            if datavaris.get()[0:2] not in inicio_header:                                                                           # Si el primer byte no es 0x0A, entonces
                print("Error: El primer byte no es correcto")                                                                       # Mostramos un mensaje de error.
                vdatos.delete(0, tk.END)                                                                                            # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                return                                                                                                              # Salimos de la función.
            else:                                                                                                                   # Si el primer byte es 0x0A, entonces
                if datavaris.get()[2:4] not in fin_header:                                                                          # Si el segundo byte no es 0xA0, entonces
                    print("Error: El segundo byte no es correcto")                                                                  # Mostramos un mensaje de error.
                    vdatos.delete(0, tk.END)                                                                                        # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                    return                                                                                                          # Salimos de la función.
                else:                                                                                                               # Si el segundo byte es 0xA0, entonces
                    if ((len(datavaris.get())/2) != int(datavaris.get()[4:6], 16) + 4):                                             # Si la longitud del mensaje es diferente a la cantidad esperada + 4, entonces
                        #print(int(datavaris.get()[4:6],16))                                                                         # Mostramos la cantidad esperada.    
                        #print("Mensaje entrante: ", datavaris.get())                                                                # Mostramos el mensaje entrante.
                        #print("cantidad esperada: ", int(datavaris.get()[4:6], 16) + 8)                                             # Mostramos la cantidad esperada.
                        #print("longitud del mensaje: ", len(datavaris.get()))                                                       # Mostramos la longitud del mensaje.
                        print("Error: La longitud del mensaje es diferente!!")                                                      # Mostramos un mensaje de error.
                        vdatos.delete(0, tk.END)                                                                                    # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        return                                                                                                      # Salimos de la función.
                    else:                                                                                                           # Si la longitud del mensaje es igual a la cantidad esperada + 4, entonces
                        #print("Tipo: ", datavaris.get()[6:8])
                        if datavaris.get()[6:8] not in tipos_aceptados:                                                             # Si el tipo de dato no es 0x0B, entonces
                            print("Error: El tipo de dato no es acceptado")                                                         # Mostramos un mensaje de error.
                            vdatos.delete(0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                            return                                                                                                  # Salimos de la función.
                        else:                                                                                                       # Si el tipo de dato es 0x0B, entonces
                            conectar.write(bytearray.fromhex(datavaris.get()))                                                      # Enviamos el mensaje por el puerto serie.
                            limpiar_insertar_texto(text_estado_envio, "Datos enviados")                                              # Limpiamos el cuadro de texto para mostrar el estado de la recepción.
                            limpiar_insertar_texto(text_tipo_envio, seleccion_tipo(int(datavaris.get()[6:8], 16)))                 # Limpiamos el cuadro de texto para mostrar el tipo de dato.
                            extraccion_csv(datavaris.get())
                            return datavaris.get()                                                                                  # Retornamos el mensaje enviado.

def programa_recibir_datos(args=None):
    """
    Esta función se utiliza para recibir datos por el puerto serie.
    """
    limpiar_insertar_texto(text_estado_recibido, "Esperando datos")
    limpiar_texto(text_datos_recibidos)
    limpiar_texto(text_tipo_recibido)
    if conectar:                                                                                                                        # Si el puerto está conectado, entonces
        if conectar.in_waiting:                                                                                                         # Si hay datos en el puerto serie, entonces
            bandera = False
            datos = bytearray()                                                                                                         # Creamos un objeto de tipo bytearray para almacenar los datos recibidos por el puerto serie.
            trama = Trama(0, 0, 0, 0, [])                                                                                               # Creamos un objeto de tipo Trama para almacenar la trama recibida por el puerto serie que sera el mensaje final.
            while conectar.in_waiting:                                                                                                  # Mientras haya datos en el puerto serie, entonces
                byte = conectar.read(1)                                                                                                 # Leemos un byte del puerto serie.
                datos.append(byte[0])                                                                                                   # Añadimos el byte leído al objeto de tipo bytearray.
                limpiar_insertar_texto(text_estado_recibido, "Datos recibidos")
                limpiar_insertar_texto(text_datos_recibidos, datos.hex())
                if len(datos) == 1:                                                                                                     # Si la longitud de los datos es igual a 1, entonces
                    if datos[0] != 0x0A:                                                                                                # Verificamos si el primer byte no es 0x0A. Si no es 0x0A, entonces
                        print("Error: El primer byte no es 0A")                                                                         # Mostramos un mensaje de error.
                        text_datos_recibidos.delete(1.0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        break                                                                                                           # Salimos del bucle.
                    else:                                                                                                               # Si el primer byte es 0x0A, entonces
                        trama.entrada(datos[0], 0, 0, 0, [])                                                                            # Añadimos el primer byte al objeto de tipo Trama.
                elif len(datos) == 2:                                                                                                   # Si la longitud de los datos es igual a 2, entonces
                    if datos[1] != 0xA0:                                                                                                # Verificamos si el segundo byte no es 0xA0. Si no es 0xA0, entonces
                        print("Error: El segundo byte no es A0")                                                                        # Mostramos un mensaje de error.
                        text_datos_recibidos.delete(1.0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                        break                                                                                                           # Salimos del bucle.
                    else:                                                                                                               # Si el segundo byte es 0xA0, entonces
                        trama.entrada(trama.inicio, datos[1], 0, 0, [])                                                                 # Añadimos el segundo byte al objeto de tipo Trama.
                elif len(datos) == 3:                                                                                                   # Si la longitud de los datos es igual a 3, entonces
                    cantidad_esperada = datos[2]                                                                                        # Guardamos la cantidad de datos esperados.
                    trama.entrada(trama.inicio, trama.fin, cantidad_esperada, 0, [])                                                    # Añadimos la cantidad de datos esperados al objeto de tipo Trama.
                    #print(f"La longitud de la trama esperada del mensaje entrante es de {cantidad_esperada} bytes")                     # Mostramos la cantidad de datos esperados.
                elif len(datos) == 4:                                                                                                   # Si la longitud de los datos es igual a 4, entonces
                    tipo_dato = datos[3]                                                                                                # Guardamos el tipo de dato.
                    if datos[3] not in tipos_acceptados:                                                             # Si el tipo de dato no es 0x0B, entonces
                        print("Error: El tipo de dato no es acceptado")                                                         # Mostramos un mensaje de error.
                        vdatos.delete(0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                    else:
                        bandera = True
                    seleccion_tipo(tipo_dato)                                                                                           # Mostramos el tipo de dato en el cuadro de texto.
                    trama.entrada(trama.inicio, trama.fin, trama.cantidad, tipo_dato, [])                                               # Añadimos el tipo de dato al objeto de tipo Trama.
                elif len(datos) >= 5:                                                                                                   # Si la longitud de los datos es mayor o igual a 5, entonces
                    trama.entrada(trama.inicio, trama.fin, trama.cantidad, trama.tipo, datos[4:])                                       # Añadimos los datos al objeto de tipo Trama.
                    if len(datos) > cantidad_esperada + 4:                                                                              # Si la longitud de los datos es mayor a la cantidad esperada + 4, entonces
                        print("Error: La longitud de la trama es mayor a la cantidad esperada")                                         # Mostramos un mensaje de error.
                        limpieza_recibido()
                        trama.entrada(0, 0, 0, 0, [])                                                                                   # Limpiamos el objeto de tipo Trama.
                        break                                                                                                           # Salimos del bucle.
                    elif len(datos) == cantidad_esperada + 4:                                                                           # Si la longitud de los datos es igual a la cantidad esperada + 4, entonces    
                        if conectar.in_waiting == 0:                                                                                    # Si no hay datos en el puerto serie, entonces
                            if bandera:
                                trama.entrada(trama.inicio, trama.fin, trama.cantidad, trama.tipo, datos[4:])                               # Añadimos los datos al objeto de tipo Trama.
                                limpiar_insertar_texto(text_estado_recibido, "Datos recibidos")
                                limpiar_insertar_texto(text_datos_recibidos, datos.hex())
                                limpiar_insertar_texto(text_tipo_recibido, seleccion_tipo(trama.tipo))
                                print(trama.tipo, bandera)
                                extraccion_csv(datos.hex())
                                return datos.hex()                                                                                         # Retornamos los datos recibidos por el puerto serie.
                            else:
                                print("Error: El tipo de dato no es acceptado")                                                         # 
                                vdatos.delete(0, tk.END)                                                                                # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                                return None
                    else:                                                                                                               # Si la longitud de los datos es menor a la cantidad esperada + 4, entonces
                        if conectar.in_waiting == 0:                                                                                    # Si no hay datos en el puerto serie, entonces
                            print("Error: La longitud del mensaje es menor a la cantidad esperada")                                     # Mostramos un mensaje de error.
                            text_datos_recibidos.delete(1.0, tk.END)                                                                            # Limpiamos el cuadro de texto para mostrar los datos recibidos por el puerto serie.
                            limpieza_recibido()
                            trama.entrada(0, 0, 0, 0, [])                                                                               # Limpiamos el objeto de tipo Trama.
                            break                                                                                                       # Salimos del bucle.
                elif len(datos) >= 15:                                                                                                  # Si la longitud de los datos es mayor o igual a 15, entonces
                    print("Error: La longitud de la trama es mayor a 15 bytes")                                                         # Mostramos un mensaje de error.
                    limpieza_recibido()
                    trama.entrada(0, 0, 0, 0, [])                                                                                       # Limpiamos el objeto de tipo Trama.
                    break                                                                                                               # Salimos del bucle.
        else:                                                                                                                           # Si no hay datos en el puerto serie, entonces
            print("Error: No hay datos en el puerto serie")                                                                            # Mostramos un mensaje de error.
    else:                                                                                                                               # Si el puerto no está conectado, entonces
        print("Error: El puerto no está conectado")                                                                                    # Mostramos un mensaje de error.

def recibir_datos():
    A, B, C = None, None, None
    A = programa_recibir_datos()
    ventana.update()
    time.sleep(1)
    print("A: ", A)
    if A != None:
        print("Progama ha recibido: ", A, " y lo va a procesar")
        B = tratamiendo_datos(A)
        ventana.update()
        time.sleep(1)
        if B != None:
            print("Programa ha enviado: ", B, " a parquimetro")
            C = datos_start(B)
            ventana.update()
            time.sleep(1)
            limpieza_recibido()
            ventana.update()
            print("A: ", A)
            print("B: ", B)
            C = programa_recibir_datos()
            ventana.update()
            time.sleep(1)
            print("C: ", C)
        else:
            print("Error: el programa no ha podido procesar los datos")
    else:
        print("Error: el programa no ha podido recibir los datos")
    
def seleccion_tipo(tipo):
    if tipo == 0x0B:
        text_tipo_recibido.insert(tk.END, "Peticion cobro en Visa..")
        return "Peticion cobro en Visa.."
    elif tipo == 0x0C:
        text_tipo_recibido.insert(tk.END, "Recepcion correcta..")
        return "Recepcion correcta.."
    elif tipo == 0x0D:
        text_tipo_recibido.insert(tk.END, "Cobro rechazado..")
        return "Cobro rechazado.."
    elif tipo == 0x0E:
        text_tipo_recibido.insert(tk.END, "Cobro acceptado..")
        return "Cobro acceptado.."
    elif tipo == 0x0F:
        text_tipo_recibido.insert(tk.END, "Peticion registro cobro..")
        return "Peticion registro cobro.."
    elif tipo == 0x10:
        text_tipo_recibido.insert(tk.END, "Recepcion registro cobro..")
        return "Recepcion registro cobro.."
    elif tipo == 0x11:
        text_tipo_recibido.insert(tk.END, "Registro alarma..")
        return "Registro alarma.."
    elif tipo == 0x12:
        text_tipo_recibido.insert(tk.END, "Confirmacion alarma..")
        return "Confirmacion alarma.."
    else:
        text_tipo_recibido.insert(tk.END, "Tipo de dato no reconocido..", tipo)
        return "Tipo de dato no reconocido.."

def tratamiendo_datos(recepcion):
    if recepcion != None:
        array = bytearray.fromhex(recepcion)
        print(array)
        if array[3] == 0x0B:
            array[3] = 0x0C
        elif array[3] == 0x0C:
            array[3] = 0x0D
        elif array[3] == 0x0F:
            array[3] = 0x10
        elif array[3] == 0x11:
            array[3] = 0x12
        print(array)
        return array.hex()
    else:
        return None
    
def limpieza_envio():
    limpiar_insertar_texto(text_estado_envio, "Esperando datos")
    limpiar_texto(text_tipo_envio)
    vdatos.delete(0, tk.END)

def limpieza_recibido():
    limpiar_insertar_texto(text_estado_recibido, "Esperando datos")
    limpiar_texto(text_datos_recibidos)
    limpiar_texto(text_tipo_recibido)

def extraccion_csv(datos):
    try:
        # Si el archivo no existe, lo creamos
        if not os.path.exists('datos.csv'):
            mode = 'w'
            identificador = 360000001 # mas adelante, tendríamos que leer el último identificador del archivo
            print(identificador)
        else:
            mode = 'a'
            with open('datos.csv', 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                identificador = 360000000 + len(lines)
        with open('datos.csv', mode, newline='') as file:
            writer = csv.writer(file)
            if mode == 'w':
                writer.writerow(["Identificador", "dia/mes/año", "hora:minuto:segundo", "Trama", "Importe final"])
                writer.writerow([identificador, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), datos, str(int(datos[8:10], 16) + int(datos[10:12], 16)/100)])
            else:
                writer.writerow([identificador, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), datos, str(int(datos[8:10], 16) + int(datos[10:12], 16)/100)])
    except Exception as e:
        print("An error occurred:", str(e))

def limpiar_insertar_texto(text_widget, text):
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)

def limpiar_texto(text_widget):
    text_widget.delete(1.0, tk.END)


########################################## Fin de funciones ############################################################
################################################## Variables globales ##################################################
conectar = None     
inicio_header = ["0a", "0A"]
fin_header = ["a0", "A0"]
tipos_aceptados = ["0b", "0B", "0c", "0C", "0d", "0D", "0e", "0E", "0f", "0F", "10", "11", "12"]
tipos_acceptados = [0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12]                                                                  
########################################## Fin de variables globales #####################################################
########################################## Parte de la interfaz gráfica ##################################################
ventana = tk.Tk(className=" TestPort")
ventana.geometry("500x550")
ventana.config(bg="grey")

# Cabecera de la ventana principal
altura_cabecera = 40
altura_envio = altura_cabecera + 50
altura_recibir = altura_envio + 200
etiqueta = tk.Label(ventana, text=" TEST DE PUERTO SERIE", font=("Arial",14),bg="red",fg="white")
etiqueta.pack(side=tk.TOP, fill="both")
datavaris = tk.StringVar() #Variable para enviar datos por el puerto serie
# Puertos COM
combo_puertos = ttk.Combobox(ventana, state='readonly')
combo_puertos.place(x=40, y=altura_cabecera, width=120, height=30)
# Actualizar
btn_actualizar = tk.Button(ventana, text="Actualizar", command=mostrar_puertos_com)
btn_actualizar.place(x=350, y=altura_cabecera, width=100, height=30)
# Conectar
btn_conectar = tk.Button(ventana, text="Conectar", command=conectar_o_desconectar)
btn_conectar.place(x=200, y=altura_cabecera, width=100, height=30)
# Enviar datos
vdatos = ttk.Entry(ventana, width="40", textvariable=datavaris)
vdatos.place(x=250, y=altura_envio + 50, width=200, height=20)
text_cabecera_enviados = tk.Label(ventana, text="ENVIAR DATOS", font=("Arial",12), padx=1, pady=5, bg="brown", fg="white")
text_cabecera_enviados.place(x=10, y=altura_envio, width=480)
text_estado_envio = tk.Text(ventana, width=20, height=1)
text_estado_envio.insert(tk.END, "Esperando conexion..")
text_estado_envio.place(x=250, y=altura_envio + 80, width=200)
text_tipo_envio = tk.Text(ventana, width=20, height=1)
text_tipo_envio.place(x=250, y=altura_envio + 110, width=200)
label_datos_envio = tk.Label(ventana, text="Datos a enviar", font=("Arial",10), padx=1, pady=1, bg="black", fg="white")
label_datos_envio.place(x=40, y=altura_envio + 50, width=200)
label_estado_envio = tk.Label(ventana, text="Estado del envio", font=("Arial",10), padx=1, pady=1, bg="black", fg="white")
label_estado_envio.place(x=40, y=altura_envio + 80, width=200)
label_tipo_envio = tk.Label(ventana, text="Tipo de dato", font=("Arial",10), padx=1, pady=1, bg="black", fg="white")
label_tipo_envio.place(x=40, y=altura_envio + 110, width=200)
button_start_envio = tk.Button(ventana, text="ENVIAR", font=("Arial",12), padx=1, pady=1, bg="green4", fg="white",activebackground="green2", activeforeground="black", command=datos_start)
button_start_envio.place(x=250, y =altura_envio + 140, width=200, height=30)
button_reset_envio = tk.Button(ventana, text="RESET", font=("Arial",12), padx=1, pady=1, bg="red", fg="white",activebackground="red2", activeforeground="black", command=limpieza_envio)
button_reset_envio.place(x=40, y=altura_envio + 140, width=200, height=30)
# Recibir datos
text_cabecera_recibidos = tk.Label(ventana, text="RECIBIR DATOS", font=("Arial",12), padx=1, pady=5, bg="brown", fg="white")
text_cabecera_recibidos.place(x=10, y=altura_recibir, width=480)
text_datos_recibidos = tk.Text(ventana, width=20, height=1)
text_datos_recibidos.place(x=250, y=altura_recibir + 50, width=200)
text_estado_recibido = tk.Text(ventana, width=20, height=1)
text_estado_recibido.insert(tk.END, "Esperando conexion..")
text_estado_recibido.place(x=250, y=altura_recibir + 80, width=200)
text_tipo_recibido = tk.Text(ventana, width=20, height=1)
text_tipo_recibido.place(x=250, y=altura_recibir + 110, width=200)
label_datos_recibidos = tk.Label(ventana, text="Datos recibidos", font=("Arial",10), padx=1, pady=1, bg="black", fg="white")
label_datos_recibidos.place(x=40, y=altura_recibir + 50, width=200)
label_estado_recibido = tk.Label(ventana, text="Estado de la recepción", font=("Arial",10), padx=1, pady=1, bg="black", fg="white")
label_estado_recibido.place(x=40, y=altura_recibir + 80, width=200)
label_tipo_recibido = tk.Label(ventana, text="Tipo de dato", font=("Arial",10), padx=1, pady=1, bg="black", fg="white")
label_tipo_recibido.place(x=40, y=altura_recibir + 110, width=200)
button_start_recibido = tk.Button(ventana, text="RECIBIR", font=("Arial",12), padx=1, pady=1, bg="green4", fg="white",activebackground="green2", activeforeground="black", command=recibir_datos)
button_start_recibido.place(x=250, y =altura_recibir + 140, width=200, height=30)
button_reset_recibido = tk.Button(ventana, text="RESET", font=("Arial",12), padx=1, pady=1, bg="red", fg="white",activebackground="red2", activeforeground="black", command=limpieza_recibido)
button_reset_recibido.place(x=40, y=altura_recibir + 140, width=200, height=30)

# Boton para cerrar la ventana principal y salir del programa.
btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
btn_cerrar.place(x=200, y=480, width=100, height=30)

# Icono de la ventana
ventana.iconbitmap("mvp.ico")
########################################## Fin de la interfaz gráfica ##################################################

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
    
    # Funcio que verifica si la trama es valida.
    def es_valida(self):
        return self.inicio == 0x0A and self.fin == 0xA0 and len(self) == self.cantidad
    
########################################## Fin de la estructura de la trama que vamos a enviar por el puerto serie ##############################################


##################################################### PROGRAMA PRINCIPAL ######################################################
mostrar_puertos_com()
ventana.mainloop()
##################################################### FIN DEL PROGRAMA PRINCIPAL ######################################################
