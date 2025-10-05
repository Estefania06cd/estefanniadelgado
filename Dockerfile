# 1. IMAGEN BASE: Define la versión de Python a usar.
FROM python:3.10-slim-buster

# 2. DIRECTORIO DE TRABAJO: Crea y establece la carpeta principal dentro del contenedor.
WORKDIR /app

# 3. INSTALAR DEPENDENCIAS: Copia el archivo requirements.txt e instala las librerías.
# Esto es más rápido y eficiente.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. COPIAR CÓDIGO: Copia el resto de tu proyecto (app.py, templates/, static/) al contenedor.
COPY . .

# 5. PUERTO: Informa al mundo que el contenedor escucha en el puerto 8080.
# Render a menudo lo ignora y usa su propio puerto, pero es una buena práctica.
EXPOSE 8080

# 6. COMANDO DE INICIO: Define cómo se inicia la aplicación.
# Se usa Gunicorn, el servidor de producción, enlazando la IP 0.0.0.0 y el puerto 8080.
# app:app significa: 'app.py' (archivo) : 'app' (variable Flask dentro del archivo)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]