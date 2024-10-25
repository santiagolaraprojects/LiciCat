from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import *

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Post, Put, Delete of the Own profile and Get of all the users
    path('', UserViewSet.as_view({ "get": "list", "post": "create", "put": "put", "delete": "delete"})),
    
    path('me', OwnUserView.as_view(), name='own-user'),
   
    # Get of one user
    path('<int:pk>', UserDetail.as_view(), name='user-detail'),
    
    # Get the token
    path('login/', obtain_auth_token),
    
    # Get return preferences, Post create them, Put modifie them
    path('preferences', Add_to_preferences.as_view()),
    
    # Post Follow a user if not following else unfollow
    path('<int:pk>/follow', FollowView.as_view()),
    # Get users following you

    path('following', ListFollowing.as_view()),
    # Get userse that follow you
    path('followers', ListFollowers.as_view()),

    #Create a rating
    path('ratings/', RatingCreateView.as_view(), name='rating_create'),
    #Get the average rating of a user
    path('ratings/average/', RatingAverageView.as_view()),

    #Get athenticated user notifications
    path('notifications/', NotificationsList.as_view()),    

    #Get users that start with prefix
    path('search/', BuscarPorNombre.as_view()),    

]
