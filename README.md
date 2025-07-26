# BMI Meal Recommender API

A FastAPI-powered backend that provides personalized meal recommendations based on a user's profile, BMI, and fitness goal (cutting, bulking, maintenance). It integrates with OpenAI via LangChain to generate intelligent diet plans.

## Features

- 🔐 Secure user authentication with JWT
- 📄 Profile creation with BMI calculation
- 🤖 AI-generated meal plans using OpenAI (LangChain)
- 🛠️ Modular project structure with SQLAlchemy ORM
- 🌐 CORS-enabled API for frontend integration

## Tech Stack

- FastAPI
- SQLAlchemy + MySQL
- LangChain + OpenAI
- JWT (via python-jose)
- Pydantic
- Passlib (bcrypt)

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/bmi-meal-recommender.git
   cd bmi-meal-recommender
