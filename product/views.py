from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from product.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, ChangeUserPasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, GetProductSerializer, CategorySerializer, CreateProductSerializer, CreateCategorySerializer, UserUpdateSerializer
from django.contrib.auth import authenticate
from product.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from product.models import Product, Category

# generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)

            return Response({"msg": "Registration Success", "token": token}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')    
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', 'token':token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Invalid Credentials']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangeUserPasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeUserPasswordSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'msg': 'Password reset link sent. Check your email.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Your Profile has been Updated Successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetProductView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(user=request.user)
        serializer = GetProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['user'] = request.user.id

        serializer = CreateProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'msg': 'Your item has been added'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, itemCode):

        product = Product.objects.get(itemCode=itemCode)

        serializer = CreateProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({'msg': 'Your item has been updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    def delete(self, request, itemCode):
        item = Product.objects.get(itemCode=itemCode)
        
        item.delete()

        return Response({'msg': 'Your Item has been Deleted'}, status=status.HTTP_200_OK)


class CategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        request.data['user'] = request.user.id

        serializer = CreateCategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'msg': 'Your Category has been added'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, catId):

        category = Category.objects.get(uid=catId)

        serializer = CreateCategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({'msg': 'Your category has been updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, catId):
        item = Category.objects.get(uid=catId)
        
        item.delete()

        return Response({'msg': 'Your Category has been Deleted'}, status=status.HTTP_200_OK)