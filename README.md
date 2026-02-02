# HW7-TravelGuide-AI-Project
The Travel Guide AI App is a Python-based application that helps users plan personalized travel itineraries using AI-assisted workflows.
# 🌍 Travel Guide AI App
**Author:** Azhar Soomro

## 📌 Purpose
The Travel Guide AI App is a Python-based application that helps users plan
personalized travel itineraries using AI-assisted workflows.

The project solves the problem of manual travel planning by automatically
generating:
- Day-by-day itineraries
- Morning, afternoon, and evening schedules
- Hotel and restaurant recommendations
- Cost estimations
- AI-powered travel assistance

This project demonstrates how AI models can be integrated into real-world
applications to enhance user experience and decision-making.

---

## 🤖 AI & Technology Used
- **Python**
- **Streamlit** for the web interface
- **OpenAI API** for AI-generated itineraries and chat assistance
- **ReportLab** for PDF generation

AI is used to:
- Generate intelligent travel plans based on user preferences
- Answer follow-up questions using an embedded AI travel assistant

---

## ⚙️ What the Code Does (High-Level)
- Collects user input such as destination cities, number of days, interests,
  and accessibility preferences
- Uses an AI model to generate a detailed travel itinerary
- Displays the plan in a clean web interface
- Generates a downloadable PDF version of the travel plan
- Provides mock live hotel and flight pricing
- Allows users to save trips and share itineraries
- Includes an AI chat assistant for itinerary-related questions

---

## ▶️ How to Run the Project

### 1. Install dependencies
```bash
pip install -r requirements.txt

streamlit run Travel_Guide.py

