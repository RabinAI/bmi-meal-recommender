from langchain_community.chat_models import ChatOpenAI
from config import OPENAI_API_KEY

def generate_meal_plan(profile):
    llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
    prompt = f"""
    Recommend a meal plan for a person with the following details:
    Age: {profile.age},
    Height: {profile.height_cm} cm,
    Weight: {profile.weight_kg} kg,
    BMI: {profile.bmi},
    Goal: {profile.goal}
    """
    return llm.predict(prompt)
