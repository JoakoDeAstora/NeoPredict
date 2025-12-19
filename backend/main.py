from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="NeoPredict API",
    description="Financial Prediction System for IPSA Market",
    version="1.0.0"
)

app.include_router(endpoints.router)

@app.get("/")
async def root():
    return {"message": "NeoPredict System Online", "status": "active"}

if __name__ == "__main__":
    import uvicorn
    # Start Scheduler
    from app.services.updater import UpdaterService
    updater = UpdaterService()
    updater.start()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
