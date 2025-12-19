# Usa una versión ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requerimientos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . .

# El puerto por defecto en Cloud Run es 8080
ENV PORT 8080

# El comando de inicio (Exactamente como en tu imagen, pero en formato Docker)
# Nota: backend.main:app asume que tienes una carpeta 'backend' y dentro 'main.py'
CMD exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT