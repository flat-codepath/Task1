from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserRegistrationSerializer,UserLoginSerarilizer,AdminProfileSerializer,StudentProfielSerialzier,TeacherProfileSerialzier
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
# from rest_framework
from . models import User
class UserRegisterationApiView(APIView):
       def post(self,request,formate=None):
           serializer=UserRegistrationSerializer(data=request.data)
           if serializer.is_valid():
              serializer.save()
              return Response({'message':"user created successfully"},status=status.HTTP_201_CREATED)
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
  
class UserLoginView(APIView):
     def post(self,request,formate=None):
         serializer=UserLoginSerarilizer(data=request.data)
         if serializer.valid():
             username=serializer.validated_data.get('username')
             password=serializer.validated_data.get('password')
             user=authenticate(username=username,password=password)
             if user is not None:
                 return Response({"msg":"Logged in Successfully"},status=status.HTTP_200_OK)
             return Response({'errors':'username or password is Invalid'},status=status.HTTP_401_UNAUTHORIZED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None,formate=None,):
         id=pk 
         user=User.objects.get(id=pk) 
         if request.user.role == 'admin': 
            if id is not None:
               if User.objects.get(id=pk).sub_organization == request.user.sub_organization:
                  user=User.objects.get(id=pk)
                  if user.role == "teacher":
                        serializers=TeacherProfileSerialzier(user)
                     
                  elif user.role == 'student':
                        serializers=StudentProfielSerialzier(user)
                     
                  elif user.role == 'admin' and user.id == request.user.id:
                     serializers=AdminProfileSerializer(serializers.data,status=status.HTTP_201_CREATED)
                  return Response(serializers.data,status=status.HTTP_200_OK)
               
               return Response({'error':'you have no access to this  Profile'})
            return Response({},)
         elif request.user.role == 'teacher' and User.objects.get(id=pk).role == 'student':
             if request.user.teacher_set.teacher_class == User.objects.get(id=pk).student_set.student_class:
                 student=User.object.get(id=pk)
                 serializers=StudentProfielSerialzier(id=pk)

            