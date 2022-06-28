from .models import CustomUser
from . import serializer
from rest_framework.generics import (UpdateAPIView,
                                     DestroyAPIView,
                                     ListAPIView)
from .renderers import UserRenderers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class CreateSuperUser(APIView):

    def post(self, request):
        user_data = request.data
        serialized_data = serializer.SuperUserSerializer(data=user_data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(status=status.HTTP_201_CREATED, data=serialized_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serialized_data.errors)


class CreateManager(APIView):

    def post(self, request):
        user_data = request.data
        serialized_data = serializer.ManagerSerializer(data=user_data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(status=status.HTTP_201_CREATED, data=serialized_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serialized_data.errors)


class CreateEmployee(APIView):

    def post(self, request):
        if request.user.is_manager:
            user_data = request.data
            serialized_data = serializer.EmployeeSerializer(data=user_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(status=status.HTTP_201_CREATED, data=serialized_data.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serialized_data.errors)
        else:
            return Response(data="Permission denied")


class GetUserData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = CustomUser.objects.all()
        serialized_data = serializer.EmployeeSerializer(data)
        return Response(data=serialized_data.data)


# View class for getting list of all Employees registered(Can be performed by
# Manager only)
class GetEmpListView(ListAPIView):
    serializer_class = serializer.EmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role != "MANAGER":
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = CustomUser.objects.filter(role="EMPLOYEE")
            if users.count() >= 1:
                serializer = self.serializer_class(users, many=True)
                response = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Successfully fetched users',
                    'users': serializer.data

                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No employees available in this category!'},
                                status=status.HTTP_204_NO_CONTENT)


# View class for updating details of an existing employee(Can be performed by
# Manager only)
class UpdateEmpView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.EmployeeSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return CustomUser.objects.filter(id=user_id)

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user.role != "MANAGER":
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            instance = self.get_object()
            instance.first_name = request.data["first_name"]
            instance.last_name = request.data["last_name"]
            instance.date_of_birth = request.data["date_of_birth"]
            instance.address = request.data["address"]
            instance.contact_number = request.data["contact_number"]

            serializer = self.get_serializer(instance, data=request.data)

            if serializer.is_valid(raise_exception=True):
                self.partial_update(serializer)

            response = {
                'success': True,
                'message': 'Employee updated successfully!',
                'user': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)


# View class for deleting an existing employee(Can be performed by Manager only)
class DeleteEmpView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.role != "MANAGER":
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            user_id = self.kwargs["pk"]
            user_profile = CustomUser.objects.filter(id=user_id)
            serializers = serializer.EmployeeSerializer(user_profile, many=True)

            if serializers.data[0]["role"] == "SUPERUSER" or serializers.data[0]["role"] == "MANAGER":
                return Response({'message': 'You cannot delete any superuser or manager!'}, status.HTTP_403_FORBIDDEN)
            else:
                user_profile.delete()
                return Response({'message': 'Employee Deleted Successfully!'}, status.HTTP_204_NO_CONTENT)


class LoginUser(APIView):

    def post(self, request):
        data = request.data
        email = data['email']
        password = data["password"]

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            return Response(data="incorrect email")

        if not user.check_password(password):
            return Response(data="incorrect password")

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        return Response(data=get_tokens_for_user(user))


class Profile(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializers = serializer.ProfileSerializer(request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ChangedPassword(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializers = serializer.ChangedPasswordSerializer(
            data=request.data, context={'user': request.user})
        if serializers.is_valid(raise_exception=True):
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)

        return Response(serializers.errrors, status=status.HTTP_404_NOT_FOUND)


class ForgotPassword(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializers = serializer.ForgotPasswordSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, uid, token, format=None):
        serializers = serializer.ResetPasswordSerializer(data=request.data, context={
            'uid': uid, 'token': token})
        if serializers.is_valid(raise_exception=True):
            return Response({'msg': 'Password is  Reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
