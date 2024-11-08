import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import streamlit as st
from PIL import Image

# Load the model
model_path = "C:/Users/admin/Desktop/models/cnn-mobilenet2_finetuned.keras"
model = tf.keras.models.load_model(model_path)

# Define food labels with nutritional information
food_labels = {
    "baby_back_ribs": {"calories": 290, "nutriscore": "E", "protein": 20, "carbs": 0, "fat": 22},
    "baklava": {"calories": 430, "nutriscore": "E", "protein": 6.0, "carbs": 54, "fat": 21},
    "beef_carpaccio": {"calories": 120, "nutriscore": "B", "protein": 12, "carbs": 0, "fat": 8},
    "beef_tartare": {"calories": 180, "nutriscore": "B", "protein": 15, "carbs": 0, "fat": 12},
    "beet_salad": {"calories": 75, "nutriscore": "A", "protein": 2.0, "carbs": 16, "fat": 0.5},
    "beignets": {"calories": 200, "nutriscore": "D", "protein": 4.0, "carbs": 22, "fat": 10},
    "bibimbap": {"calories": 490, "nutriscore": "C", "protein": 20, "carbs": 70, "fat": 15},
    "breakfast_burrito": {"calories": 350, "nutriscore": "D", "protein": 15, "carbs": 40, "fat": 15},
    "bruschetta": {"calories": 150, "nutriscore": "B", "protein": 5.0, "carbs": 20, "fat": 5},
    "caesar_salad": {"calories": 280, "nutriscore": "D", "protein": 7.0, "carbs": 12, "fat": 24},
    "cannoli": {"calories": 340, "nutriscore": "D", "protein": 6.0, "carbs": 28, "fat": 22},
    "caprese_salad": {"calories": 220, "nutriscore": "B", "protein": 9.0, "carbs": 7, "fat": 18},
    "carrot_cake": {"calories": 330, "nutriscore": "D", "protein": 4.0, "carbs": 45, "fat": 15},
    "cheese_plate": {"calories": 400, "nutriscore": "E", "protein": 22, "carbs": 0, "fat": 34},
    "cheesecake": {"calories": 320, "nutriscore": "D", "protein": 6.0, "carbs": 28, "fat": 22},
    "chicken_curry": {"calories": 270, "nutriscore": "C", "protein": 22, "carbs": 5, "fat": 18},
    "chicken_quesadilla": {"calories": 310, "nutriscore": "D", "protein": 20, "carbs": 30, "fat": 14},
    "chicken_wings": {"calories": 290, "nutriscore": "D", "protein": 22, "carbs": 0, "fat": 22},
    "chocolate_cake": {"calories": 400, "nutriscore": "D", "protein": 5.0, "carbs": 55, "fat": 20},
    "churros": {"calories": 310, "nutriscore": "D", "protein": 4.0, "carbs": 34, "fat": 18},
    "club_sandwich": {"calories": 380, "nutriscore": "C", "protein": 18, "carbs": 40, "fat": 18},
    "crab_cakes": {"calories": 220, "nutriscore": "C", "protein": 20, "carbs": 10, "fat": 12},
    "creme_brulee": {"calories": 240, "nutriscore": "D", "protein": 5.0, "carbs": 30, "fat": 12},
    "croque_madame": {"calories": 360, "nutriscore": "D", "protein": 22, "carbs": 24, "fat": 20},
    "cup_cakes": {"calories": 290, "nutriscore": "D", "protein": 3.0, "carbs": 45, "fat": 12},
    "deviled_eggs": {"calories": 120, "nutriscore": "B", "protein": 6.0, "carbs": 2, "fat": 10},
    "donuts": {"calories": 270, "nutriscore": "D", "protein": 4.0, "carbs": 30, "fat": 15},
    "dumplings": {"calories": 170, "nutriscore": "C", "protein": 8.0, "carbs": 22, "fat": 6},
    "edamame": {"calories": 120, "nutriscore": "A", "protein": 11, "carbs": 9, "fat": 5},
    "eggs_benedict": {"calories": 310, "nutriscore": "D", "protein": 15, "carbs": 20, "fat": 20},
    "escargots": {"calories": 190, "nutriscore": "C", "protein": 12, "carbs": 2, "fat": 15},
    "falafel": {"calories": 300, "nutriscore": "C", "protein": 12, "carbs": 28, "fat": 18},
    "fish_and_chips": {"calories": 590, "nutriscore": "D", "protein": 25, "carbs": 60, "fat": 28},
    "foie_gras": {"calories": 460, "nutriscore": "E", "protein": 12, "carbs": 4, "fat": 44},
    "french_fries": {"calories": 365, "nutriscore": "D", "protein": 4.0, "carbs": 52, "fat": 17},
    "french_onion_soup": {"calories": 210, "nutriscore": "C", "protein": 7.0, "carbs": 16, "fat": 12},
    "french_toast": {"calories": 290, "nutriscore": "D", "protein": 9.0, "carbs": 40, "fat": 10},
    "fried_calamari": {"calories": 150, "nutriscore": "C", "protein": 15, "carbs": 8, "fat": 7},
    "fried_rice": {"calories": 370, "nutriscore": "C", "protein": 8.0, "carbs": 45, "fat": 16},
    "frozen_yogurt": {"calories": 180, "nutriscore": "B", "protein": 6.0, "carbs": 34, "fat": 2},
    "garlic_bread": {"calories": 150, "nutriscore": "C", "protein": 4.0, "carbs": 20, "fat": 6},
    "gnocchi": {"calories": 250, "nutriscore": "C", "protein": 6.0, "carbs": 45, "fat": 4},
    "greek_salad": {"calories": 170, "nutriscore": "A", "protein": 5.0, "carbs": 8, "fat": 14},
    "grilled_cheese_sandwich": {"calories": 320, "nutriscore": "D", "protein": 12, "carbs": 32, "fat": 16},
    "grilled_salmon": {"calories": 370, "nutriscore": "B", "protein": 34, "carbs": 0, "fat": 24},
    "guacamole": {"calories": 230, "nutriscore": "B", "protein": 3.0, "carbs": 12, "fat": 20},
    "gyoza": {"calories": 170, "nutriscore": "C", "protein": 7.0, "carbs": 22, "fat": 6},
    "hamburger": {"calories": 500, "nutriscore": "D", "protein": 28, "carbs": 40, "fat": 22},
    "hot_and_sour_soup": {"calories": 90, "nutriscore": "A", "protein": 6.0, "carbs": 10, "fat": 3},
    "hummus": {"calories": 160, "nutriscore": "B", "protein": 5.0, "carbs": 15, "fat": 9},
    "ice_cream": {"calories": 210, "nutriscore": "D", "protein": 4.0, "carbs": 27, "fat": 10},
    "jalapeno_poppers": {"calories": 290, "nutriscore": "D", "protein": 6.0, "carbs": 24, "fat": 20},
    "kaiser_roll": {"calories": 160, "nutriscore": "B", "protein": 5.0, "carbs": 30, "fat": 2},
    "kale_salad": {"calories": 100, "nutriscore": "A", "protein": 3.0, "carbs": 10, "fat": 5},
    "key_lime_pie": {"calories": 290, "nutriscore": "D", "protein": 4.0, "carbs": 40, "fat": 14},
    "kimchi": {"calories": 25, "nutriscore": "A", "protein": 2.0, "carbs": 5, "fat": 0.2},
    "kung_pao_chicken": {"calories": 290, "nutriscore": "C", "protein": 18, "carbs": 18, "fat": 16},
    "lasagna": {"calories": 390, "nutriscore": "C", "protein": 20, "carbs": 40, "fat": 18},
    "lobster_roll": {"calories": 360, "nutriscore": "C", "protein": 16, "carbs": 30, "fat": 20},
    "macaroni_and_cheese": {"calories": 330, "nutriscore": "D", "protein": 12, "carbs": 40, "fat": 14},
    "macarons": {"calories": 160, "nutriscore": "C", "protein": 3.0, "carbs": 20, "fat": 8},
    "margarita": {"calories": 200, "nutriscore": "D", "protein": 0.0, "carbs": 24, "fat": 0.1},
    "miso_soup": {"calories": 40, "nutriscore": "A", "protein": 3.0, "carbs": 5, "fat": 1},
    "mojito": {"calories": 150, "nutriscore": "C", "protein": 0.0, "carbs": 12, "fat": 0.1},
    "mozzarella_sticks": {"calories": 260, "nutriscore": "D", "protein": 12, "carbs": 20, "fat": 14},
    "nachos": {"calories": 400, "nutriscore": "D", "protein": 12, "carbs": 40, "fat": 20},
    "naan_bread": {"calories": 300, "nutriscore": "C", "protein": 8.0, "carbs": 50, "fat": 8},
    "nachos": {"calories": 400, "nutriscore": "D", "protein": 12, "carbs": 40, "fat": 20},
    "omelette": {"calories": 210, "nutriscore": "B", "protein": 18, "carbs": 4, "fat": 14},
    "onion_rings": {"calories": 280, "nutriscore": "D", "protein": 4.0, "carbs": 32, "fat": 14},
    "pad_thai": {"calories": 450, "nutriscore": "C", "protein": 20, "carbs": 60, "fat": 14},
    "pancakes": {"calories": 350, "nutriscore": "C", "protein": 6.0, "carbs": 60, "fat": 10},
    "panna_cotta": {"calories": 200, "nutriscore": "D", "protein": 5.0, "carbs": 25, "fat": 10},
    "pasta_primavera": {"calories": 320, "nutriscore": "B", "protein": 12, "carbs": 50, "fat": 8},
    "peking_duck": {"calories": 380, "nutriscore": "C", "protein": 28, "carbs": 12, "fat": 22},
    "pepperoni_pizza": {"calories": 300, "nutriscore": "D", "protein": 14, "carbs": 32, "fat": 14},
    "pesto_pasta": {"calories": 340, "nutriscore": "C", "protein": 10, "carbs": 45, "fat": 12},
    "pho": {"calories": 350, "nutriscore": "B", "protein": 15, "carbs": 50, "fat": 8},
    "pizza_margherita": {"calories": 260, "nutriscore": "C", "protein": 10, "carbs": 30, "fat": 12},
    "pork_chops": {"calories": 260, "nutriscore": "B", "protein": 26, "carbs": 0, "fat": 18},
    "pulled_pork_sandwich": {"calories": 380, "nutriscore": "C", "protein": 20, "carbs": 40, "fat": 14},
    "quesadilla": {"calories": 310, "nutriscore": "D", "protein": 15, "carbs": 30, "fat": 18},
    "quiche": {"calories": 330, "nutriscore": "C", "protein": 12, "carbs": 20, "fat": 20},
    "ramen": {"calories": 430, "nutriscore": "C", "protein": 20, "carbs": 50, "fat": 18},
    "ravioli": {"calories": 260, "nutriscore": "C", "protein": 10, "carbs": 30, "fat": 10},
    "rice_pudding": {"calories": 180, "nutriscore": "C", "protein": 4.0, "carbs": 30, "fat": 5},
    "risotto": {"calories": 350, "nutriscore": "C", "protein": 10, "carbs": 50, "fat": 12},
    "roast_beef": {"calories": 250, "nutriscore": "B", "protein": 30, "carbs": 0, "fat": 14},
    "roasted_brussels_sprouts": {"calories": 70, "nutriscore": "A", "protein": 3.0, "carbs": 10, "fat": 3},
    "sashimi": {"calories": 130, "nutriscore": "A", "protein": 20, "carbs": 0, "fat": 4},
    "scallops": {"calories": 140, "nutriscore": "B", "protein": 20, "carbs": 4, "fat": 4},
    "shepherds_pie": {"calories": 300, "nutriscore": "C", "protein": 20, "carbs": 30, "fat": 12},
    "shrimp_cocktail": {"calories": 90, "nutriscore": "A", "protein": 12, "carbs": 10, "fat": 2},
    "spaghetti_bolognese": {"calories": 370, "nutriscore": "C", "protein": 20, "carbs": 45, "fat": 12},
    "spaghetti_carbonara": {"calories": 380, "nutriscore": "C", "protein": 18, "carbs": 50, "fat": 14},
    "spring_rolls": {"calories": 150, "nutriscore": "B", "protein": 5.0, "carbs": 20, "fat": 6},
    "steak_frites": {"calories": 520, "nutriscore": "D", "protein": 40, "carbs": 40, "fat": 22},
    "strawberry_shortcake": {"calories": 290, "nutriscore": "D", "protein": 5.0, "carbs": 50, "fat": 12},
    "sushi": {"calories": 150, "nutriscore": "B", "protein": 10, "carbs": 20, "fat": 5},
    "tacos": {"calories": 200, "nutriscore": "C", "protein": 10, "carbs": 20, "fat": 10},
    "takoyaki": {"calories": 250, "nutriscore": "C", "protein": 8.0, "carbs": 30, "fat": 12},
    "tiramisu": {"calories": 400, "nutriscore": "D", "protein": 6.0, "carbs": 55, "fat": 22},
    "tuna_tartare": {"calories": 180, "nutriscore": "B", "protein": 20, "carbs": 0, "fat": 7},
    "waffles": {"calories": 310, "nutriscore": "D", "protein": 7.0, "carbs": 50, "fat": 10},
}


# List of class names in the same order as the model's output
class_names = [
    "baby_back_ribs", "baklava", "beef_carpaccio", "beef_tartare", "beet_salad",
    "beignets", "bibimbap", "breakfast_burrito", "bruschetta", "caesar_salad",
    "cannoli", "caprese_salad", "carrot_cake", "cheese_plate", "cheesecake",
    "chicken_curry", "chicken_quesadilla", "chicken_wings", "chocolate_cake", "churros",
    "club_sandwich", "crab_cakes", "creme_brulee", "croque_madame", "cup_cakes",
    "deviled_eggs", "donuts", "dumplings", "edamame", "eggs_benedict",
    "escargots", "falafel", "fish_and_chips", "foie_gras", "french_fries",
    "french_onion_soup", "french_toast", "fried_calamari", "fried_rice", "frozen_yogurt",
    "garlic_bread", "gnocchi", "greek_salad", "grilled_cheese_sandwich", "grilled_salmon",
    "guacamole", "gyoza", "hamburger", "hot_and_sour_soup", "hot_dog",
    "huevos_rancheros", "hummus", "ice_cream", "lasagna", "lobster_bisque",
    "lobster_roll_sandwich", "macaroni_and_cheese", "macarons", "miso_soup", "mussels",
    "nachos", "omelette", "onion_rings", "oysters", "pad_thai",
    "paella", "pancakes", "panna_cotta", "peking_duck", "pho",
    "pizza", "poutine", "prime_rib", "pulled_pork_sandwich", "ramen",
    "ravioli", "red_velvet_cake", "risotto", "sashimi", "seaweed_salad",
    "spaghetti_bolognese", "spaghetti_carbonara", "strawberry_shortcake", "sushi", "tacos",
    "takoyaki", "tiramisu", "tuna_tartare", "waffles"
]

# Streamlit webpage setup
st.set_page_config(page_title="Food Nutritional Tracker", layout="centered")

# Add a logo at the beginning
logo_path = "C:/Users/admin/Downloads/Smart Diet (1).png"
logo = Image.open(logo_path)
st.image(logo, use_column_width=True)

# Add a big "START TRACKING" button
if st.button("START TRACKING"):
    st.write("Upload an image of food to get nutritional information")

    # File uploader in Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        # Load and preprocess the image
        img = Image.open(uploaded_file).resize((224, 224))
        img_array = np.array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        try:
            # Make predictions
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_name = class_names[predicted_class_index]

            # Retrieve nutritional information
            nutrition_info = food_labels.get(predicted_class_name, {})

            # Display predicted class and nutritional information
            st.image(img, caption="Uploaded Image", use_column_width=True)
            st.write(f"Predicted food item: {predicted_class_name.replace('_', ' ').title()}")
            
            if nutrition_info:
                st.write(f"Calories: {nutrition_info['calories']} kcal")
                st.write(f"Nutriscore: {nutrition_info['nutriscore']}")
                st.write(f"Protein: {nutrition_info['protein']} g")
                st.write(f"Carbs: {nutrition_info['carbs']} g")
                st.write(f"Fat: {nutrition_info['fat']} g")
            else:
                st.write("Nutritional information is not available for this food item.")
        except Exception as e:
            st.write(f"Error during prediction: {e}")
    else:
        st.write("Please upload an image to see the prediction and nutritional information.")
else:
    st.write("Click 'START TRACKING' to begin.")