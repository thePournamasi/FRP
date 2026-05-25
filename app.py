import difflib
import os
import json
import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import numpy as np
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

try:
    import requests
except ImportError:
    requests = None

from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array

# 2. LOAD YOUR AI MODELS ONCE
@st.cache_resource
def load_vision_model():
    return MobileNetV2(weights='imagenet')

@st.cache_resource
def load_rf_model():
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'obesity_rf_model.joblib')
    return joblib.load(model_path)

@st.cache_resource
def load_food_database():
    from food_data import LOCAL_FOOD_DATABASE, LOCAL_FOOD_ALIASES
    return LOCAL_FOOD_DATABASE, LOCAL_FOOD_ALIASES

# 1. PAGE SETUP
st.set_page_config(page_title="Obesity & Diet Tracker", layout="wide")

# Initialize session state
if 'total_calories' not in st.session_state:
    st.session_state['total_calories'] = 0
if 'obesity_level' not in st.session_state:
    st.session_state['obesity_level'] = None
if 'last_calories' not in st.session_state:
    st.session_state['last_calories'] = 0

# Show loading message while models load
with st.spinner("Loading AI models and data... This may take a moment on first run."):
    vision_model = load_vision_model()
    rf_model = load_rf_model()
    LOCAL_FOOD_DATABASE, LOCAL_FOOD_ALIASES = load_food_database()

st.title("🩺 Obesity Control and Diet Recommendation Website")

def normalize_food_name(label, use_aliases=False):
    normalized = label.strip().lower().replace(' ', '_').replace('-', '_')
    normalized = normalized.replace('__', '_')
    
    # Check direct database match first
    if normalized in LOCAL_FOOD_DATABASE:
        return normalized
    
    # Apply alias resolution
    if normalized in LOCAL_FOOD_ALIASES:
        aliased = LOCAL_FOOD_ALIASES[normalized]
        if aliased in LOCAL_FOOD_DATABASE:
            return aliased
    
    # Force alias resolution if indian_only mode
    if use_aliases:
        aliased = LOCAL_FOOD_ALIASES.get(normalized, normalized)
        if aliased in LOCAL_FOOD_DATABASE:
            return aliased
    
    return normalized

def find_similar_food(label, indian_only=False):
    # Normalize and get the base name
    normalized = label.strip().lower().replace(' ', '_').replace('-', '_').replace('__', '_')
    candidates = list(LOCAL_FOOD_DATABASE.keys())

    # Step 1: Check exact match in database
    if normalized in LOCAL_FOOD_DATABASE:
        return normalized

    # Step 2: Check if it's an alias
    if normalized in LOCAL_FOOD_ALIASES:
        aliased = LOCAL_FOOD_ALIASES[normalized]
        if aliased in LOCAL_FOOD_DATABASE:
            return aliased

    # Step 3: For Indian-only mode, try all possible aliases first
    if indian_only:
        for key, value in LOCAL_FOOD_ALIASES.items():
            if key in normalized or normalized in key:
                if value in LOCAL_FOOD_DATABASE:
                    return value
    
    # Step 4: Fuzzy match using difflib for misspellings and similar names
    close_matches = difflib.get_close_matches(normalized, candidates, n=1, cutoff=0.6)
    if close_matches:
        return close_matches[0]

    # Step 5: Partial match on token overlap
    tokens = normalized.split('_')
    for choice in candidates:
        if any(token for token in tokens if token and token in choice):
            return choice

    return None

def get_food_details(label, indian_only=False):
    # Normalize the label first
    normalized = label.strip().lower().replace(' ', '_').replace('-', '_').replace('__', '_')
    
    # Try to find in database using improved matching
    candidate = find_similar_food(normalized, indian_only=indian_only)
    
    if candidate:
        info = LOCAL_FOOD_DATABASE[candidate].copy()
        info['label'] = candidate.replace('_', ' ').title()
        info['source'] = 'Local database'
        return info

    # Fallback to API
    api_info = get_food_info_from_api(label, indian_only=indian_only)
    if api_info:
        api_info['source'] = 'API'
        return api_info

    return None

   


def parse_food_api_response(data):
    if not data:
        return None

    if 'hints' in data and data['hints']:
        food = data['hints'][0].get('food', {})
        nutrients = food.get('nutrients', {})
        return {
            'label': food.get('label', 'Unknown Food'),
            'calories': nutrients.get('ENERC_KCAL'),
            'protein': nutrients.get('PROCNT'),
            'carbs': nutrients.get('CHOCDF'),
            'fat': nutrients.get('FAT'),
            'description': food.get('category', 'Nutrition data from API')
        }

    if 'foods' in data and data['foods']:
        food = data['foods'][0]
        return {
            'label': food.get('food_name', 'Unknown Food'),
            'calories': food.get('nf_calories'),
            'protein': food.get('nf_protein'),
            'carbs': food.get('nf_total_carbohydrate'),
            'fat': food.get('nf_total_fat'),
            'description': food.get('brand_name', 'Nutrition data from API')
        }

    if 'items' in data and data['items']:
        food = data['items'][0]
        nutrients = food.get('nutrition', {}) or food.get('nutrients', {})
        return {
            'label': food.get('name', food.get('label', 'Unknown Food')),
            'calories': nutrients.get('calories') or nutrients.get('calories_kcal'),
            'protein': nutrients.get('protein'),
            'carbs': nutrients.get('carbohydrates') or nutrients.get('carbs'),
            'fat': nutrients.get('fat'),
            'description': food.get('description', 'Nutrition data from API')
        }

    if 'data' in data and isinstance(data['data'], list) and data['data']:
        food = data['data'][0]
        nutrients = food.get('nutrition', {}) or food.get('nutrients', {})
        return {
            'label': food.get('name', food.get('label', 'Unknown Food')),
            'calories': nutrients.get('calories') or nutrients.get('calories_kcal'),
            'protein': nutrients.get('protein'),
            'carbs': nutrients.get('carbohydrates') or nutrients.get('carbs'),
            'fat': nutrients.get('fat'),
            'description': food.get('description', 'Nutrition data from API')
        }

    return None


def get_indian_food_info_from_api(query):
    endpoint = os.getenv('INDIAN_FOOD_API_URL', '').strip()
    api_key = os.getenv('INDIAN_FOOD_API_KEY', '').strip()
    if not endpoint or requests is None:
        return None

    params = {'query': query}
    headers = {'Accept': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return parse_food_api_response(response.json())
    except Exception:
        return None

    return None


def get_food_info_from_api(query, indian_only=False):
    if requests is None:
        return None

    # Prioritize a configured Indian dish API when available
    indian_info = get_indian_food_info_from_api(query)
    if indian_info:
        return indian_info

    if indian_only:
        return None

    edamam_app_id = os.getenv('EDAMAM_APP_ID', '').strip()
    edamam_app_key = os.getenv('EDAMAM_APP_KEY', '').strip()
    if edamam_app_id and edamam_app_key:
        edamam_endpoint = 'https://api.edamam.com/api/food-database/v2/parser'
        params = {
            'app_id': edamam_app_id,
            'app_key': edamam_app_key,
            'ingr': query,
            'nutrition-type': 'logging'
        }
        try:
            response = requests.get(edamam_endpoint, params=params, timeout=10)
            if response.status_code == 200:
                return parse_food_api_response(response.json())
        except Exception:
            return None

    endpoint = os.getenv('FOOD_INFO_API_URL', '').strip()
    api_key = os.getenv('FOOD_INFO_API_KEY', '').strip()
    if endpoint and api_key:
        params = {'query': query}
        headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                return parse_food_api_response(response.json())
        except Exception:
            return None

    return None


def get_food_details(label, indian_only=False):
    normalized = normalize_food_name(label)
    candidate = find_similar_food(normalized)
    if candidate:
        info = LOCAL_FOOD_DATABASE[candidate].copy()
        info['label'] = candidate.replace('_', ' ').title()
        info['source'] = 'Local database'
        return info

    api_info = get_food_info_from_api(label, indian_only=indian_only)
    if api_info:
        api_info['source'] = 'API'
        return api_info

    return None

# 3. CREATE THE TABS
# This creates two clickable buttons at the top of your app
# Change this line at the top of your app:
tab1, tab2, tab3 = st.tabs(["📊 Obesity Predictor", "📸 Food Calorie Scanner", "💡 Health Recommendation"])
# ==========================================
# TAB 1: THE PREDICTOR
# ==========================================
with tab1:
    st.header("Step 1: Predict your current status")
    
    with st.sidebar:
        st.header("Enter Details")
        
        # Categorical Inputs
        sex = st.selectbox("Sex", ["Male", "Female"])
        overweight_family = st.selectbox("Overweight/Obese Family History?", ["Yes", "No"])
        fast_food = st.selectbox("Consumption of Fast Food?", ["Yes", "No"])
        veg_freq = st.selectbox("Frequency of Consuming Vegetables (0-2)", [0, 1, 2])
        between_meals = st.selectbox("Food Intake Between Meals (0-3)", [0, 1, 2, 3])
        smoking = st.selectbox("Smoking?", ["Yes", "No"])
        transport = st.selectbox("Type of Transportation Used", ["Automobile", "Public_Transportation", "Walking", "Bike"])
        
       # Numeric Inputs
        age = st.number_input("Age", min_value=0, value=25)
        
        # Ensuring the bottom line is 0 for valid data entry across all metrics
        weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)

        # --- HEIGHT CONVERTER ---
        height_mode = st.radio("Height Unit", ["Meters", "Centimeters", "Feet & Inches"], horizontal=True)

        if height_mode == "Meters":
            h_m = st.number_input("Height (m)", min_value=0.0, max_value=2.5, value=1.70)
            final_height_cm = h_m * 100
        
        elif height_mode == "Centimeters":
            final_height_cm = st.number_input("Height (cm)", min_value=0, max_value=250, value=170)
        
        else: # Feet & Inches
            col_ft, col_in = st.columns(2)
            ft = col_ft.number_input("Feet", min_value=0, max_value=8, value=5)
            inch = col_in.number_input("Inches", min_value=0, max_value=11, value=7)
            # Conversion: (Feet * 30.48) + (Inches * 2.54)
            final_height_cm = (ft * 30.48) + (inch * 2.54)
            st.caption(f"Calculated: {final_height_cm:.1f} cm")

        # --- BMI VISUALIZER ---
        if final_height_cm > 0:
            bmi = weight / ((final_height_cm / 100) ** 2)
            st.metric("Your Calculated BMI", f"{bmi:.1f}")

            if bmi < 18.5:
                bmi_category = "Insufficient_Weight"
            elif bmi < 25:
                bmi_category = "Normal_Weight"
            elif bmi < 30:
                bmi_category = "Overweight_Level_I"
            elif bmi < 35:
                bmi_category = "Overweight_Level_II"
            elif bmi < 40:
                bmi_category = "Obesity_Type_I"
            elif bmi < 45:
                bmi_category = "Obesity_Type_II"
            else:
                bmi_category = "Obesity_Type_III"

        st.info(f"📊 BMI Category: {bmi_category.replace('_',' ')}")
            
        meals = st.number_input("Number of Main Meals Daily", min_value=0, value=3)
        liquid_intake = st.number_input("Liquid Intake Daily (L)", min_value=0.0, value=2.0)
        phys_ex = st.number_input("Physical Excercise (0-3 scale)", min_value=0, max_value=3, value=1)
        tech_sch = st.number_input("Schedule Dedicated to Technology (hours)", min_value=0, value=2)

         # ===== ADDITION: HEALTH CONDITIONS =====
        st.markdown("---")
        st.subheader("⚕️ Health Conditions")

        allergies = st.multiselect("Allergies", ["Dairy","Nuts","Gluten","Seafood","Eggs"])
        gastric = st.checkbox("Gastric / Acid Reflux")
        ibs = st.checkbox("IBS")
        constipation = st.checkbox("Constipation")
        diabetes = st.checkbox("Diabetes")

        st.session_state['conditions'] = {
            "allergies": allergies,
            "gastric": gastric,
            "ibs": ibs,
            "constipation": constipation,
            "diabetes": diabetes
        }

    # The button logic
    if st.button("Predict Obesity Level"):
        # Restoring the correct 1 and 2 mapping logic so the AI routes correctly
        input_data = pd.DataFrame({
            'Sex': [2 if sex == 'Female' else 1],
            'Age': [age],
            'Height': [final_height_cm / 100],   
            'Weight': [weight],
            'Overweight_Obese_Family': [1 if overweight_family == 'Yes' else 2],
            'Consumption_of_Fast_Food': [1 if fast_food == 'Yes' else 2],
            'Frequency_of_Consuming_Vegetables': [veg_freq + 1], 
            'Number_of_Main_Meals_Daily': [meals],
            'Food_Intake_Between_Meals': [between_meals + 1],    
            'Smoking': [1 if smoking == 'Yes' else 2],
            'Liquid_Intake_Daily': [1 if liquid_intake < 1.0 else (2 if liquid_intake <= 2.0 else 3)],
            'Calculation_of_Calorie_Intake': [2],  
            'Physical_Excercise': [phys_ex + 1],                 
            'Schedule_Dedicated_to_Technology': [tech_sch],
            'Type_of_Transportation_Used': [4 if transport == "Walking" else (3 if transport == "Public_Transportation" else 1)]
        })
        
        # 1. Get the raw number from the AI
        raw_prediction = rf_model.predict(input_data)[0]
        
        # 2. Translate the number to English (Using the 4-class consolidation)
        target_mapping = {
            1: "Insufficient_Weight",
            2: "Normal_Weight",
            3: "Overweight",
            4: "Obese"
        }
        
        try:
            if isinstance(raw_prediction, (int, np.integer)):
                final_status = target_mapping.get(int(raw_prediction), "Obese")
            else:
                # Try to convert to int first
                final_status = target_mapping.get(int(float(raw_prediction)), "Obese")
            
            if final_status is None:
                final_status = "Obese"
                
        except (ValueError, TypeError):
            final_status = "Obese"
            st.warning(f"⚠️ Could not properly interpret prediction: {raw_prediction}. Defaulting to 'Obese'.")
            
        # 3. Show the result on screen
        st.success(f"The predicted obesity level is: {final_status.replace('_', ' ')}")
        
        # 4. Save the ENGLISH word to memory for Tab 3 to use (ensure it's not None)
        st.session_state['obesity_level'] = final_status if final_status else "Obese"
        

# ==========================================
# TAB 2: THE FOOD SCANNER
# ==========================================
with tab2:
    st.header("Step 2: Scan your meal")
    st.write("Take a photo or upload a picture of your food to estimate its calories.")

    st.info("If camera does not open on mobile, use the upload option below.")

    camera_image = st.camera_input("Take a photo of your food")

    uploaded_file = st.file_uploader(
        "Or upload / take photo from mobile camera",
        type=["jpg", "png", "jpeg"]
    )

    lookup_mode = st.radio(
        "Food lookup mode",
        ["Standard", "Indian dishes only"],
        help="Choose Indian dishes only to prioritize the local Indian database and a configured Indian dish API."
    )
    indian_only = lookup_mode == "Indian dishes only"
    if indian_only:
        st.info("Indian-only lookup mode is enabled. The app will use local Indian food data first and then the configured Indian food API.")
        if not os.getenv('INDIAN_FOOD_API_URL', '').strip():
            st.warning("INDIAN_FOOD_API_URL is not configured, so Indian-only mode will use local Indian food data only.")
    
    # Determine which image to use
    if camera_image is not None:
        image = Image.open(camera_image)
        source = "camera"
    elif uploaded_file is not None:
        image = Image.open(uploaded_file)
        source = "upload"
    else:
        image = None
        source = None
    
    if image is not None:
        # Display the image
        st.image(image, caption=f'Food from {source}', use_container_width=True)
        
        st.write("Analyzing image...")
        
        # 3. Process the image for the AI
        img_resized = image.resize((224, 224)) # MobileNet requires exactly 224x224 pixels
        img_array = img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # 4. Make the prediction - use the top 3 guesses for better context
        predictions = vision_model.predict(img_array)
        decoded_preds = decode_predictions(predictions, top=3)[0]

        st.subheader("Top image predictions")
        for idx, pred in enumerate(decoded_preds, 1):
            label_text = pred[1].replace('_', ' ').title()
            score_text = pred[2] * 100
            st.write(f"{idx}. {label_text} — {score_text:.1f}%")

        raw_prediction = decoded_preds[0][1].lower().replace('_', ' ')
        confidence = decoded_preds[0][2] * 100
        st.success(f"I am {confidence:.2f}% sure this is: **{raw_prediction.title()}**")

        # Show alternative matches for the same image
        suggestions = [raw_prediction]
        for pred in decoded_preds[1:]:
            pred_name = pred[1].lower().replace('_', ' ')
            if pred_name not in suggestions:
                suggestions.append(pred_name)
            
            # Check if this prediction has an alias to an Indian food
            normalized = pred_name.replace(' ', '_')
            if normalized in LOCAL_FOOD_ALIASES:
                aliased_food = LOCAL_FOOD_ALIASES[normalized]
                if aliased_food in LOCAL_FOOD_DATABASE and aliased_food not in suggestions:
                    suggestions.append(aliased_food.replace('_', ' '))

        # For Indian-only mode, prioritize alias matches
        probable_match = None
        probable_match_score = 0
        
        if indian_only:
            for idx, pred in enumerate(decoded_preds):
                pred_name = pred[1].lower().replace('_', ' ')
                pred_norm = pred_name.replace(' ', '_')
                pred_score = pred[2]
                
                # Check direct database match
                if pred_norm in LOCAL_FOOD_DATABASE and pred_score > probable_match_score:
                    probable_match = pred_norm
                    probable_match_score = pred_score
                
                # Check alias match
                if pred_norm in LOCAL_FOOD_ALIASES:
                    aliased = LOCAL_FOOD_ALIASES[pred_norm]
                    if aliased in LOCAL_FOOD_DATABASE and pred_score > probable_match_score:
                        probable_match = aliased
                        probable_match_score = pred_score

        if probable_match:
            st.info(f"🍜 Likely Indian match: **{probable_match.replace('_', ' ').title()}**")
            if probable_match.replace('_', ' ') not in suggestions:
                suggestions.append(probable_match.replace('_', ' '))

        selected_index = 0
        if probable_match and probable_match.replace('_', ' ') in suggestions:
            selected_index = suggestions.index(probable_match.replace('_', ' '))

        selected_match = st.selectbox(
            "Choose the most accurate match if needed:",
            options=[s.title() for s in suggestions],
            index=selected_index,
            help="Select a better match for your image if the top prediction is wrong."
        ).lower()

        with st.expander("🛠️ Did the AI guess wrong? Type your food name here"):
            manual_override = st.text_input("Type the correct food name (e.g., 'samosa' or 'dosa'):")

        if manual_override:
            food_name = manual_override.strip().lower()
            st.warning(f"Overriding AI. Looking up your entry: **{food_name.title()}**")
        else:
            food_name = selected_match

        # 5. Look up the calories and nutrition data
        info = get_food_details(food_name, indian_only=indian_only)

        # If the top prediction did not resolve, try the alternate image guesses with the API/local database
        if info is None and not manual_override:
            for pred in decoded_preds[1:]:
                alt_name = pred[1].lower().replace('_', ' ')
                alt_info = get_food_details(alt_name, indian_only=indian_only)
                if alt_info is not None:
                    info = alt_info
                    food_name = alt_name
                    st.info(f"Trying alternate guess: **{alt_name.title()}**")
                    break
        
        st.markdown("---")
        st.subheader("📊 Calorie & Nutrition Estimate")
        
        if info and info.get('calories') is not None:
            calories = info['calories']
            st.metric(label="Estimated Calories", value=f"{calories} kcal")
            st.write(f"**Food:** {info.get('label', food_name.replace('_', ' ').title())}")
            st.write(f"**Source:** {info.get('source', 'Local/API lookup')} ")
            if info.get('description'):
                st.write(info['description'])
            nutrition_cols = st.columns(3)
            nutrition_cols[0].metric("Protein", f"{info.get('protein', 'N/A')} g")
            nutrition_cols[1].metric("Carbs", f"{info.get('carbs', 'N/A')} g")
            nutrition_cols[2].metric("Fat", f"{info.get('fat', 'N/A')} g")
            st.info("Note: This estimate is based on average portion sizes and dish recipes.")
            st.session_state['last_calories'] = calories
            
            if st.button("➕ Log this meal to my Daily Tracker"):
                st.session_state['total_calories'] += calories
                st.success(f"Added {calories} kcal! Your daily total is now {st.session_state['total_calories']} kcal.")
        else:
            st.warning(f"I recognized this as **{food_name.replace('_', ' ')}**, but I could not determine nutrition info automatically.")
            st.info("If this is an Indian dish, enter its name below to fetch calories and nutrition details.")
            manual_dish = st.text_input("Enter Indian dish name", value="")
            if manual_dish:
                manual_info = get_food_details(manual_dish, indian_only=indian_only)
                if manual_info and manual_info.get('calories') is not None:
                    calories = manual_info['calories']
                    st.metric(label="Estimated Calories", value=f"{calories} kcal")
                    st.write(f"**Food:** {manual_info.get('label', manual_dish.title())}")
                    st.write(f"**Source:** {manual_info.get('source', 'Lookup')} ")
                    if manual_info.get('description'):
                        st.write(manual_info['description'])
                    st.session_state['last_calories'] = calories
                    if st.button("➕ Log this meal to my Daily Tracker", key="manual_log"):
                        st.session_state['total_calories'] += calories
                        st.success(f"Added {calories} kcal! Your daily total is now {st.session_state['total_calories']} kcal.")
                else:
                    st.error("Could not find nutrition details for that dish. Please try a different name or upload another image.")


# ==========================================
# TAB 3: THE RECOMMENDATION ENGINE & TRACKER
# ==========================================
with tab3:
    st.header("Step 3: Your Personalized Action Plan")
    
    # Check if the user has actually done Steps 1 and 2 yet
    if 'obesity_level' not in st.session_state or 'last_calories' not in st.session_state:
        st.warning("⚠️ Please complete the Obesity Predictor (Tab 1) and scan a meal (Tab 2) to get personalized advice.")
    else:
        # Grab the saved data from memory
        user_status = st.session_state.get('obesity_level', 'Obese')
        meal_cals = st.session_state.get('last_calories', 0)
        total_cals = st.session_state.get('total_calories', 0) # Safely grabs the total
        
        # Safety check: ensure user_status is not None or empty
        if not user_status:
            user_status = "Obese"
        
        # --- NEW DAILY SUMMARY DASHBOARD ---
        st.markdown("---")
        st.subheader("📈 Your Daily Summary")
        
        # Set a dynamic daily limit based on their AI prediction
        if "Normal_Weight" in user_status or "Insufficient" in user_status:
            daily_limit = 2200
        elif "Overweight" in user_status:
            daily_limit = 1800
        else: # Obesity categories
            daily_limit = 1500
            
        # Calculate how much is left and draw a progress bar
        calories_left = daily_limit - total_cals
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Daily Limit", f"{daily_limit} kcal")
        col2.metric("Consumed Today", f"{total_cals} kcal")
        
        if calories_left >= 0:
            col3.metric("Remaining", f"{calories_left} kcal")
            # Calculate percentage for progress bar (cap at 1.0 to prevent crashing)
            progress_pct = min(total_cals / daily_limit, 1.0)
            st.progress(progress_pct)
        else:
            col3.metric("Remaining", f"{calories_left} kcal", delta="Over Limit", delta_color="inverse")
            st.progress(1.0) # Bar is 100% full
            st.error("🚨 You have exceeded your recommended daily calorie limit based on your health profile.")
            
        st.markdown("---")
        
        st.subheader(f"Based on your profile ({user_status}) and your last meal ({meal_cals} kcal):")
        
        # --- THE LOGIC ENGINE ---
        
        # 1. Logic for Normal/Underweight users
        if user_status in ["Insufficient_Weight", "Normal_Weight"]:
            if meal_cals > 400:
                st.success("✅ **Diet Check:** This is a heavy meal, but it fits well within a healthy metabolism. Make sure you are getting enough protein!")
                st.info("🏃‍♂️ **Action:** A light 15-minute walk after eating aids digestion.")
            else:
                st.success("✅ **Diet Check:** A light and healthy meal! Make sure you are eating enough throughout the day to maintain your energy.")
                st.info("🏃‍♂️ **Action:** Standard strength training 3x a week is recommended.")
                
        # 2. Logic for Overweight users
        elif "Overweight" in user_status:
            if meal_cals > 300:
                st.warning("⚠️ **Diet Check:** This meal is slightly calorie-dense. Try swapping out simple carbs for leafy greens next time.")
                st.info("🏃‍♂️ **Action:** To burn off this specific meal, aim for a 30-minute brisk walk or light jogging today.")
            else:
                st.success("✅ **Diet Check:** Great choice! Keeping meals under 300 calories is an excellent strategy for steady, sustainable weight loss.")
                st.info("🏃‍♂️ **Action:** Keep up the good work! A 20-minute daily walk will amplify your results.")

        # 3. Logic for Obese users (Type I, II, III)
        elif "Obesity" in user_status:
            if meal_cals > 300:
                st.error("🚨 **Diet Check:** This meal is high in calories and may disrupt your weight loss goals. Consider cutting the portion size in half.")
                st.info("🏃‍♂️ **Action:** We recommend 45 minutes of low-impact cardio (like swimming or cycling) to offset this calorie intake.")
            else:
                st.success("✅ **Diet Check:** Excellent portion control! Light meals like this are exactly what you need to progress toward your goals.")
                st.info("🏃‍♂️ **Action:** Focus on consistency. 30 minutes of daily activity will help build a healthy routine.")

                
