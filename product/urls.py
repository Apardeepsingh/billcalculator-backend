
from django.urls import path, include
from product.views import UserRegistrationView, UserLoginView, UserProfileView, ChangeUserPasswordView, SendPasswordResetEmailView, UserPasswordResetView, GetProductView, CategoryView, UserUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('update-user/', UserUpdateView.as_view(), name='update-user'),
    path('changepassword/', ChangeUserPasswordView.as_view(), name='changepassowrd'),
    path('send_reset_password_email/', SendPasswordResetEmailView.as_view(), name='send_reset_password_email'),
    path('reset_password/<uid>/<token>', UserPasswordResetView.as_view(), name='reset_password'),
    path('get-products/', GetProductView.as_view(), name='get-products'),
    path('add-product/', GetProductView.as_view(), name='add-products'),
    path('delete-product/<itemCode>', GetProductView.as_view(), name='delete-products'),
    path('update-product/<itemCode>', GetProductView.as_view(), name='update-products'),
    path('get-categories/', CategoryView.as_view(), name='get-categories'),
    path('add-categories/', CategoryView.as_view(), name='add-categories'),
    path('delete-category/<catId>', CategoryView.as_view(), name='delete-category'),
    path('update-category/<catId>', CategoryView.as_view(), name='update-category'),
]
