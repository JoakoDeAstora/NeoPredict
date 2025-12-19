from fastapi import APIRouter, HTTPException
from app.services import data_service

router = APIRouter()

@router.get("/market/{ticker}/history")
async def get_history(ticker: str):
    try:
        data = data_service.get_monthly_data(ticker)
        if not data:
             raise HTTPException(status_code=404, detail="Ticker not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/{ticker}/prediction")
async def get_prediction(ticker: str):
    try:
        data = data_service.get_prediction_data(ticker)
        return data
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
