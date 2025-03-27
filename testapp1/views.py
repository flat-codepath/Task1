from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserRegistrationSerializer,UserLoginSerializer,AdminProfileSerializer,StudentProfileSerialzier,TeacherProfileSerialzier
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from . models import User,Teacher,Student,Admin

class UserRegisterationApiView(APIView):
       def post(self,request,formate=None):
           serializer=UserRegistrationSerializer(data=request.data)
           if serializer.is_valid():
              serializer.save()
              return Response({'message':"user created successfully"},
                              status=status.HTTP_201_CREATED)
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
     def post(self,request,formate=None):
         serializer=UserLoginSerializer(data=request.data)
         if serializer.is_valid():
             username=serializer.validated_data.get('username')
             password=serializer.validated_data.get('password')
             user=authenticate(username=username,password=password)
             if user is not None:
                 login(request,user)
                 print(user.id)
                 return Response({"msg":"Logged in Successfully",
                                  "user":user.username,
                                  'id':user.id},
                                 status=status.HTTP_200_OK)
             return Response({'errors':'Username or Password is Invalid'},
             status=status.HTTP_401_UNAUTHORIZED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def get_user_by_id(pk):
    try:
        user=User.objects.get(id=pk)
        return user
    except User.DoesNotExist:
        return None
 
def get_profile_by_id(pk,model):
    try:
        profile=model.objects.get(id=pk)
        return profile
    except model.DoesNotExist:
        return None

# To access the Current Login User Profile 
class ProfileView(APIView):
    def get(self, request, pk=None, format=None):
        user = get_user_by_id(pk)
        if not user:
            return Response({"error": "User not Found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.username != user.username:
            return Response({"error": "You can't access others' profiles"}, status=status.HTTP_403_FORBIDDEN)
        
        profile_mapping = {
            "teacher": (Teacher, TeacherProfileSerialzier),
            "student": (Student, StudentProfileSerialzier),
            "admin": (Admin, AdminProfileSerializer)
        }

        if user.role in profile_mapping:
            model, serializer_class = profile_mapping[user.role]
            try:
                user_profile = model.objects.get(user=user)
                serializer = serializer_class(user_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except model.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "User has no Profile"}, status=status.HTTP_400_BAD_REQUEST)


class getStudentProfileView(APIView):

    def get_profile_data(self, profile):
        serializer=StudentProfileSerialzier(profile)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def get(self,request,pk=None,formate=None):
        id=pk
        profile=get_profile_by_id(id,Student)
        
        if not profile:
           return Response({'error':'Student Profile not found'}) 
        if request.user.sub_organization != profile.user.sub_organization:
            return Response({'you can not access the profiles of the other organziation student'})
        
        if request.user.role == 'admin':
            return self.get_profile_data(profile)
        
        if request.user.role == 'teacher':
            if request.user.teacher.teacher_class == profile.user.student.student_class:
                 return self.get_profile_data(self,profile)
            
        return Response({'error':f'you are not admin or teacher to access {profile.name} profile'})


         

class ListStudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if not request.user.sub_organization:
            return Response({'error': 'You are not an authorized user'}, status=status.HTTP_403_FORBIDDEN)

        role_filter = {
            'admin': {'user__sub_organization': request.user.sub_organization}
        }

        if request.user.role == 'teacher':
            if hasattr(request.user, 'teacher'): 
                role_filter['teacher'] = {'student_class': request.user.teacher.teacher_class}
            else:
                return Response({'error': 'You are registered as a teacher but have no teacher profile'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        filter_criteria = role_filter.get(request.user.role)
        if not filter_criteria:
            return Response({'error': 'You should be a Teacher or Admin to access these details'}, 
                            status=status.HTTP_403_FORBIDDEN)

        students = Student.objects.filter(**filter_criteria)
        serializer = StudentProfileSerialzier(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
             
 
class StudentProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk=None, format=None):
        profile = get_profile_by_id(pk, Student)
        print(profile)
        if not profile:
            return Response({"error": 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        if not (request.user.sub_organization and profile.user.sub_organization and request.user.sub_organization == profile.user.sub_organization):
            return Response({'error': 'You are not authorized to access or update the student details'}, status=status.HTTP_403_FORBIDDEN)

        role_access = (
            request.user.role == 'admin' or
            (request.user.role == 'teacher' and request.user.teacher.teacher_class == profile.student_class)
        )
        
        if not role_access:
            return Response({"error": f"You are not {profile.name}'s class teacher to update this profile"}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudentProfileSerialzier(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Student Profile Updated Successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getTeacherProfileView(APIView):
    def get_profile_data(self,profile):
        serializer=TeacherProfileSerialzier(profile)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def get(self,request,pk=None,formate=None):
        profile =get_profile_by_id(pk,Teacher)
        if not profile:
            return Response({'error':"Profile not Found"})
         
        if request.user.sub_organization != profile.user.sub_organization:
            return Response({'you can not access the profiles of the other organziation Staff'})
        
        if request.user.role == 'admin':
            return self.get_profile_data(profile)
        
        return Response({'error':f'you are not admin  to access {profile.name} profile'})
        

class ListTeacherProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,formate=None):
        if  request.user.sub_organization:
            if request.user.role == 'admin':
                teachers=Teacher.objects.filter(user__sub_organization=request.user.sub_organization)
                serialzier=TeacherProfileSerialzier(teachers,many=True)
                return Response(serialzier.data,status=status.HTTP_200_OK)
            else:
                return Response({'error':"Only Admin can access Teacher Profiles"})
        else:
            return Response({'error',"YOu are not Authorized user"})
        

class EditTeacherProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,pk=None,formate=None):
        id=pk
        profile=get_profile_by_id(id,Teacher)
        if not profile:
            return Response({"error": 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not profile.user.sub_organization and profile.user.sub_organization and profile.user.sub_organization == request.user.sub_organization:
            return Response({"error":"Your don't have any access to view or Change this profile "})
        
        if  request.user.role != 'admin':
              return Response({"error":"Your dont have access to change this profile "},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=TeacherProfileSerialzier(profile,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Teacher Profile Updated Successfully"},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)