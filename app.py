import streamlit as st
import pickle
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="SL House Predictor Pro", page_icon="🏠", layout="wide")

# 2. Sidebar Navigation
page = st.sidebar.selectbox("Go to", ["🏠 Home", "📊 Price Predictor"])

# --- PAGE 1: HOME PAGE ---
if page == "🏠 Home":
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
            background-position: center;
        }
        .home-box {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin-top: 100px;
        }
        </style>
        <div class="home-box">
            <h1> Smart House Price Predictor</h1>
            <p style='font-size: 20px;'>Estimate the price of your dream home in Sri Lanka today.</p>
            <p>Go to the Predictor page from the sidebar and enter the details..</p>
        </div>
        """, unsafe_allow_html=True)

# --- PAGE 2: PRICE ESTIMATION PAGE ---
elif page == "📊 Price Predictor":
    st.markdown("""
        <style>
	label {
    color: #1E3A8A !important; /* තද නිල් පාට */
    font-weight: bold !important;
    font-size: 16px !important;
	}
	div.stButton > button:first-child {
    background-color: #1E3A8A !important;
    color: white !important;
    border-radius: 8px !important;
    width: 100% !important; /* Button එක දිගටම පේන්න */
    font-size: 18px !important;
	}
        .stApp { background-color: #f0f2f6 !important; }
        .main-title { color: #0E1117 !important; font-size: 45px !important; font-weight: 800 !important; text-align: center; margin-bottom: 5px; }
        .sub-text { color: #31333F !important; font-size: 20px !important; text-align: center; margin-bottom: 30px; }

        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">📊 Estimate Your House Price</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Please enter your household details below.</p>', unsafe_allow_html=True)
    st.divider()

    try:
        model = pickle.load(open('house_model.pkl', 'rb'))
        columns = pickle.load(open('columns.pkl', 'rb'))
        
        # Inputs
        col1, col2 = st.columns(2)
        with col1:
            size = st.number_input("Square Feet:", min_value=500, value=1500, step=50)
        with col2:
            bedrooms = st.selectbox("Bedrooms:", [1, 2, 3, 4, 5, 6])

        city_list = [col.replace('City_', '') for col in columns if col.startswith('City_')]
        city = st.selectbox("Select city:", city_list)

        # Dynamic Image Selection
        city_images = {
            "Colombo": r"C:/Users/Kushini Kasunthara/Downloads/House Price App/colombo.jpg",
            "Kandy": r"C:/Users/Kushini Kasunthara/Downloads/House Price App/kandy.jpg",
            "Galle": r"C:/Users/Kushini Kasunthara/Downloads/House Price App/galle.webp",
	    "Gampaha": r"C:/Users/Kushini Kasunthara/Downloads/House Price App/Gampaha.webp",
	    "Kurunagala": r"C:/Users/Kushini Kasunthara/Downloads/House Price App/kuru.jpg"}

        if city in city_images:
            st.image(city_images[city], caption=f"Beautiful {city}", width=400)
        else:
            st.image("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80", use_container_width=True)

        st.write("") 

        if st.button("Calculate Price"):
            input_vector = np.zeros(len(columns))
            input_vector[0] = size
            input_vector[1] = bedrooms
            
            city_col = 'City_' + city
            if city_col in columns:
                idx = columns.index(city_col)
                input_vector[idx] = 1
                
            prediction = model.predict([input_vector])[0]
            st.balloons()
            st.success(f"## 💰 Estimated Price: Rs. {prediction:,.2f}")
            
    except Exception as e:
        st.error(f"Error loading model: {e}")