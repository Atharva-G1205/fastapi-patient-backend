from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description="the predicted insurance premium category",
        examples=["High"]
    )
    confidence: float = Field(
        ...,
        description="model's confidence score for the predicted class (range: 0 - 1)",
        examples=[0.343]
    )
    class_probabilities: dict[str, float] = Field(
        ...,
        description="probability distribution across all possible classes",
        examples=[{"low": 0.34, "medium": 0.53, "high": 0.13}]
    )
