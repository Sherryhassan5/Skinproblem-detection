from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.capture_image, name='capture_image'),
    path('images/', views.display_images, name='display_images'),
    path('decision/', views.decision_page, name='decision_page'),
    path('prediction_page',views.prediction_page, name='prediction_page')
]