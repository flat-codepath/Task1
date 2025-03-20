from rest_framework import serializers
from . models import User,Profile,Teacher,Student,Admin,Class,Section,Subject,SubOrganization


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Admin
        fields=['name','date_of_birth','date_of_joining','phone_number','address']


class TeacherProfileSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields=['name','date_of_birth','date_of_joining','phone_number','address','subjects','salary']

class StudentProfielSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields=['name','date_of_birth','date_of_joining','phone_number','address','roll_number','student_class','student_section']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'intputType':'password'},write_only=True)
    sub_organization = serializers.PrimaryKeyRelatedField(queryset=SubOrganization.objects.all())
    name=serializers.CharField(max_length=100)
    date_of_birth=serializers.DateField()
    date_of_joining =serializers.DateField()
    address=serializers.CharField(max_length=256)
    phone_number=serializers.CharField(max_length=10)
    
    roll_number = serializers.CharField(max_length=20, required=False)
    student_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), required=False)
    student_section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), required=False)
    
    subjects=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(),many=True,required=False)
    salary =serializers.IntegerField(required=False)


    class Meta:
        model=User
        fields=['username','email','sub_organization','role','password','password2','name','date_of_birth','date_of_joining',
                'address','phone_number','roll_number','student_class','student_section','subjects','salary']
        extra_kwargs={
              'password':{'write_only':True }
         }

    def validate(self, data):
        password=data.get('password')
        password2 =data.get('password2')
        role=data.get('role')

        if password != password2:
            raise serializers.ValidationError("Password and Comfirm password must be match")
        
        if role =='student':
            if not data.get('roll_number') or not data.get('student_class') or not data.get('student_section'):
                raise serializers.ValidationError('Please fill the roll_number,Class, Section Fields')
            
        if role == 'teacher':
            if not data.get('subjects') or not data.get('salary'):
                raise serializers.ValidationError("Please Provide the Above details")
        return data
    
        
    def create(self,validate_data):
        role=validate_data.pop('role')
        validate_data.pop('password2')
        profile_data={
            'name':validate_data.pop('name',None),
            'date_of_birth':validate_data.pop('date_of_birth',None),
            'date_of_joining':validate_data.pop('date_of_joining',None),
            'address':validate_data.pop('address',None),
            'phone_number':validate_data.pop('phone_number')
        }

        teacher_data={
            'salary':validate_data.pop('salary',None)
        }

        subjects=validate_data.pop('subjects',[])
        
        student_data={
            'roll_number':validate_data.pop('roll_number',None),
            'student_class':validate_data.pop('student_class',None),
            'student_section':validate_data.pop("student_section",None)
        }
        
        user=User.objects.create_user(role=role, **validate_data)

        if user.role == "admin":
            Admin.objects.create(user=user,**profile_data)
        elif user.role =="teacher":
            teacher= Teacher.objects.create(user=user, **profile_data,**teacher_data )
            teacher.subjects.set(list(subjects))
           
        elif user.role == "student":
            Student.objects.create(user=user,**profile_data,**student_data)
        return user
        

    
class UserLoginSerarilizer(serializers.ModelSerializer):
   class Meta:
       model=User
       fields=['username','password']
