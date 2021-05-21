from django.urls import path
from user import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='api_token_auth'), 
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.registration_view, name="signup"), 
    path('login/', views.login_View, name="login"), 
    path('users/', views.UserList.as_view(), name="users"),
    path('message/', views.MessagePost.as_view(), name="message"),
    path('getmessage/', views.GetMessageView.as_view(), name ="getmessage"),
]