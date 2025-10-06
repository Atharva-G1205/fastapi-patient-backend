# Combined Patient Management API

This FastAPI application combines all the functionality from folders 1-5 into a comprehensive patient management system.

## Features Combined

### From Folder 1 (Demo)
- Basic hello world endpoints
- Simple FastAPI application structure

### From Folder 2 (Patients)
- Patient data viewing functionality
- JSON file-based data storage
- Patient sorting and filtering

### From Folder 3 (Pydantic)
- Various Pydantic model examples
- Field validation
- Model validation
- Computed fields
- Nested models
- Serialization examples

### From Folder 4 (Post Request)
- Patient creation functionality
- POST endpoint with validation
- Pydantic model integration

### From Folder 5 (Update Delete)
- Patient update functionality (PUT)
- Patient deletion functionality (DELETE)
- Partial updates with PatientUpdate model

## API Endpoints

### Basic Routes
- `GET /` - Hello world
- `GET /about` - API information
- `GET /health` - Health check

### Patient Management
- `GET /patients` - Get all patients
- `GET /patients/{patient_id}` - Get specific patient
- `GET /patients/sort/by` - Sort patients by field
- `POST /patients` - Create new patient
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient

## Models

### Main Patient Model
```python
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int (1-120)
    gender: Literal['male', 'female', 'others']
    height: float (in meters)
    weight: float (in kg)
    
    # Computed fields
    bmi: float (calculated)
    verdict: str (underweight/normal/overweight/obese)
```

### Update Model
```python
class PatientUpdate(BaseModel):
    name: Optional[str]
    city: Optional[str]
    age: Optional[int]
    gender: Optional[Literal['male', 'female', 'others']]
    height: Optional[float]
    weight: Optional[float]
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Data Storage

Patient data is stored in `patients.json` file with the following structure:

```json
{
  "P001": {
    "name": "Alice Johnson",
    "city": "New York",
    "age": 34,
    "gender": "Female",
    "height": 1.65,
    "weight": 68,
    "bmi": 24.98,
    "verdict": "Normal"
  }
}
```

## Features

1. **CRUD Operations**: Complete Create, Read, Update, Delete functionality
2. **Data Validation**: Comprehensive validation using Pydantic models
3. **Computed Fields**: Automatic BMI calculation and health verdict
4. **Sorting**: Sort patients by height, weight, or BMI
5. **Error Handling**: Proper HTTP status codes and error messages
6. **API Documentation**: Auto-generated OpenAPI documentation

## Additional Models

The `models.py` file contains additional Pydantic model examples from the pydantic folder:
- BasicPatient
- DetailedPatient
- PatientWithValidation
- NestedPatient
- PatientSummary

These demonstrate various Pydantic features like field validation, model validation, nested models, and serialization.