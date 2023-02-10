from pet_kare.urls import path

from .views import PetDetailView, PetView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetDetailView.as_view())
]
