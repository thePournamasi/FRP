# ==========================================
# THE MEGA CALORIE & MACRO DATABASE
# ==========================================
LOCAL_FOOD_DATABASE = {
    # --- Western & Fast Food ---
    "pizza": {"calories": 266, "protein": 11, "carbs": 33, "fat": 10, "description": "1 slice"},
    "hamburger": {"calories": 295, "protein": 17, "carbs": 32, "fat": 12, "description": "Regular hamburger"},
    "cheeseburger": {"calories": 303, "protein": 15, "carbs": 30, "fat": 16, "description": "Classic cheeseburger"},
    "french_fries": {"calories": 312, "protein": 3, "carbs": 35, "fat": 17, "description": "Medium fry"},
    "hotdog": {"calories": 290, "protein": 12, "carbs": 27, "fat": 18, "description": "Standard beef hot dog"},
    "taco": {"calories": 156, "protein": 8, "carbs": 18, "fat": 7, "description": "Single taco"},
    "pasta": {"calories": 288, "protein": 8, "carbs": 57, "fat": 1, "description": "1 cup cooked"},
    "spaghetti": {"calories": 220, "protein": 8, "carbs": 43, "fat": 1, "description": "1 cup cooked"},
    "sandwich": {"calories": 250, "protein": 12, "carbs": 30, "fat": 8, "description": "Standard deli sandwich"},
    "fried_chicken": {"calories": 320, "protein": 15, "carbs": 10, "fat": 20, "description": "1 piece"},
    "steak": {"calories": 679, "protein": 62, "carbs": 0, "fat": 47, "description": "8 oz"},
    "salad": {"calories": 150, "protein": 3, "carbs": 10, "fat": 10, "description": "Side salad with dressing"},

    # --- Indian Staples (Breads & Rice) ---
    "roti": {"calories": 85, "protein": 3, "carbs": 17, "fat": 2, "description": "1 medium"},
    "chapati": {"calories": 85, "protein": 3, "carbs": 17, "fat": 2, "description": "1 medium"},
    "naan": {"calories": 260, "protein": 9, "carbs": 42, "fat": 5, "description": "1 piece"},
    "butter_naan": {"calories": 300, "protein": 9, "carbs": 42, "fat": 10, "description": "1 piece"},
    "paratha": {"calories": 250, "protein": 5, "carbs": 35, "fat": 10, "description": "1 plain paratha"},
    "stuffed_paratha": {"calories": 300, "protein": 6, "carbs": 40, "fat": 12, "description": "Aloo/Paneer"},
    "steamed_rice": {"calories": 205, "protein": 4, "carbs": 45, "fat": 0, "description": "1 cup cooked"},
    "jeera_rice": {"calories": 220, "protein": 4, "carbs": 45, "fat": 2, "description": "1 cup cooked"},
    "brown_rice": {"calories": 215, "protein": 5, "carbs": 45, "fat": 2, "description": "1 cup cooked"},
    "biryani": {"calories": 400, "protein": 15, "carbs": 50, "fat": 15, "description": "1 cup"},
    "pulao": {"calories": 250, "protein": 6, "carbs": 40, "fat": 6, "description": "1 cup"},

    # --- Indian Curries & Mains ---
    "dal": {"calories": 150, "protein": 9, "carbs": 25, "fat": 4, "description": "1 cup (yellow dal)"},
    "dal_makhani": {"calories": 300, "protein": 11, "carbs": 30, "fat": 15, "description": "1 cup"},
    "dal_tadka": {"calories": 180, "protein": 9, "carbs": 25, "fat": 6, "description": "1 cup"},
    "paneer_butter_masala": {"calories": 350, "protein": 12, "carbs": 15, "fat": 28, "description": "1 cup"},
    "palak_paneer": {"calories": 280, "protein": 14, "carbs": 12, "fat": 20, "description": "1 cup"},
    "chana_masala": {"calories": 260, "protein": 10, "carbs": 35, "fat": 10, "description": "1 cup"},
    "rajma": {"calories": 260, "protein": 10, "carbs": 35, "fat": 10, "description": "1 cup"},
    "mixed_vegetable": {"calories": 150, "protein": 4, "carbs": 20, "fat": 8, "description": "1 cup"},
    "chicken_curry": {"calories": 240, "protein": 20, "carbs": 10, "fat": 12, "description": "1 cup"},
    "butter_chicken": {"calories": 450, "protein": 25, "carbs": 15, "fat": 30, "description": "1 cup"},
    "mutton_curry": {"calories": 320, "protein": 22, "carbs": 12, "fat": 20, "description": "1 cup"},
    "indian_thali": {"calories": 750, "protein": 20, "carbs": 100, "fat": 25, "description": "Standard mixed plate"},
    "chicken_biryani": {"calories": 420, "protein": 20, "carbs": 50, "fat": 18, "description": "1 cup"},
    "veg_biryani": {"calories": 380, "protein": 12, "carbs": 60, "fat": 10, "description": "1 cup"},
    "aloo_paratha": {"calories": 300, "protein": 6, "carbs": 45, "fat": 12, "description": "1 piece"},
    "chole": {"calories": 280, "protein": 12, "carbs": 40, "fat": 10, "description": "1 cup"},
    "chole_bhature": {"calories": 520, "protein": 15, "carbs": 70, "fat": 22, "description": "1 plate"},
    "matar_paneer": {"calories": 320, "protein": 14, "carbs": 18, "fat": 22, "description": "1 cup"},
    "bhindi_masala": {"calories": 170, "protein": 4, "carbs": 20, "fat": 8, "description": "1 cup"},
    "aloo_gobi": {"calories": 180, "protein": 5, "carbs": 25, "fat": 8, "description": "1 cup"},
    "matar_malai": {"calories": 330, "protein": 10, "carbs": 18, "fat": 24, "description": "1 cup"},
    "fish_curry": {"calories": 280, "protein": 24, "carbs": 10, "fat": 16, "description": "1 cup"},
    "prawn_curry": {"calories": 260, "protein": 22, "carbs": 8, "fat": 14, "description": "1 cup"},
    "kadhi": {"calories": 220, "protein": 6, "carbs": 20, "fat": 12, "description": "1 cup"},
    "dal_fry": {"calories": 220, "protein": 10, "carbs": 30, "fat": 8, "description": "1 cup"},
    "kadhi_pakora": {"calories": 300, "protein": 8, "carbs": 35, "fat": 14, "description": "1 cup"},
    "methi_mutter": {"calories": 200, "protein": 7, "carbs": 20, "fat": 10, "description": "1 cup"},
    "aloo_matar": {"calories": 220, "protein": 6, "carbs": 25, "fat": 10, "description": "1 cup"},
    "aloo_masala": {"calories": 230, "protein": 5, "carbs": 26, "fat": 10, "description": "1 cup"},

    # --- South Indian ---
    "idli": {"calories": 40, "protein": 1, "carbs": 8, "fat": 0, "description": "1 piece"},
    "dosa": {"calories": 130, "protein": 3, "carbs": 20, "fat": 3, "description": "1 plain dosa"},
    "masala_dosa": {"calories": 250, "protein": 5, "carbs": 35, "fat": 10, "description": "1 dosa with filling"},
    "vada": {"calories": 150, "protein": 4, "carbs": 15, "fat": 8, "description": "1 piece"},
    "sambar": {"calories": 110, "protein": 4, "carbs": 15, "fat": 3, "description": "1 cup"},
    "upma": {"calories": 200, "protein": 5, "carbs": 25, "fat": 8, "description": "1 cup"},
    "uttapam": {"calories": 180, "protein": 4, "carbs": 25, "fat": 6, "description": "1 piece"},

    # --- Street Food & Snacks ---
    "samosa": {"calories": 250, "protein": 4, "carbs": 30, "fat": 13, "description": "1 piece"},
    "kachori": {"calories": 200, "protein": 3, "carbs": 20, "fat": 12, "description": "1 piece"},
    "panipuri": {"calories": 25, "protein": 0, "carbs": 5, "fat": 1, "description": "1 piece (golgappa)"},
    "bhel_puri": {"calories": 150, "protein": 3, "carbs": 25, "fat": 5, "description": "1 plate"},
    "pav_bhaji": {"calories": 400, "protein": 8, "carbs": 50, "fat": 20, "description": "1 plate (2 pavs)"},
    "vada_pav": {"calories": 300, "protein": 6, "carbs": 35, "fat": 15, "description": "1 piece"},
    "momos": {"calories": 35, "protein": 1, "carbs": 6, "fat": 0, "description": "1 piece (steamed)"},
    "spring_roll": {"calories": 150, "protein": 3, "carbs": 15, "fat": 8, "description": "1 piece"},
    "green_chutney": {"calories": 25, "protein": 1, "carbs": 4, "fat": 0, "description": "1 tbsp"},

    # --- Sweets & Desserts ---
    "gulab_jamun": {"calories": 150, "protein": 2, "carbs": 25, "fat": 5, "description": "1 piece"},
    "rasgulla": {"calories": 100, "protein": 2, "carbs": 22, "fat": 1, "description": "1 piece"},
    "jalebi": {"calories": 150, "protein": 1, "carbs": 30, "fat": 4, "description": "1 piece (large)"},
    "kheer": {"calories": 220, "protein": 5, "carbs": 35, "fat": 7, "description": "1 cup"},
    "laddoo": {"calories": 170, "protein": 3, "carbs": 25, "fat": 7, "description": "1 piece (besan/motichoor)"},
    "barfi": {"calories": 130, "protein": 3, "carbs": 18, "fat": 5, "description": "1 piece"},
    "ice_cream": {"calories": 207, "protein": 3, "carbs": 24, "fat": 11, "description": "1 scoop"},
    "brownie": {"calories": 400, "protein": 4, "carbs": 50, "fat": 22, "description": "1 piece"},

    # --- Beverages ---
    "chai": {"calories": 100, "protein": 2, "carbs": 12, "fat": 3, "description": "1 cup with milk/sugar"},
    "coffee": {"calories": 2, "protein": 0, "carbs": 0, "fat": 0, "description": "black"},
    "cold_coffee": {"calories": 250, "protein": 6, "carbs": 35, "fat": 8, "description": "with milk and sugar"},
    "lassi": {"calories": 200, "protein": 6, "carbs": 30, "fat": 5, "description": "1 glass (sweet)"},
    "buttermilk": {"calories": 40, "protein": 2, "carbs": 4, "fat": 1, "description": "1 glass (chaas)"},
    "soda": {"calories": 140, "protein": 0, "carbs": 39, "fat": 0, "description": "1 can (cola)"},

    # --- Regional Specials (Odia / East Indian) ---
    "pakhala": {"calories": 220, "protein": 5, "carbs": 50, "fat": 0, "description": "1 bowl (water rice)"},
    "dalma": {"calories": 180, "protein": 8, "carbs": 30, "fat": 4, "description": "1 cup"},
    "chhena_poda": {"calories": 250, "protein": 10, "carbs": 25, "fat": 12, "description": "1 slice"},
    "rasabali": {"calories": 200, "protein": 6, "carbs": 25, "fat": 10, "description": "1 piece"}
}

LOCAL_FOOD_ALIASES = {
    # === BREADS & BREAKFAST ===
    # Generic bread/flatbread types
    "flatbread": "roti",
    "tortilla": "paratha",
    "naan_bread": "naan",
    "pita": "roti",
    "roti_bread": "roti",
    "chapati_bread": "chapati",
    "french_loaf": "naan",  # Similar shape/texture
    "baguette": "naan",
    "dough": "idli",
    "dumpling": "idli",
    "bun": "naan",
    
    # Breakfast/Pancake items
    "pancake": "dosa",
    "crepe": "dosa",
    "waffle": "dosa",
    "crepes": "dosa",
    "french_toast": "uttapam",
    "muffin": "idli",
    
    # Rice dishes
    "rice": "steamed_rice",
    "rice_dish": "steamed_rice",
    "basmati_rice": "jeera_rice",
    "brown_rice_dish": "brown_rice",
    "risotto": "biryani",
    "fried_rice": "pulao",
    "pilaf": "pulao",
    "rice_pilaf": "pulao",
    "rice_and_vegetables": "pulao",
    
    # === CURRIES & MAINS ===
    "consomme": "dal",
    "soup": "dal_tadka",
    "broth": "dal",
    "vegetable_soup": "dal_tadka",
    "lentil_soup": "dal",
    "hot_pot": "mixed_vegetable",
    "stew": "chicken_curry",
    "meat_stew": "mutton_curry",
    "curry_dish": "chicken_curry",
    "gravy": "dal_makhani",
    "sauce": "dal_makhani",
    
    # Vegetable dishes
    "cauliflower": "aloo_gobi",
    "mashed_potatoes": "aloo_masala",
    "potato_dish": "aloo_masala",
    "vegetable_stir_fry": "mixed_vegetable",
    "vegetables": "mixed_vegetable",
    "okra": "bhindi_masala",
    
    # Meat dishes
    "meat_loaf": "butter_chicken",
    "roasted_chicken": "butter_chicken",
    "fried_meat": "chicken_curry",
    "lamb": "mutton_curry",
    "lamb_stew": "mutton_curry",
    "goat_meat": "mutton_curry",
    "seafood": "fish_curry",
    "fish": "fish_curry",
    "shrimp": "prawn_curry",
    "prawns": "prawn_curry",
    
    # === SNACKS & STREET FOOD ===
    "potpie": "samosa",
    "empanada": "samosa",
    "pastry": "samosa",
    "spring_roll": "spring_roll",
    "egg_roll": "spring_roll",
    "croquette": "vada",
    "fritter": "vada",
    "fried_cake": "vada",
    "dumpling_fried": "vada",
    "pretzel": "jalebi",
    "churro": "jalebi",
    "spiral_pasta": "jalebi",
    "guacamole": "green_chutney",
    "dip": "green_chutney",
    "burrito": "spring_roll",
    "wrap": "spring_roll",
    "roll": "spring_roll",
    "momo": "momos",
    "dumpling_steamed": "momos",
    
    # === SWEETS & DESSERTS ===
    "doughnut": "gulab_jamun",
    "donut": "gulab_jamun",
    "dessert": "kheer",
    "pudding": "kheer",
    "trifle": "kheer",
    "cake": "kheer",
    "candy": "laddoo",
    "bonbon": "laddoo",
    "confection": "laddoo",
    "chocolate": "barfi",
    "fudge": "barfi",
    "brownie_dessert": "brownie",
    
    # === BEVERAGES ===
    "tea": "chai",
    "black_tea": "chai",
    "milk_tea": "chai",
    "espresso": "coffee",
    "cappuccino": "cold_coffee",
    "latte": "cold_coffee",
    "yogurt_drink": "lassi",
    "smoothie": "lassi",
    "soda_drink": "soda",
    "cola": "soda"
}
