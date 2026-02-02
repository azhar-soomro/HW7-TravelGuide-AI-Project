import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import openai
import json
import os
import uuid

# ================= CONFIG =================
st.set_page_config(page_title="Travel Guide", layout="wide")
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
DATA_FILE = "saved_trips.json"
SHARE_FILE = "shared_trips.json"

# ================= DATA HELPERS =================
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ================= AI CORE =================
def generate_plan_chatgpt(cities, days, interests, guardrails, language):
    prompt = f"""
You are an expert travel planner.

Language: {language}
Cities: {', '.join(cities)}
Total days: {days}

Interests: {', '.join(interests) if interests else 'General sightseeing'}
Constraints: {', '.join(guardrails) if guardrails else 'None'}

Generate a detailed itinerary with:
- City-wise and day-wise breakdown
- Morning, Afternoon, Evening schedule
- Top-rated attractions with reviews
- Hotel & restaurant recommendations
- Estimated daily cost in USD

Format cleanly.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def ai_chat(question, itinerary):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": f"Itinerary:\n{itinerary}\n\nQuestion: {question}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

# ================= LIVE PRICING (API-READY MOCK) =================
def get_live_hotel_prices(city):
    return [
        {"name": "Hotel Central", "price": "$150/night"},
        {"name": "City View Inn", "price": "$110/night"},
        {"name": "Luxury Grand", "price": "$260/night"},
    ]


def get_live_flight_prices(city):
    return [
        {"route": f"NYC → {city}", "price": "$520"},
        {"route": f"LAX → {city}", "price": "$610"},
    ]

# ================= PDF =================
def generate_pdf(text, title):
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles['Title']), Spacer(1, 12)]
    for line in text.split("\n"):
        elements.append(Paragraph(line, styles['Normal']))
        elements.append(Spacer(1, 6))
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    SimpleDocTemplate(temp.name).build(elements)
    return temp.name

# ================= UI =================
st.title("🌍 Travel Guide")
st.caption("AI Travel Planner • Live Pricing • Collaboration • Assistant")

# ---------- USER ----------
st.sidebar.header("User")
username = st.sidebar.text_input("Username")

# ---------- LANGUAGE ----------
language = st.sidebar.selectbox("Language", ["English", "Spanish", "French", "German", "Hindi"])

# ---------- TRIP DETAILS ----------
cities_input = st.sidebar.text_input("Cities (comma separated)")
days = st.sidebar.number_input("Total Days", min_value=1, max_value=90, value=5)

interests = st.sidebar.multiselect(
    "Interests",
    ["Museums", "Food & Cuisine", "Historic Sites", "Nightlife", "Nature", "Shopping"]
)

guardrails = st.sidebar.multiselect(
    "Guardrails",
    ["No walking tours", "Kids friendly", "Wheelchair accessible", "No nightlife"]
)

col1, col2 = st.sidebar.columns(2)

# ---------- RESET ----------
if col2.button("Reset Form"):
    st.session_state.clear()
    st.experimental_rerun()

# ---------- GENERATE ----------
if col1.button("Generate Travel Plan"):
    if not username or not cities_input:
        st.warning("Username and cities required")
    else:
        cities = [c.strip() for c in cities_input.split(",")]
        with st.spinner("Generating AI itinerary..."):
            itinerary = generate_plan_chatgpt(cities, days, interests, guardrails, language)

        # Save trip
        trips = load_json(DATA_FILE)
        trips.setdefault(username, []).append({"id": str(uuid.uuid4()), "cities": cities, "itinerary": itinerary})
        save_json(DATA_FILE, trips)

        st.subheader("✈️ Itinerary")
        st.markdown(itinerary)

        # Live pricing
        st.subheader("💰 Live Pricing (Sample)")
        for city in cities:
            st.markdown(f"**{city}**")
            st.write("Hotels:", get_live_hotel_prices(city))
            st.write("Flights:", get_live_flight_prices(city))

        # PDF
        pdf_path = generate_pdf(itinerary, "Travel Guide Itinerary")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download PDF", f, "Travel_Plan.pdf", "application/pdf")

        # Share link
        share_id = str(uuid.uuid4())
        shared = load_json(SHARE_FILE)
        shared[share_id] = itinerary
        save_json(SHARE_FILE, shared)
        st.success(f"Shareable Trip ID: {share_id}")

# ---------- AI CHAT ----------
st.markdown("---")
st.subheader("🤖 Ask the AI Assistant")
question = st.text_input("Ask about your itinerary")

user_trips = load_json(DATA_FILE).get(username, [])
if question and user_trips:
    answer = ai_chat(question, user_trips[-1]['itinerary'])
    st.write(answer)

st.caption("Live Pricing • Trip Sharing • AI Assistant • Production-ready Architecture")

