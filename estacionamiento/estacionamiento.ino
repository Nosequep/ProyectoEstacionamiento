// Incluímos la librería para poder controlar el servo
#include <Servo.h>
#include <NoDelay.h>
#include <NewPing.h>

const int PIN_PIR = 13;
const int PIN_SERVO = 9;
const int PIN_LED_PLUMA = 8;

//Pins led RGB
const int PIN_LED_ROJO = 12;
const int PIN_LED_VERDE = 10;
const int PIN_LED_AZUL = 11;

//Colores de led
const int RED = 0;
const int YELLOW = 1;
const int GREEN = 2;

// Use el siguiente arreglo si el diodo RGB es de Anodo comun
int componentesRGB_colores[][3] = {{LOW, HIGH, HIGH},
{LOW, LOW, HIGH},
{HIGH, LOW, HIGH}};

//Pins del sensor ultrasonico
const int PIN_TRIGGER = 3;
const int PIN_ECHO = 2;

//Distancias del sensor ultrasonico
const int DISTANCIA_MAX = 200;
const int DISTANCIA_ROJO = 5;
const int DISTANCIA_AMARILLO = 10;

// Crea una instancia de la clase NewPing
NewPing sonar(PIN_TRIGGER, PIN_ECHO, DISTANCIA_MAX);

// Estado anterior del PIR
int estadoAntPir = LOW; 

// Periodo en ms que dura encendido el pir
const long PERIODO_PIR = 5000;
// Periodo de sensor ultrasonico
const long PERIODO_DISTANCIA = 500;
// Crea una instancia de la clase noDelay
// que determina si han transcurrido PERIODO ms
noDelay pausa(PERIODO_PIR);
noDelay pausa2(PERIODO_DISTANCIA);

// Declaramos la variable para controlar el servo
Servo servoMotor;
//Estados del servo
int ESTADO_ABIERTO = 180;
int ESTADO_CERRADO = 90;

//Estado en el que se encuentra el servo
int estadoServo = ESTADO_CERRADO;

void setup() {
  pinMode(PIN_LED_ROJO, OUTPUT);
  pinMode(PIN_LED_VERDE, OUTPUT);
  pinMode(PIN_LED_AZUL, OUTPUT);
  pinMode(PIN_LED_PLUMA, OUTPUT);
  
  // Iniciamos el monitor serie para mostrar el resultado
  Serial.begin(9600);
  // Iniciamos el servo para que empiece a trabajar con el pin 9
  servoMotor.attach(PIN_SERVO);
}
 
void loop() {
  //Si transcurrido el tiempo de actualización del sensor ultrasonico
  if(pausa2.update()){
    //Se activa la alerta de proximidad
    alertaProximidad();  
  }

  // Si ha transcurrido el tiempo de actualización del sensor pir
  if (pausa.update()) {
    if(estadoServo == ESTADO_ABIERTO) {
      //Se cambia el estado del servo
      estadoServo = ESTADO_CERRADO;
      //Se cierra ele servomotor
      servoMotor.write(estadoServo);
      //Se enciende el led
      digitalWrite(PIN_LED_PLUMA, LOW);
    }
  }
  
  // Se lee el sensor de movimiento
  int valorPir = digitalRead(PIN_PIR);
  if (valorPir == HIGH) {
    //Serial.println("Se detecta movimiento");
    if (estadoServo == ESTADO_CERRADO){
      // Envia señal a relevador conectado al pin
      // PIN_RELEVADOR para que energice el LED
      estadoServo = ESTADO_ABIERTO;
      //Se abre el servomotor
      servoMotor.write(estadoServo);
      //Se enciende el led
      digitalWrite(PIN_LED_PLUMA, HIGH);
    }
    // Reinicia el contador de tiempo transcurrido a 0
    pausa.start();
  }
}

/*
* Esta función btiene la distancia entre el sensor ultrasónico
* HC-SR04 y el objeto en cm, usando la mediana de 5 pings y si
* la distancia es menor que DISTANCIA_ROJO, enciende el LED en rojo, si
* es menor a la DISTANCIA_AMARILLO, enciende el LED en amarillo,
* si es mayor a lo anterior, enciende el LED en elverde.
*/
void alertaProximidad() {
  // Obtiene la mediana de 5 mediciones del tiempo de viaje del
  // sonido entre el sensor y el objeto
  int uS = sonar.ping_median();
  // Calcular la distancia a la que se encuentra el objeto
  int distancia = sonar.convert_cm(uS);
  
  //Si la distancia es menor a DISTANCIA_ROJO, enciende el LED en rojo
  if (distancia <= DISTANCIA_ROJO){
    digitalWrite(PIN_LED_ROJO, componentesRGB_colores[RED][0]);
    digitalWrite(PIN_LED_VERDE, componentesRGB_colores[RED][1]);
    digitalWrite(PIN_LED_AZUL, componentesRGB_colores[RED][2]);
  //Si la distancia es menor a DISTANCIA_AMARILLO, enciende el LED en amarillo
  }else if (distancia <= DISTANCIA_AMARILLO){
    digitalWrite(PIN_LED_ROJO, componentesRGB_colores[YELLOW][0]);
    digitalWrite(PIN_LED_VERDE, componentesRGB_colores[YELLOW][1]);
    digitalWrite(PIN_LED_AZUL, componentesRGB_colores[YELLOW][2]);
  //Si es mayor a lo anterior, enciende el LED en verde
  }else{
    digitalWrite(PIN_LED_ROJO, componentesRGB_colores[GREEN][0]);
    digitalWrite(PIN_LED_VERDE, componentesRGB_colores[GREEN][1]);
    digitalWrite(PIN_LED_AZUL, componentesRGB_colores[GREEN][2]);
  } 
}
