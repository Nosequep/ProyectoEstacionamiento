
#Librerias que se utilizan
import tkinter
import math
from tkinter.constants import TRUE
import serial
from datetime import datetime



import threading


#Definición de las funciones-------------------------------------------------
def generarEspaciosEstacionamiento(frameCont, et):
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
    list = frame.grid_slaves()
    for l in list:
        l.destroy()

def editarEspaciosTotales():
    global espacios_totales
    espacios_totales = int(textEspaciosTotales.get())
    global espacios_disponibles
    espacios_disponibles = espacios_totales
    labelEspaciosTotales2.config(text=f"{espacios_totales}")
    labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")
    clearEspacios(frameEspacios3)
    generarEspaciosEstacionamiento(frameEspacios3 , espacios_totales)

def eventoScrollListas(a, b):
    listaId.yview(a, b)
    listaEspacio.yview(a, b)
    listaFecha.yview(a, b)
    listaHora.yview(a, b)

def isEstacionamientoLleno():
    global espacios_disponibles
    return espacios_disponibles <= 0
        

#Variables generales----------------------------------------------------------
espacios_totales = 23
espacios_disponibles = espacios_totales

#Colores
ROJO = '#FF5773'
VERDE = '#35DE55'

listaEspaciosDisponibles = []
listaEspaciosOcupados = []

#Generación de la interfaz gráfica
#Se crea la ventana
ventana = tkinter.Tk()
ventana.title("Sistema de estacionamiento")
ventana["bg"] = "grey" 
#Dejar el tamaño de la ventana fijo
ventana.resizable(False,True)
#Redimencionar la ventana
ventana.geometry("500x500")

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



def recibirComandos():
    #Hay que cambiar de COM4 a COM3
    arduino = serial.Serial('COM4', 9600, timeout = 1)
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
                if(not isEstacionamientoLleno()):
                    if(data == b'carro-estacionado'):
                        ocuparEspacioEstacionamiento()
                        print("se estaciona")
                    elif(data == b'carro-salida'):
                        desocuparEspacioEstacionamiento()
                else: 

                    arduino.write(b'lleno')
                
                    
                print(data)
                print()
                #Sale del ciclo
                break

def ocuparEspacioEstacionamiento():
    listaEspaciosDisponibles[0].config(bg=ROJO)
    removed = listaEspaciosDisponibles.pop(0)
    listaEspaciosOcupados.append(removed)
    global espacios_disponibles
    espacios_disponibles -= 1
    labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")
    registroEntrada(removed['text'])

def desocuparEspacioEstacionamiento():
    removed = listaEspaciosOcupados.pop()
    removed.config(bg=VERDE)
    listaEspaciosDisponibles.insert(0, removed)
    global espacios_disponibles
    espacios_disponibles += 1
    labelEspaciosDisponibles2.config(text=f"{espacios_disponibles}")

def registroEntrada(numEspacio):
    global listaId
    global listaEspacio
    global listaFecha 
    global listaHora
    fecha = datetime.today().strftime('%Y-%m-%d')
    hora = datetime.today().strftime('%H:%M')
    listaId.insert("end", numEspacio)
    listaEspacio.insert("end", numEspacio)
    listaFecha.insert("end",fecha)
    listaHora.insert("end",hora)
x = threading.Thread(target=recibirComandos)
x.start()


#Se inicializa la ventana
ventana.mainloop()



