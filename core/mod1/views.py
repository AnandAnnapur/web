from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Person
from .serializers import PersonSerializer
from .utils import get_tokens_for_user


    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_person(request):
    """
    Create a new person record and generate JWT tokens for them.
    """
    serializer = PersonSerializer(data=request.data)
    
    if serializer.is_valid():
        person = serializer.save()

        # Create a User account linked to the Person
        user, created = User.objects.get_or_create(
            username=person.email,
            defaults={'email': person.email, 'password': make_password(get_random_string(12))}
        )

        # Generate JWT tokens for the new user
        tokens = get_tokens_for_user(user)

        return Response({
            'message': 'Person created successfully',
            'person': serializer.data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def person_login(request):
    """
    Authenticate a person using email and phone number via GET request
    and return JWT tokens.
    """
    email = request.query_params.get('email')
    phone_no = request.query_params.get('phone_no')  # Using query params for GET

    if not email or not phone_no:
        return Response(
            {'error': 'Both email and phone number are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Find the Person by email and phone number
        person = get_object_or_404(Person, email=email, phone=phone_no)

        # Find or create a corresponding User account
        user, created = User.objects.get_or_create(
            username=person.email,
            defaults={'email': person.email, 'password': make_password(get_random_string(12))}
        )

        # Generate JWT tokens for the User
        tokens = get_tokens_for_user(user)

        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            'person_id': person.id,
            'email': person.email
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_person(request):
    """
    Get person details for the authenticated user.
    """
    user = request.user
    person = get_object_or_404(Person, email=user.email)
    serializer = PersonSerializer(person)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_person(request):
    """
    Update person details for the authenticated user.
    """
    user = request.user
    person = get_object_or_404(Person, email=user.email)
    serializer = PersonSerializer(person, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def partial_update_person(request):
    """
    Partially update person details for the authenticated user.
    """
    user = request.user
    person = get_object_or_404(Person, email=user.email)
    serializer = PersonSerializer(person, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_person(request):
    """
    Delete person record for the authenticated user.
    """
    user = request.user
    person = get_object_or_404(Person, email=user.email)
    person.delete()
    return Response({'message': 'Person deleted successfully'}, 
                    status=status.HTTP_204_NO_CONTENT)
