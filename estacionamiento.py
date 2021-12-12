
#Librerias que se utilizan
import tkinter
import math
from tkinter.constants import TRUE
import serial
from datetime import datetime
import mysql.connector



import threading


#Definición de las funciones-------------------------------------------------
def generarEspaciosEstacionamiento(frameCont, et):
    ''' Esta función genera todos los Label que representan visualmente los espacios
        del estacionamiento
    
        @param frameCont el frame donde se generaran los espacios de estacionamiento
        @param et indica los espacios totales que se van a generar

    '''
    global listaEspaciosDisponibles
    listaEspaciosDisponibles = []
    contador = 1
    for i in range(math.ceil(et/5)):
        for j in range(5):
            if(contador > et):
                break
            f = tkinter.Frame(frameCont, background="#cecece")
            f.config(padx=5, pady=5)
            label = tkinter.Label(f, text = f"{contador}", bd=0)
            label.config(width=5, height=2)
            label["bg"] = VERDE
            label.pack(padx=2, pady=2)
            listaEspaciosDisponibles.append(label)
            f.grid(row=i, column=j)
            contador +=1

def clearEspacios(frame):
    ''' Esta función se encarga de borrar los widgets dentro de un frame
    
        @param frame es el contenedor al cual se le borraran los widgets
    '''
    list = frame.grid_slaves()
    for l in list:
        l.destroy()

def editarEspaciosTotales():
    ''' Esta función se utiliza para actualizar los espacios totales cuando
        se usa el boton de editar espacios totales.
    '''
    global espacios_totales
    espacios_totales = int(textEspaciosTotales.get())
    global espacios_disponibles
    espacios_disponibles = espacios_totales
    labelEspaciosTotales2.config(text=f"{espacios_totales}")
    labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")
    clearEspacios(frameEspacios3)
    generarEspaciosEstacionamiento(frameEspacios3 , espacios_totales)

def eventoScrollListas(a, b):
    ''' Esta función sirve para controlar sincronizar el scroll de todos los 
        listbox widgets con el scroll general del frame
    '''
    listaId.yview(a, b)
    listaEspacio.yview(a, b)
    listaFecha.yview(a, b)
    listaHora.yview(a, b)

def isEstacionamientoLleno():
    ''' Esta función indica si el estacionamiento esta completamente lleno,
        osea que indica si ya no existen espacios disponibles

        @return devulve true si el estacionamiento se encuentra lleno, false en caso contrario.
    '''
    global espacios_disponibles
    return espacios_disponibles <= 0

def ocuparEspacioEstacionamiento(arduino):
    ''' Esta función nos sirve para remover uno de los espacios disponibles y 
        en el estacionamiento pasarlo a ocupado.

        @param arduino el objeto para mandar mensajes al arduino
    '''
    listaEspaciosDisponibles[0].config(bg=ROJO)
    removed = listaEspaciosDisponibles.pop(0)
    listaEspaciosOcupados.append(removed)
    global espacios_disponibles
    espacios_disponibles -= 1
    labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")
    registroEntrada(removed['text'])
    if(isEstacionamientoLleno()):
        arduino.write(b'lleno')
        print("esta lleno")

def desocuparEspacioEstacionamiento():
    ''' Esta función nos sirve para remover uno de los espacios ocupados y 
        pasarlo a disponible.

        @param arduino el objeto para mandar mensajes al arduino
    '''
    print("desocupando")
    removed = listaEspaciosOcupados.pop()
    removed.config(bg=VERDE)
    listaEspaciosDisponibles.insert(0, removed)
    global espacios_disponibles
    espacios_disponibles += 1
    labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")

def registroEntrada(numEspacio):
    ''' Esta función carga un registro de entrada en la tabla de
        historial de entradas.

        @param numEspacio es el número asignado que tine el espacio en el estacionamiento
    '''
    global contador
    global listaId
    global listaEspacio
    global listaFecha 
    global listaHora
    contador += 1
    fecha = datetime.today().strftime('%Y-%m-%d')
    hora = datetime.today().strftime('%H:%M')
    listaId.insert("end", contador)
    listaEspacio.insert("end", numEspacio)
    listaFecha.insert("end",fecha)
    listaHora.insert("end",hora)
    agregarRegistroDB(db, numEspacio, fecha, hora)

def agregarRegistroDB(db, numEspacio, fecha, hora):
    ''' Esta función registra los atributos de una entrada en la base de datos MySQL

        @param db la conexión con la base de datos
        @param numEspacio es el número asignado que tine el espacio en el estacionamiento
        @param fecha la fecha en la que se registro la entrada
        @param hora la hora en la que se registro la entrada
    '''
    query = f"INSERT INTO entrada(numEspacio, fecha, hora) VALUES ({numEspacio}, '{fecha}', '{hora}');"
    #Objeto para ejectuar los queries
    mycursor = db.cursor()
    mycursor.execute(query)
    db.commit()

def recibirComandos():
    ''' Esta función recibe todos los comandos que el arduino envia para 
        realizar las diferetes acciones, como abrir la pluma barrera.
    '''
    while True:
        print("Esperando por actualización de los sensores...")
        print()
      

        #El ciclo continua hasta que se reciba un mensaje
        while(True): 
            
            # Lee el puerto serie. Elimina los dos ultimos caracteres que
            # son el salto de linea
            data = arduino.readline()[:-2]
            # Si se mando el comando 'Alarma-ON'
            if data:
                data = str(data).split("'")[1]
                if(data == 'carro-estacionado'):
                    if(not isEstacionamientoLleno()):
                        ocuparEspacioEstacionamiento(arduino)
                        print("se estaciona")   
                      
                elif(data == 'carro-salida'):
                    if(espacios_disponibles != espacios_totales):
                        desocuparEspacioEstacionamiento()
                        arduino.write(b'disp')
                elif(data == 'pluma-abierta'):
                    labelPluma2.config(text="Abierto")
                    labelPluma2.config(bg=VERDE)
                elif(data == 'pluma-cerrada'):
                    labelPluma2.config(text="Cerrado")
                    labelPluma2.config(bg=ROJO)     
                elif(data.split(":")[0] == 'distancia'):
                    distancia = data.split(":")[1]
                    labelSensor2.config(text=f"{distancia}"+ " cm")

                    
                print(data)
                print()
                #Sale del ciclo
                break

#Variables generales----------------------------------------------------------
#Hay que cambiar de COM4 a COM3
arduino = serial.Serial('COM4', 9600, timeout = 1)

#Cantidad de espacios totales en el estacionamiento
espacios_totales = 23
#Cantidad de espacios disponibles en el estacionamiento
espacios_disponibles = espacios_totales

#Colores
ROJO = '#FF5773'
VERDE = '#35DE55'

#Guarda los espacios que se encuentran disponibles
listaEspaciosDisponibles = []
#Guarda los espacios que se encuentran ocupados
listaEspaciosOcupados = []

#Lleva el conteo de los los registros de entrada
contador = 0

#Coneccion con base de datos mysql
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234",
  database="estacionamiento"
)


#Generación de la interfaz gráfica
#Se crea la ventana
ventana = tkinter.Tk()
ventana.title("Sistema de estacionamiento")

ventana["bg"] = "grey" 
#Dejar el tamaño de la ventana fijo
ventana.resizable(False,True)
#Redimencionar la ventana
ventana.geometry("500x600")

#Primer modulo de la interfaz------------------------------------------------
frameEspacios1 = tkinter.Frame(ventana) 
frameEspacios1.config(width="50", height="50")
frameEspacios1.config(bg="white")
frameEspacios1.pack(fill="x")

frameEspacios2 = tkinter.Frame(frameEspacios1) 
frameEspacios2.config(bg="#7A1BF7")
frameEspacios2.pack(fill="x")
labelEspacios = tkinter.Label(frameEspacios2)
labelEspacios.config(text="Espacios disponibles")
labelEspacios.config(font=("Arial", 16))
labelEspacios.config(fg="white")
labelEspacios.config(pady=5)
labelEspacios.config(bg="#7A1BF7")
labelEspacios.pack(fill="x", expand=True)

frameEspacios3 =  tkinter.Frame(frameEspacios1) 
frameEspacios3.config(bg="white")
frameEspacios3.pack()

generarEspaciosEstacionamiento(frameEspacios3 , espacios_totales)

#Segundo modulo de la interfaz------------------------------------------------
frameInformacion1 = tkinter.Frame(ventana)
frameInformacion1.config(width="50", height="50")
frameInformacion1.config(bg="white")
frameInformacion1.pack(fill="x")

frameInformacion2 = tkinter.Frame(frameInformacion1)
frameInformacion2.config(bg="#2433E0")
frameInformacion2.pack(fill="x")

labelInformacion = tkinter.Label(frameInformacion2)
labelInformacion.config(text="Información del estacionamiento")
labelInformacion.config(font=("Arial", 16))
labelInformacion.config(fg="white")
labelInformacion.config(pady=5)
labelInformacion.config(bg="#2433E0")
labelInformacion.pack(side="top")

frameInformacion3 = tkinter.Frame(frameInformacion1)
frameInformacion3.pack(fill="x")

labelEspaciosTotales = tkinter.Label(frameInformacion3)
labelEspaciosTotales.config(text="Espacios totales: ")
labelEspaciosTotales.config(font=("Arial", 12))
labelEspaciosTotales.grid(row=0,column=0)

labelEspaciosTotales2 = tkinter.Label(frameInformacion3)
labelEspaciosTotales2.config(text=f"{espacios_totales}")
labelEspaciosTotales2.config(width=5)
labelEspaciosTotales2.config(font=("Arial", 12))
labelEspaciosTotales2.grid(row=0,column=1)

textEspaciosTotales = tkinter.Entry(frameInformacion3)
textEspaciosTotales.config(width="20")
textEspaciosTotales.grid(row=0, column=2)

botonEspaciosTotales = tkinter.Button(frameInformacion3)
botonEspaciosTotales.config(text="Editar")
botonEspaciosTotales.config(command=lambda:editarEspaciosTotales())
botonEspaciosTotales.grid(row=0, column=3)

frameInformacion4 = tkinter.Frame(frameInformacion1)
frameInformacion4.pack(fill="x")

labelEspaciosDisponibles = tkinter.Label(frameInformacion4)
labelEspaciosDisponibles.config(text="Espacios disponibles: ")
labelEspaciosDisponibles.config(font=("Arial", 12))
labelEspaciosDisponibles.grid(row=1,column=0)

labelEspaciosDisponibles2 = tkinter.Label(frameInformacion4)
labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")
labelEspaciosTotales2.config(width=5)
labelEspaciosDisponibles2.config(font=("Arial", 12))
labelEspaciosDisponibles2.grid(row=1,column=1)

frameInformacion5 = tkinter.Frame(frameInformacion1)
frameInformacion5.pack(fill="x")

labelPluma = tkinter.Label(frameInformacion5)
labelPluma.config(text="Barrera pluma: ")
labelPluma.config(font=("Arial", 12))
labelPluma.grid(row=2,column=0)

labelPluma2 = tkinter.Label(frameInformacion5)
labelPluma2.config(padx=6)
labelPluma2.config(text=f"Cerrada")
labelPluma2.config(width=5)
labelPluma2.config(bg=ROJO)
labelPluma2.config(fg="white")
labelPluma2.config(font=("Arial", 12))
labelPluma2.grid(row=2,column=1)

frameInformacion6 = tkinter.Frame(frameInformacion1)
frameInformacion6.pack(fill="x")

labelSensor = tkinter.Label(frameInformacion6)
labelSensor.config(text="Sensor ultrasonico: ")
labelSensor.config(font=("Arial", 12))
labelSensor.grid(row=3,column=0)

labelSensor2 = tkinter.Label(frameInformacion6)
labelSensor2.config(padx=6)
labelSensor2.config(text=f"0"+" cm")
labelSensor2.config(width=5)
labelSensor2.config(font=("Arial", 12))
labelSensor2.grid(row=3,column=1)

#Segundo modulo de la interfaz------------------------------------------------
frameHistorial1 = tkinter.Frame(ventana)
frameHistorial1.config(width="50", height="50")
frameHistorial1.config(bg="white")
frameHistorial1.pack(fill="x")

frameHistorial2 = tkinter.Frame(frameHistorial1)
frameHistorial2.config(bg="#23A0FA")
frameHistorial2.pack(fill="x")

labelHistorial = tkinter.Label(frameHistorial2)
labelHistorial.config(text="Historial de entradas")
labelHistorial.config(font=("Arial", 16))
labelHistorial.config(fg="white")
labelHistorial.config(pady=5)
labelHistorial.config(bg="#23A0FA")
labelHistorial.pack(side="top")

frameHistorial2 = tkinter.Frame(frameHistorial1)
frameHistorial2.pack(fill="x")

frameHistorial3 = tkinter.Frame(frameHistorial2)
frameHistorial3.pack(side="top", fill="x")

labelId = tkinter.Label(frameHistorial3)
labelId.config(text="Id")
labelId.config(bd=2)
labelId.config(relief="solid")
labelId.config(width=17)
labelId.pack(side="left")

labelEspacio = tkinter.Label(frameHistorial3)
labelEspacio.config(text="Número")
labelEspacio.config(bd=2)
labelEspacio.config(relief="solid")
labelEspacio.config(width=17)
labelEspacio.pack(side="left")

labelFecha = tkinter.Label(frameHistorial3)
labelFecha.config(text="Fecha")
labelFecha.config(bd=2)
labelFecha.config(relief="solid")
labelFecha.config(width=17)
labelFecha.pack(side="left")

labelHora = tkinter.Label(frameHistorial3)
labelHora.config(text="Hora")
labelHora.config(bd=2)
labelHora.config(relief="solid")
labelHora.config(width=17)
labelHora.pack(side="left")

scrollbar = tkinter.Scrollbar(frameHistorial2)
scrollbar.pack(side="right", fill="y")

listaId = tkinter.Listbox(frameHistorial2, yscrollcommand = scrollbar.set)
listaId.config(width=20)
listaId.pack(side="left")

listaEspacio = tkinter.Listbox(frameHistorial2, yscrollcommand = scrollbar.set)
listaEspacio.config(width=20)
listaEspacio.pack(side="left")


listaFecha = tkinter.Listbox(frameHistorial2, yscrollcommand = scrollbar.set)
listaFecha.config(width=20)
listaFecha.pack(side="left")


listaHora = tkinter.Listbox(frameHistorial2, yscrollcommand = scrollbar.set)
listaHora.config(width=20)
listaHora.pack(side="left")

    


scrollbar.config( command = eventoScrollListas)


x = threading.Thread(target=recibirComandos)
x.start()


#Se inicializa la ventana
ventana.mainloop()



