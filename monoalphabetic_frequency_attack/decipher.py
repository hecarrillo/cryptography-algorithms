import string
import random

# Este diccionario debe ser llenado con las frecuencias de las letras del inglés obtenidas de la imagen.
# Las llaves son las letras en mayúsculas y los valores son las frecuencias en porcentaje.
frecuencias_ingles = {
    'E': 11.1607, 'T': 9.056, 'A': 8.4966, 'O': 7.1635,
    'I': 7.5448, 'N': 6.6544, 'S': 5.7351, 'H': 3.0034,
    'R': 7.5809, 'D': 3.3844, 'L': 5.4893, 'C': 4.5388,
    'U': 3.6308, 'M': 3.0129, 'W': 1.2899, 'F': 1.8121,
    'G': 2.4705, 'Y': 1.7779, 'P': 3.1671, 'B': 2.0720,
    'V': 1.0074, 'K': 1.1016, 'X': 0.2902, 'Q': 0.1962,
    'J': 0.1965, 'Z': 0.2722
}

# Ordenar las letras por frecuencia en inglés
frecuencias_ingles_ordenadas = sorted(frecuencias_ingles, key=frecuencias_ingles.get, reverse=True)

def leer_texto_cifrado(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        # convertir a mayusculas
        texto_cifrado = archivo.read().upper()
    return texto_cifrado
def analizar_frecuencia(texto_cifrado):
    # Contar la frecuencia de cada letra en el texto cifrado
    frecuencias_cifrado = {letra: 0 for letra in string.ascii_uppercase}
    for caracter in texto_cifrado:
        if caracter.upper() in frecuencias_cifrado:
            frecuencias_cifrado[caracter.upper()] += 1
    
    total_caracteres = sum(frecuencias_cifrado.values())
    frecuencias_cifrado = {letra: (frecuencia / total_caracteres) * 100 for letra, frecuencia in frecuencias_cifrado.items()}
    
    # Ordenar las letras del texto cifrado por frecuencia
    return sorted(frecuencias_cifrado, key=frecuencias_cifrado.get, reverse=True)

def descifrar_texto(texto_cifrado, frecuencias_cifrado_ordenadas, letras_adivinadas_correctamente):
    texto_descifrado = ''
    letras_disponibles = list(set(frecuencias_ingles_ordenadas) - set(letras_adivinadas_correctamente.values()))

    for i, caracter in enumerate(texto_cifrado):
        if caracter.upper() in letras_adivinadas_correctamente:
            texto_descifrado += letras_adivinadas_correctamente[caracter.upper()]
        elif caracter.upper() in string.ascii_uppercase:
            # Hacer la primera suposición basada en la frecuencia si no se ha adivinado aún
            if caracter.upper() not in letras_adivinadas_correctamente:
                if letras_disponibles:
                    indice = frecuencias_cifrado_ordenadas.index(caracter.upper())
                    texto_descifrado += frecuencias_ingles_ordenadas[indice] if indice < len(frecuencias_ingles_ordenadas) else caracter
                else:
                    texto_descifrado += caracter
            else:
                texto_descifrado += caracter
        else:
            texto_descifrado += caracter

    return texto_descifrado

ruta_archivo_cifrado = 'ciphered_text.txt'
texto_cifrado = leer_texto_cifrado(ruta_archivo_cifrado)
frecuencias_cifrado_ordenadas = analizar_frecuencia(texto_cifrado)
texto_descifrado = ''
letras_adivinadas_correctamente = {}
while True:
    texto_descifrado = descifrar_texto(texto_cifrado, frecuencias_cifrado_ordenadas, letras_adivinadas_correctamente)

    # Mostrar el texto descifrado al usuario y preguntar caracteres adivinados
    print(texto_descifrado[:1000])
    caracteres_adivinados = input('Ingrese los caracteres correctos que identificó o escribe TERMINAR si el texto es el correcto: ')
    
    if caracteres_adivinados.lower() == 'terminar':
        break

    # Actualizar el diccionario con las letras adivinadas correctamente
    for caracter in caracteres_adivinados.upper():
        if caracter in string.ascii_uppercase:  # Asegurarse de que es una letra
            for i, c in enumerate(texto_descifrado):
                if texto_cifrado[i].upper() == caracter:
                    letras_adivinadas_correctamente[texto_cifrado[i].upper()] = c
                    break

# Guardar el texto descifrado en un archivo
with open('texto_descifrado.txt', 'w', encoding='utf-8') as archivo_salida:
    archivo_salida.write(texto_descifrado)

print("El texto ha sido descifrado y guardado en 'texto_descifrado.txt'")
