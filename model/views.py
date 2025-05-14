import os
import numpy as np
import tensorflow as tf
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from keras.preprocessing import image
from keras.models import load_model
from keras.applications.efficientnet import preprocess_input
import joblib
from ultralytics import YOLO

# Load the trained model and PCA object
# Modify model loading to handle GPU errors
try:
    # Force CPU usage for model inference to avoid GPU errors
    with tf.device('/CPU:0'):
        model = load_model('model.h5')
    yolo_model = YOLO('best.pt')
except Exception as e:
    print(f"Error loading models: {str(e)}")
    # Initialize placeholders that will be properly loaded when the app is accessed
    model = None
    yolo_model = None

def load_models_if_needed():
    global model, yolo_model
    if model is None or yolo_model is None:
        try:
            # Force CPU usage for model inference
            with tf.device('/CPU:0'):
                model = load_model('model.h5')
            yolo_model = YOLO('best.pt')
            return True
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            return False
    return True

classes = ['Acral Lentiginous Melanoma','Healthy Nail', 'Onychogryphosis','Blue Finger', 'Clubbing',  'Pitting']


def load_and_preprocess_image(image_path):
    # Load the image and resize it to 128x128, which should give us closer to 25088 features
    img = image.load_img(image_path, target_size=(128, 128))  # Changed to 128x128
    img_array = image.img_to_array(img)  # Convert image to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (1, 128, 128, 3)
    
    # Apply the same preprocessing as during training
    # If using EfficientNet, use its preprocessing function
    img_array = preprocess_input(img_array)  # Using the imported preprocess_input
    
    return img_array

def predict_image(model, img_array):
    # Define the class names (change as per your model's classes)
    classes = ['Blue Finger', 'Acral Lentiginous Melanoma', 'Pitting', 'Onychogryphosis', 'Clubbing', 'Healthy Nail']
    
    # Get model predictions for the image
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)

    # Get the prediction accuracy
    acc = float(predictions[0][predicted_class] * 100)
    return f"{classes[predicted_class[0]]}", acc, predicted_class[0]

def handle_uploaded_file(file):
    # Create media directory if it doesn't exist
    media_path = os.path.join(settings.BASE_DIR, 'media')
    os.makedirs(media_path, exist_ok=True)
    
    # Save file to media directory
    file_path = os.path.join(media_path, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def pred(request):
    if request.method == "POST":
        print("POST request received")
        try:
            # Load models if they weren't loaded at startup
            if not load_models_if_needed():
                messages.error(request, "Error loading AI models. Please try again later.")
                return render(request, 'model.html', {})
                
            # Print model summary to see expected input shape
            print("Model summary:")
            model.summary()
            
            file = request.FILES.get('fileinput')
            if not file:
                print("No file received")
                messages.error(request, "No file was uploaded")
                return render(request, 'model.html', {})
                
            print(f"File received: {file.name}")
            
            # Save the uploaded file
            file_path = handle_uploaded_file(file)
            print(f"File saved at: {file_path}")
            
            try:
                print("Processing image...")

                resultclsft = yolo_model.predict(source=file_path)

                # Predict using the model
                print("Making prediction...")
                predt, pred_value, ind = classes[resultclsft[0].probs.top1],resultclsft[0].probs.top1conf.item()*100,resultclsft[0].probs.top1
                print(f"Prediction result: {predt} with confidence {pred_value}")
                acc = f'{str(round(pred_value, 2))}%'
                
                # Fetch disease details
                print("Fetching disease details...")
                diseases_data = {
                    "Blue Finger":  "A condition where the finger appears bluish due to lack of oxygen in the blood, commonly caused by circulatory or respiratory issues.",
                    "Acral Lentiginous Melanoma": "A rare form of melanoma that typically appears on the palms, soles, or under the nails, often characterized by dark streaks or discoloration.",
                    "Pitting": "Small dents or pits on the nail surface, often associated with conditions like psoriasis, eczema, or alopecia areata.",
                    "Onychogryphosis": "A condition characterized by thickened, overgrown, and curved nails, usually due to neglect, trauma, or underlying medical conditions.",
                    "Clubbing": "Enlargement of the fingertips and downward curving of the nails, often linked to lung or heart diseases and low blood oxygen levels.",
                    "Healthy Nail":  "A nail that is smooth, evenly colored, free of spots or discolorations, and not brittle or overly thick.",
                }

                # Fetch details for the predicted disease
                disease_details = list(diseases_data.values())[ind]
                print(f"Disease details fetched for: {predt}")

                context = {
                    "disease_name": predt,
                    "accuracy": acc,
                    "description": disease_details,
                    "disease_image": os.path.basename(file_path)
                }
                print(f"Context prepared: {context}")
                
                # Render the output page with the context
                print("Rendering output page...")
                return render(request, 'output.html', context)
            
            except Exception as e:
                print(f"Error during prediction: {str(e)}")
                messages.error(request, f"Error during prediction: {str(e)}")
                return render(request, 'model.html', {})
        
        except Exception as e:
            print(f"Error handling file: {str(e)}")
            messages.error(request, f"Error handling file: {str(e)}")
            return render(request, 'model.html', {})
    
    print("GET request - rendering model page")
    return render(request, 'model.html', {})
