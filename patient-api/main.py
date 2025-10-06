from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI(
    title="Combined Patient Management API",
    description="A comprehensive FastAPI application combining all patient management features",
    version="1.0.0"
)

def load_data():
    """Load patient data from JSON file"""
    try:
        with open('patients.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

def save_data(data):
    """Save patient data to JSON file"""
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

class Patient(BaseModel):
    """Complete Patient model with validation and computed fields"""
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P999'])]
    name: Annotated[str, Field(..., description='Name of the patient', examples=['John Doe'])]
    city: Annotated[str, Field(..., description='City of the patient', examples=['Pune'])]
    age: Annotated[int, Field(..., gt=0, le=120, description='Age of the patient', examples=[30])]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient', examples=['male'])]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in metres', examples=[1.7])]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kg', examples=[55])]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI based on height and weight"""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        """Determine health verdict based on BMI"""
        if self.bmi < 18.5:
            return "underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "normal"
        elif 25 <= self.bmi < 29.9:
            return "overweight"
        else:
            return "obese"

class PatientUpdate(BaseModel):
    """Model for partial patient updates"""
    name: Annotated[Optional[str], Field(default=None, description='Name of the patient')]
    city: Annotated[Optional[str], Field(default=None, description='City of the patient')]
    age: Annotated[Optional[int], Field(default=None, gt=0, le=120, description='Age of the patient')]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, description='Gender of the patient')]
    height: Annotated[Optional[float], Field(default=None, gt=0, description='Height of the patient in metres')]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description='Weight of the patient in kg')]


@app.get("/", tags=["Basic"])
def hello():
    """Basic hello endpoint"""
    return {'message': "Patient Management API"}

@app.get("/about", tags=["Basic"])
def about():
    """About endpoint with API information"""
    return {"message": "This is a FastAPI application for patient management."}

@app.get("/patients", tags=["Patients"])
def view_all_patients():
    """Get all patients data"""
    data = load_data()
    return data

@app.get("/patients/{patient_id}", tags=["Patients"])
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example="P001")):
    """Get specific patient by ID"""
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patients/sort/by", tags=["Patients"])
def sort_patients(
    sort_by: str = Query(None, description="Sort on the basis of height, weight or bmi"),
    order: str = Query('asc', description='Sort in asc or desc order')
):
    """Sort patients by specified field"""
    data = load_data()

    if sort_by is None:
        return data

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field, select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order, select from asc or desc")

    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/patients', tags=["Patients"])
def create_patient(patient: Patient):
    """Create a new patient"""
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)

    return JSONResponse(
        status_code=201, 
        content={"message": "Patient created successfully", "patient_id": patient.id}
    )

@app.put('/patients/{patient_id}', tags=["Patients"])
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """Update an existing patient"""
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient = data[patient_id]
    updated_patient = existing_patient.copy()
    
    for field, value in patient_update.model_dump(exclude_unset=True).items():
        if value is not None:
            updated_patient[field] = value
    
    updated_patient['id'] = patient_id
    validated_patient = Patient(**updated_patient)
    data[patient_id] = validated_patient.model_dump(exclude={'id'})

    save_data(data)

    return JSONResponse(
        status_code=200, 
        content={"message": "Patient updated successfully", "patient_id": patient_id}
    )

@app.delete('/patients/{patient_id}', tags=["Patients"])
def delete_patient(patient_id: str):
    """Delete a patient"""
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient does not exist")

    del data[patient_id]
    save_data(data)

    return JSONResponse(
        status_code=200, 
        content={'message': 'Patient info deleted successfully'}
    )

@app.get("/health", tags=["Basic"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Patient Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)