
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd

from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import model, predict_output, MODEL_VERSION

app = FastAPI()

@app.get('/')
def home():
    return {'message': "Insurance Premium Prediction API"}

@app.get("/health")
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None

    }

@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    user_input = {
            'bmi': data.bmi,
            'lifestyle_risk': data.lifestyle_risk,
            'age_group': data.age_group,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={
        'response': prediction})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={
            'error': str(e),
            'message': 'An error occurred while processing your request.'
        })


 