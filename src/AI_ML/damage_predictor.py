import numpy as np 
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Load the model and image processor
processor = AutoImageProcessor.from_pretrained("beingamit99/car_damage_detection")
model = AutoModelForImageClassification.from_pretrained("beingamit99/car_damage_detection")

# Load and process the image
image = Image.open(r"C:\practice\challenge\damage\image75.jpg")
inputs = processor(images=image, return_tensors="pt")

# Make predictions
outputs = model(**inputs)
logits = outputs.logits.detach().cpu().numpy()
predicted_class_id = np.argmax(logits)
predicted_proba = np.max(logits)
label_map = model.config.id2label
predicted_class_name = label_map[predicted_class_id]

# Print the results
print(f"Predicted class: {predicted_class_name} (probability: {predicted_proba:.4f}")
