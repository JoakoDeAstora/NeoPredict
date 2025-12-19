from fastapi import FastAPI
from app.api import endpoints
# 1. Importa tu servicio aquí arriba
from app.services.updater import UpdaterService 

app = FastAPI(
    title="NeoPredict API",
    description="Financial Prediction System for IPSA Market",
    version="1.0.0"
)

app.include_router(endpoints.router)

@app.get("/")
async def root():
    return {"message": "NeoPredict System Online", "status": "active"}

# ---------------------------------------------------------
# 2. NUEVO ENDPOINT: Esto es lo que Cloud Scheduler llamará
# ---------------------------------------------------------
@app.post("/trigger-update")
async def trigger_update_process():
    """
    Este endpoint es gatillado por Google Cloud Scheduler.
    Ejecuta el ciclo de actualización una vez y termina.
    """
    print("Iniciando actualización solicitada por Cloud Scheduler...")
    
    updater = UpdaterService()
    
    # Aquí llamamos a la función que hace el trabajo (NO a .start())
    # Asumo que tu clase UpdaterService tiene un método 'run_update_cycle'.
    # Si se llama diferente, cambia el nombre aquí.
    await updater.run_update_cycle()
    
    return {"status": "Update executed successfully"}

# ---------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    # NOTA: En Google Cloud, esta sección NO se ejecuta automáticamente
    # para el Scheduler. Solo sirve si lo corres en tu PC.
    
    # Para pruebas locales puedes dejar esto, pero en producción
    # quien manda es el endpoint /trigger-update
    uvicorn.run(app, host="0.0.0.0", port=8000)
