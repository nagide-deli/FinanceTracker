from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse('dashboard'))  # Ensure 'dashboard' is the name of your dashboard URL

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'signup.html')




class LoginView(APIView):
    def post(self, request):
        # Get email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard page
        else:
            messages.error(request, "Invalid email or password")
            return redirect('signin')


    def get(self, request):
            return render(request, 'signin.html')
