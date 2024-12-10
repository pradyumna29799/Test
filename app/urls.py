from django.urls import path
from . import views

urlpatterns = [
    path('books/',views.BookListCreateAPIView.as_view(),name = 'book-list-create'),
    path('book/<int:pk>/',views.BookDetailAPIView.as_view(),name = 'book-details-view'),
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    
    path('', views.RegisterViewUsingTemplate.as_view(), name='register'),
    path('sucess/', views.SuccessViewUsingTemplate.as_view(), name='sucess'),
    path('loginTemplate/', views.LoginViewUsingTemplate.as_view(), name='loginTemplate'),
    path('loginSucess/', views.SuccessLoginViewUsingTemplate.as_view(), name='loginSucess'),
    
    path('multipleForms/',views.MultipleFormsHandling.as_view(),name="multipleForms"),
    path('detailBook/<int:pk>',views.bookDetailTemplate.as_view(),name="multipleForms-singleData"),
   path('deleteBook/<int:pk>',views.DeleteBookTemplate.as_view(),name="deleteBook"),
   
   path('sidebar/',views.sideBarView.as_view(),name="sidebar")

]
           