from django.urls import path
from .import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    # path('profile/',views.profile,name="profile"),
    # path('login/',authentication_views.LoginView.as_view(template_name='users/login.html', authentication_form=forms.UserLoginForm), name='login'),
    # path('logout/',authentication_views.LogoutView.as_view(template_name='home/index.html'), name='logout'),
    # path('profile/edit/<int:id>',views.edit,name='edit-profile'),
    # path('update/<int:id>',views.update,name='update-profile'),

]