from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int, Field(...,gt=0, le=120, description="age of the user", examples=[30])]
    weight: Annotated[float, Field(...,gt=0, description="weight of the user in kg", examples=[65])]
    height: Annotated[float, Field(...,gt=0, description="height of the user in metres", examples=[1.8])]
    income_lpa: Annotated[float, Field(..., gt=0, description="annual salary in LPA")]
    smoker: Annotated[bool, Field(..., description='is user a smoker?')]
    city: Annotated[str, Field(..., description='residing city?', examples=['Pune'])]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description='occupation of the user')]

    # improvement 2: using field_validator to normalize city names
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        return v.strip().title()

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
          
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3