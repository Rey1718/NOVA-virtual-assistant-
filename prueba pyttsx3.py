import pyttsx3

engine = pyttsx3.init()

engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('rate', 150)  # velocidad normal
engine.setProperty('volume', 1.0)  # máximo volumen

engine.say("Hola, esta es una prueba de voz")
engine.runAndWait()
