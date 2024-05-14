from django.shortcuts import render,redirect
from .forms import ImageForm
from django.http import HttpResponse
from .models import CapturedImage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from django.conf import settings

saved_model_path = os.path.join(settings.BASE_DIR, 'models', 'cnn_practice1_model.h5')
model = load_model(saved_model_path)

IMAGE_WIDTH, IMAGE_HEIGHT = 100, 100
class_names = ['acne', 'dark circles', 'white spots']








# Create your views here.

def capture_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the image to the database
            request.session['captured_image_id'] = image_instance.id  # Store image ID in session
            return redirect('decision_page')  # Redirect to decision page
    else:
        form = ImageForm()
    return render(request, 'capture_image.html', {'form': form})

def decision_page(request):
    return render(request, 'decision_page.html')


def prediction_page(request):
    captured_image_id = request.session.get('captured_image_id')
    if captured_image_id:
        image_instance = CapturedImage.objects.get(id=captured_image_id)
        img_path = image_instance.image.path

        try:
            img = image.load_img(img_path, target_size=(IMAGE_WIDTH, IMAGE_HEIGHT))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.  # Rescale pixel values to [0, 1]

            prediction = model.predict(img_array)
            predicted_class_index = np.argmax(prediction)
            predicted_class = class_names[predicted_class_index]
            confidence = prediction[0][predicted_class_index]

            return render(request, 'prediction_page.html', {
                'image_instance': image_instance,
                'predicted_class': predicted_class,
                'confidence': confidence
            })
        except Exception as e:
            return HttpResponse("Error: " + str(e))
    else:
        return HttpResponse("No captured image found.")




# def capture_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 image_instance = CapturedImage(image=form.cleaned_data['image'])
#                 image_instance.save()
#                 img_path = image_instance.image.path
#                 print(f"Image saved at {img_path}")

#                 # Predict the skin type using the saved image
#                 try:
#                     img = image.load_img(img_path, target_size=(IMAGE_WIDTH, IMAGE_HEIGHT))
#                     img_array = image.img_to_array(img)
#                     img_array = np.expand_dims(img_array, axis=0)
#                     img_array /= 255.  # Rescale pixel values to [0, 1]
#                     print(f"Image array shape: {img_array.shape}")

#                     prediction = model.predict(img_array)
#                     print(f"Prediction raw output: {prediction}")

#                     predicted_class_index = np.argmax(prediction)
#                     predicted_class = class_names[predicted_class_index]
#                     confidence = prediction[0][predicted_class_index]

#                     print(f"Predicted class: {predicted_class}, Confidence: {confidence}")

#                     return render(request, 'display_prediction.html', {
#                         'image_instance': image_instance,
#                         'predicted_class': predicted_class,
#                         'confidence': confidence
#                     })
#                 except Exception as e:
#                     print(f"Error during prediction: {e}")
#                     return HttpResponse('Image upload failed during prediction')
#             except Exception as e:
#                 print(f"Error during image saving or processing: {e}")
#                 return HttpResponse('Image upload failed during saving')
#         else:
#             print("Form is not valid")
#             print(form.errors)
#             return HttpResponse('Image upload failed due to form validation')
#     else:
#         form = ImageForm()
#     return render(request, 'capture_image.html', {'form': form})

def display_images(request):
    images = CapturedImage.objects.all()
    return render(request, 'display_images.html', {'images': images})

