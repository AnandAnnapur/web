from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from mod1.views import (
    get_person,
    create_person,
    update_person,
    partial_update_person,
    delete_person,
    person_login
)



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/person/login/', person_login, name='person_login'),
    path('api/person/', get_person, name='get_person'),
    path('api/person/create/', create_person, name='create_person'),
    path('api/person/update/', update_person, name='update_person'),
    path('api/person/partial-update/', partial_update_person, name='partial_update_person'),
    path('api/person/delete/', delete_person, name='delete_person'),
]