from rest_framework import serializers
from account.models import *
from wizard.models import *
from django.http import JsonResponse


class HirponormsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hirponorms
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainSkill
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        
class ProjectDepartmentSerializer4(serializers.ModelSerializer):

    class Meta:
        model = ProjectDepartment
        fields = ('id','name')
    
class DepartmentPositionSerializer(serializers.ModelSerializer):
    department = ProjectDepartmentSerializer4()
    class Meta:
        model = DepartmentPosition
        fields = ('name','department','id')

class DepartmentPositionForWizardSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = DepartmentPosition
        fields = ('name','department')

class ProjectDepartmentForCompSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDepartment
        fields = '__all__'
        
class DepartmentSerializerForOrganizitialChart(serializers.ModelSerializer):
    class Meta:
        model=ProjectDepartment
        fields = ('name','employee_number','id')        

class ProjectDepartmentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProjectDepartment
        fields = ('name','employee_number','project','id')

#for comptencies
class ProjectDepartmentSerializer(serializers.ModelSerializer):
    departmentpositions = DepartmentPositionSerializer(many=True)
    compatencies = serializers.SerializerMethodField()
    allSkills = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDepartment
        fields = ('id', 'project', 'name', 'description', 'employee_number', 'departmentpositions','compatencies','allSkills')
        
    def get_compatencies(self,obj):
        return obj.get_compatencies()
    
    def get_allSkills(self,obj):
        return obj.get_allSkills()

class SimpleProjectDepartmentSerializer(serializers.ModelSerializer):
    compatencies = serializers.SerializerMethodField()
    get_allSkills = serializers.SerializerMethodField()
    class Meta:
        model = ProjectDepartment
        fields = '__all__'
    
        
    def get_compatencies(self,obj):
        competencies = []
        for y in obj.departmentpositions.all():
            
            for norm in MainSkill.objects.filter(position=y,position__department__id=obj.id):
                competencies.append({'id':norm.id,'weight':norm.weight,'norm':norm.norm,'position':{'name':y.name,'id':y.id,'department':obj.id},'department':{'name':obj.name,'id':obj.id,'project':obj.project.id},'skill':{'name':norm.name,'id':norm.id,'department':norm.position.department.id}})

        return competencies
    
    def get_get_allSkills(self,obj):
        return obj.get_allSkills()

class SkillNormCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MainSkill
        fields = '__all__'


class SimpleSkillNormSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainSkill
        fields = '__all__'
    
    # def create(self, validated_data):
    #     position = validated_data.get('position')
    #     skill = validated_data.get('skill')
    #     old_object = SkillNorm.objects.filter(position=position, skill=skill)
    #     if old_object.exists():
    #         old_object.delete()
    #     new_object = SkillNorm.objects.create(**validated_data)
    #     return new_object

        


class SkillNormUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSkill
        fields = ['id','norm']
        
class WeightUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSkill
        fields = ['id','weight']

class UserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    position = DepartmentPositionSerializer()
    hard_goal = serializers.SerializerMethodField()
    soft_goal = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
    
    def get_soft_goal(self,obj):
        return obj.get_soft_goal()
    
    def get_hard_goal(self,obj):
        return obj.get_hard_goal()
    
    def get_goal(self,obj):
        return obj.get_goal()
    
class UserForEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email','id')

class NameOfEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id','first_name','last_name')

class EmployeeForUserpageSerializer(serializers.ModelSerializer):
    user = UserForEmployeeSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
        
class EmployeeForListSerializer(serializers.ModelSerializer):
    position = DepartmentPositionSerializer()
    class Meta:
        model = Employee
        fields = ('first_name','last_name','position','id')
        

class EmployeeForUserListPageSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    position = DepartmentPositionSerializer()
    user = UserForEmployeeSerializer()
    report_to = NameOfEmployeeSerializer()
    image = serializers.ImageField()
    class Meta:
        model = Employee
        fields = '__all__'
        
    def get_total(self,obj):
        score,total_score,score_number = 0,0,0
        total_weight = 0
        for y in obj.myscore.all():
            for x in y.comptency.all():
                if x.price:
                    score += x.price/x.skill.norm*x.skill.weight
       
                    total_weight += x.skill.weight
                    score_number += 1
        if score_number>0:
            total_score = score*100/total_weight
        else:
            total_score = '-'
        return {'total_score':total_score}
        
class EmployeeForCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = '__all__'
        

        
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','id')
        
class EmployeesallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('image','id')
      
class EmployeeSerializerForDashBoard(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('first_name','last_name','total_score')
        
    def get_total_score(self,obj):
        total = obj.get_total_score()
        return total      
    
    
class HomePageSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializerForDashBoard(many=True)
    bottom = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
        
    def get_bottom(self,obj):
        employees = obj.employee.all()
        
        emp = []
        for x in employees:
            emp.append({'first_name':x.first_name,'last_name':x.last_name})
            print(x.id)
        emp = emp[0:10]
        return emp[::-1]
