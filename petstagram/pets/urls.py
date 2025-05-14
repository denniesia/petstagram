from django.urls import path, include
from petstagram.pets import views
urlpatterns = [
    path('add/', views.AddPetView.as_view(), name='add-pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', views.PetDetailsView.as_view(), name='details-pet'),
        path('edit/', views.PetEditView.as_view(), name='edit-pet'),
        path('delete/', views.PetDeleteView.as_view(), name='delete-pet'),
    ]))

]