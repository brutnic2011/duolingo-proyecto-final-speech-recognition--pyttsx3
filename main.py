#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyttsx3",
# ]
# ///

"""pyttsx3 examples."""

import speech_recognition as sr
import pyttsx3
import random
import time

# SINTESIS DE VOZ (pyttsx3)

engine = pyttsx3.init()  # creación de objetos

# VELOCIDAD / RATE
rate = engine.getProperty("rate")  # obtener detalles de la tasa de habla actual
print(rate)  # imprimir la tarifa de voz actual
engine.setProperty("rate", 160)  # Configurando una nueva velocidad de voz

# VOLUMEN / VOLUME
volume = engine.getProperty("volume")  # Conocer el nivel de volumen actual (mín.=0 y máx.=1)
print(volume)  # imprimiendo el nivel de volumen actual
engine.setProperty("volume", 0.5)  # Ajustar el nivel de volumen entre 0 y 1

# VOZ / VOICE
voices = engine.getProperty("voices")  # obtener detalles de la voz actual
# engine.setProperty('voice', voices[0].id)  # Al cambiar el índice, cambian las voces. (0 para masculino)
engine.setProperty("voice", voices[0].id)  # Al cambiar el índice, cambian las voces. (1 para mujer)

# TONO / PITCH
pitch = engine.getProperty("pitch")  # Obtener el valor de tono actual
print(pitch)  # Imprimir el valor de tono actual
engine.setProperty("pitch", 100)  # Ajusta el tono (por defecto 50) a 75 de 100.


# SPEECH RECOGNITION (speech_recognition)


# Definir las palabras por nivel de dificultad
niveles = {
    "bebe": ["and", "it", "the", "cat", "dog"],
    "facil": ["see", "jaw", "book", "tree", "house"],
    "medio": ["computer", "library", "developer", "python", "programming"],
    "dificil": ["artificial intelligence", "machine learning", "neural network",
                 "biological data science", "natural language processing"],
    "pesadilla": ["Mischievous Colonel adolescent", "Worcestershire sauce with mushrooms"
                  , "Otorhinolaryngologist in audiology",
                 "Indifferential quantum entanglement phenomenon",
                  "Pseudopseudohypoparathyroidism"]
}

# Inicializar el reconocedor
r = sr.Recognizer()

# Función para reconocer la palabra hablada
def reconocer_palabra():
    engine.say("escuchando, habla")
    engine.runAndWait()

    with sr.Microphone() as source:
        print("escuchando..., habla!!!")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2.5                         # más tolerancia al silencio
        audio = r.listen(source, phrase_time_limit=8)  # hasta 8 segundos de habla

    try:
        palabra_dicha = r.recognize_google(audio, language="en-US")
        print(f"Tu dijiste: {palabra_dicha}")
        engine.say("tu dijiste " + palabra_dicha)
        engine.runAndWait()
        return palabra_dicha.lower()
    
    except sr.UnknownValueError:
        print("no te entendí. intenta de nuevo.")
        engine.say("no te entendí. intenta de nuevo.")
        engine.runAndWait()
        return None
    
    except sr.RequestError as e:
        print(f"Error en el servicio de reconocimiento: {e}")
        engine.say("error en el servicio de reconocimiento")
        engine.runAndWait()
        return None

# --- Lógica del juego ---

puntos_racha = 0 # contador de racha de puntos

print("\n\n\nbienvenido al juego de reconocimiento de voz!\n")
engine.say("bienvenido al juego de reconocimiento de voz")
engine.runAndWait()

while True:
    nivel = input("\nelige una dificultad: bebe, facil, medio, dificil, o pesadilla \n(ingresa 'no' para cerrar el programa o 'ajustes' para cambiar la voz): ").lower()
    # engine.say("elige una dificultad: bebe, facil, medio, dificil, o pesadilla")

    if nivel == "ajustes":
        print("\n--- ajustes de voz ---")
        print("1. cambiar velocidad")
        print("2. cambiar volumen")
        print("3. cambiar voz (masculina/femenina)")
        opcion = input("elige una opción (1-3) o ingresa salir para volver al juego: ")

        if opcion == "1":
            nueva_velocidad = int(input("ingresa la nueva velocidad (50-300): "))
            engine.setProperty("rate", nueva_velocidad)
            print(f"velocidad cambiada a {nueva_velocidad}")
        elif opcion == "2":
            nuevo_volumen = float(input("ingresa el nuevo volumen (0.0-1.0): "))
            engine.setProperty("volume", nuevo_volumen)
            print(f"volumen cambiado a {nuevo_volumen}")
        elif opcion == "3":
            voz_opcion = input("elige voz masculina (m) o femenina (f): ").lower()
            if voz_opcion == "m":
                engine.setProperty("voice", voices[0].id)
                print("voz cambiada a masculina")
            elif voz_opcion == "f":
                engine.setProperty("voice", voices[1].id)
                print("voz cambiada a femenina")
            else:
                print("opción de voz no válida")
        elif opcion.lower() == "salir":
            continue
        else:
            print("opción no válida")
        continue

    elif nivel == "no":
        print("gracias por jugar! hasta luego!")
        engine.say("gracias por jugar! hasta luego!")
        engine.runAndWait()
        break
    elif nivel not in niveles:
        print("el nivel no es válido. Por favor, escribe los valores correctos")
        engine.say("el nivel no es válido. Por favor, escribe los valores correctos")
    else:
        palabra_objetivo = random.choice(niveles[nivel])
        print(f"tu palabra es: '{palabra_objetivo}'")
        engine.say(f"tu palabra es: {palabra_objetivo}")
        engine.runAndWait()
        time.sleep(2)
        palabra_usuario = reconocer_palabra()

        if palabra_usuario:
            if palabra_usuario == palabra_objetivo.lower():
                print("Correcto!")
                engine.say("Correcto!")
                puntos_racha += 1
                print(f"tu racha de puntos es: {puntos_racha}")
                time.sleep(1)
                engine.say(f"tu racha de puntos es: {puntos_racha}")
            else:
                print(f"dijiste '{palabra_usuario}', pero la palabra correcta es '{palabra_objetivo}'.")
                engine.say(f"dijiste {palabra_usuario}, pero la palabra correcta es {palabra_objetivo}.")
                puntos_racha = 0
                print(f"tu racha se ha reiniciado a: {puntos_racha}")
                time.sleep(1)
                engine.say(f"tu racha se ha reiniciado a: {puntos_racha}")