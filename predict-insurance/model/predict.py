import pickle
import pandas as pd

MODEL_VERSION = '1.0.0'

with open("model/model.pkl", 'rb') as f:
    model = pickle.load(f)


# def predict_ouptut(user_input: dict):
#     input_df = pd.DataFrame([user_input])

#     output = model.predict(input_df)[0]

#     return output

class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    df = pd.DataFrame([user_input])

    predicted_class = model.predict(df)[0]
    
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    class_probs = dict(zip(class_labels, map(lambda x: round(x, 4), probabilities)))

    return {
        'predicted_category': predicted_class,
        'confidence': round(confidence, 4),
        'class_probabilities': class_probs
    }