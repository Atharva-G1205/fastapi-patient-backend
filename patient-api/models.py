"""
Pydantic Models for Patient Management API
Combines various model examples from the pydantic folder
"""

from pydantic import BaseModel, Field, EmailStr, computed_field, field_validator, model_validator
from typing import Annotated, Optional, List, Dict, Any, Literal
from datetime import datetime


class BasicPatient(BaseModel):
    """Basic patient model (from 1_pydantic_model.py)"""
    name: str
    age: int
    weight: float


class DetailedPatient(BaseModel):
    """Detailed patient model with computed fields (from 4_computed_fields.py)"""
    name: str
    email: EmailStr
    age: int
    height: float 
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI"""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi


class PatientWithValidation(BaseModel):
    """Patient model with field validation (from 2_field_validator_and_modules.py)"""
    name: Annotated[str, Field(min_length=2, max_length=100)]
    age: Annotated[int, Field(ge=0, le=120)]
    email: EmailStr
    height: Annotated[float, Field(gt=0, le=3.0)]  # in meters
    weight: Annotated[float, Field(gt=0, le=500)]  # in kg
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate name contains only letters and spaces"""
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v.title()
    
    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, v):
        """Validate email domain"""
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
        domain = v.split('@')[1].lower()
        if domain not in allowed_domains:
            raise ValueError(f'Email domain must be one of: {allowed_domains}')
        return v


class Address(BaseModel):
    """Address model for nested patient data"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "India"


class EmergencyContact(BaseModel):
    """Emergency contact model"""
    name: str
    relationship: str
    phone: str
    email: Optional[EmailStr] = None


class NestedPatient(BaseModel):
    """Patient model with nested data structures (from 5_nested_models.py)"""
    id: str
    name: str
    age: int
    email: EmailStr
    address: Address
    emergency_contacts: List[EmergencyContact]
    medical_history: Dict[str, Any]
    
    @model_validator(mode='after')
    def validate_emergency_contacts(self):
        """Ensure at least one emergency contact"""
        if len(self.emergency_contacts) == 0:
            raise ValueError('At least one emergency contact is required')
        return self


class PatientSummary(BaseModel):
    """Patient summary for serialization (from 6_serialization.py)"""
    id: str
    name: str
    age: int
    bmi: float
    status: Literal['active', 'inactive', 'discharged']
    last_visit: datetime
    
    class Config:
        """Pydantic configuration"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Example usage functions
def create_basic_patient(name: str, age: int, weight: float) -> BasicPatient:
    """Create a basic patient instance"""
    return BasicPatient(name=name, age=age, weight=weight)


def create_detailed_patient(patient_data: dict) -> DetailedPatient:
    """Create a detailed patient instance"""
    return DetailedPatient(**patient_data)


def validate_patient_data(patient_data: dict) -> PatientWithValidation:
    """Validate patient data using the validation model"""
    return PatientWithValidation(**patient_data)


SAMPLE_PATIENT_DATA = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@gmail.com",
    "height": 1.75,
    "weight": 70.5,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "1234567890", "address": "123 Main St"}
}

SAMPLE_NESTED_PATIENT = {
    "id": "P999",
    "name": "Jane Smith",
    "age": 28,
    "email": "jane.smith@gmail.com",
    "address": {
        "street": "456 Oak Avenue",
        "city": "Mumbai",
        "state": "Maharashtra",
        "zip_code": "400001",
        "country": "India"
    },
    "emergency_contacts": [
        {
            "name": "John Smith",
            "relationship": "Spouse",
            "phone": "+91-9876543210",
            "email": "john.smith@gmail.com"
        }
    ],
    "medical_history": {
        "allergies": ["peanuts"],
        "chronic_conditions": [],
        "medications": ["vitamin_d"],
        "surgeries": []
    }
}