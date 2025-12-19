# Usar imagen base de Python oficial
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . .

# Exponer el puerto (Cloud Run usa el 8080 por defecto)
ENV PORT=8080
EXPOSE 8080

# Comando para iniciar la app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
