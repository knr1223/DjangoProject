from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserDetails
from .serializers import UserDetailsSerializer

# Generic JSON Response function
def json_response(success, message, data=None, status_code=200):
    """Returns a structured JSON response"""
    return JsonResponse({
        "success": success,
        "message": message,
        "data": data
    }, status=status_code)

def print_hello(request):
    """Returns a simple hello world message"""
    return HttpResponse("Hello World!")

def home(request):
    """Renders the homepage"""
    return render(request, 'Loginify/index.html')

@csrf_exempt
def signup(request):
    """Handles user signup"""
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body)
            serializer = UserDetailsSerializer(data=input_data)

            if serializer.is_valid():
                serializer.save()
                return json_response(True, "User created successfully", serializer.data, 201)
            return json_response(False, "Validation failed", serializer.errors, 400)
        except Exception as e:
            return json_response(False, str(e), status_code=400)

    # Handle GET and other invalid request methods
    return json_response(False, "Invalid request method. Use POST.", None, 405)

@csrf_exempt
def login_user(request):
    """Handles user login"""
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body)
            email = input_data.get("email")
            password = input_data.get("password")

            if not email or not password:
                return json_response(False, "Email and password are required", None, 400)

            user = UserDetails.objects.filter(email=email).first()

            if not user:
                return json_response(False, "User not found", None, 404)

            if user.password != password:
                return json_response(False, "Invalid password", None, 401)

            return json_response(True, "Login successful", {"username": user.username, "email": user.email}, 200)
        
        except Exception as e:
            return json_response(False, str(e), status_code=400)

    return json_response(False, "Invalid request method. Use POST.", None, 405)

@csrf_exempt
def all_users(request):
    """Handles fetching all users"""
    if request.method == 'GET':
        users = UserDetails.objects.all()
        serializer = UserDetailsSerializer(users, many=True)
        return json_response(True, "Users retrieved successfully", serializer.data)

    return json_response(False, "Invalid request method. Use GET.", None, 405)

@csrf_exempt
def get_user_by_email(request, email):
    """Handles retrieving, updating, and deleting a user by email"""
    if request.method == 'GET':
        try:
            user = UserDetails.objects.get(email=email)
            serializer = UserDetailsSerializer(user)
            return json_response(True, "User found", serializer.data)
        except UserDetails.DoesNotExist:
            return json_response(False, "User not found", None, 404)

    if request.method == 'PUT':
        try:
            user = UserDetails.objects.get(email=email)
            input_data = json.loads(request.body)
            serializer = UserDetailsSerializer(user, data=input_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return json_response(True, "User updated successfully", serializer.data)
            return json_response(False, "Validation failed", serializer.errors, 400)
        except UserDetails.DoesNotExist:
            return json_response(False, "User not found", None, 404)

    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return json_response(True, "User deleted successfully", None, 204)
        except UserDetails.DoesNotExist:
            return json_response(False, "User not found", None, 404)

    return json_response(False, "Invalid request method. Use GET, PUT, or DELETE.", None, 405)
