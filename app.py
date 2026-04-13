import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Real Estate Predictor", layout="centered")

# 🔥 Premium UI CSS
st.markdown("""
<style>

/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #e5e7eb;
}

/* Title */
h1 {
    text-align: center;
    font-weight: 600;
    color: #f1f5f9;
}

/* Subtitle */
.stInfo {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    color: #cbd5f5;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

/* Labels */
label {
    color: #cbd5f5 !important;
}

/* Inputs */
input, select {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
}

/* Button */
div.stButton > button {
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    border-radius: 10px;
    color: white;
    height: 45px;
    font-size: 16px;
    border: none;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #43e97b, #38f9d7);
    color: black;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Success */
.stSuccess {
    background: rgba(34,197,94,0.2);
    color: #bbf7d0;
}

/* Divider */
hr {
    border: 0.5px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Real Estate Price Predictor</h1>", unsafe_allow_html=True)
st.info("✨ Enter property details to get an AI-powered estimate")

st.markdown("---")

# Input Card
st.markdown('<div class="card"><h3>Property Details</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Property Area (sq ft)", 300, 10000, 1200)
    bhk = st.selectbox("BHK", [1,2,3,4,5,6])

with col2:
    bath = st.selectbox("Bathrooms", [1,2,3,4,5])
    balcony = st.selectbox("Balcony", [0,1,2,3,4,5])

location = st.selectbox("Location", 
    ["Whitefield", "Electronic City", "Indiranagar", "Koramangala"])

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Prediction
if st.button("Predict Price"):
    with st.spinner("Analyzing..."):

        input_data = pd.DataFrame({
            'total_sqft': [area],
            'bath': [bath],
            'bhk': [bhk],
            'location': [location]
        })

        predicted_value = model.predict(input_data)[0]

        inr_value = predicted_value * 100000
        lower = inr_value * 0.9
        upper = inr_value * 1.1
        price_per_sqft = inr_value / area

        st.success("Prediction Ready")

        st.markdown('<div class="card"><h3>Results</h3>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Price", f"₹{int(inr_value):,}")
        with c2:
            st.metric("Min", f"₹{int(lower):,}")
        with c3:
            st.metric("Max", f"₹{int(upper):,}")

        st.success(f"₹{int(price_per_sqft):,} per sqft")

        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("✨ Built with ML + Streamlit")