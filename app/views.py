from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer,RegisterSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.generic.base import TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth import logout
# from datetime import datetime, timedelta
# from django.http import JsonResponse
# from rest_framework_simplejwt.exceptions import TokenError



########################################################CRUD and login functionality using rest API classes ##################################################################################

class BookListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        books = Book.objects.all()
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    def get(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error":"Book does not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error":"Book does not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error":"Book does not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error":"Book does not exist"},status=status.HTTP_400_BAD_REQUEST)
        book.delete()
        return Response({"message":"deleted sucessfully"},status=status.HTTP_204_NO_CONTENT)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########################################################login using templates classes(not complete) ##################################################################################
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import logout

class RegisterViewUsingTemplate(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            request.session['saved_username'] = user.username
            return redirect('sucess')  # Correct spelling: "success"
        return render(request, self.template_name, {
            'message': 'Form data is not valid!',
            'errors': serializer.errors
        })


class SuccessViewUsingTemplate(TemplateView):
    template_name = "sucess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.pop('saved_username', None)
        return context


class LoginViewUsingTemplate(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data['username']
            request.session['saved_username'] = str(user)
            return redirect('loginSucess')  # Correct spelling: "login_success"
        return render(request, self.template_name, {
            'message': 'Form data is not valid!',
            'errors': serializer.errors
        })


class SuccessLoginViewUsingTemplate(TemplateView):
    template_name = "loginSucess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.pop('saved_username', None)
        return context

class MultipleFormsHandling(TemplateView):
    template_name = "multipleFormsHandling.html"
   
    
    def get(self,request):
        book_data = Book.objects.all()
        data = BookSerializer(book_data, many=True).data    
        return render(request, self.template_name, {"book_data": data})
        
    
    def post(self, request):
        serializer = BookSerializer(data=request.POST)
        if serializer.is_valid():
            book = serializer.save()
            # Fetch all books
            book_data = Book.objects.all()
            # Serialize all book objects
            data = BookSerializer(book_data, many=True).data
            return render(request, self.template_name, {
                "success": f"Book saved successfully with ID {book.id}",
                "book_data": data
            })
        return render(request, self.template_name, {
            "error": "Form data is not valid",
            "errors": serializer.errors
        })
    

class bookDetailTemplate(TemplateView):
    template_name = "update.html"
    
    def get(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request,self.template_name,{"error":"Book does not found"})
        serializer = BookSerializer(book)
        return render (request,self.template_name,{"data":serializer.data})
    
    
    def post(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request,self.template_name,{"error":"Book does not found"})        
        serializer = BookSerializer(book,data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('/multipleForms')
        return render(request,self.template_name,serializer.errors)
    

class DeleteBookTemplate(TemplateView):
    template_name = "multipleFormsHandling.html"
    
    def get(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request,self.template_name,{"error":"Book does not found"})     
        book.delete()
        # book_data = Book.objects.all()
        #     # Serialize all book objects
        # data = BookSerializer(book_data, many=True).data
        # return render(request,self.template_name,{"book_data":data,"message":"deleted sucessfully"})    
        return redirect("/multipleForms")
    
class sideBarView(TemplateView):
    template_name = "main_sidebar.html"
##########################################################################################################################################

