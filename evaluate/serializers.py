from rest_framework import serializers
from account.models import *
from wizard.models import *
from django.http import JsonResponse

class PerioddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = '__all__'

class Evaluation_ffrequencySerializer(serializers.ModelSerializer):
    freq_number = serializers.IntegerField()
    period = PerioddSerializer()
    class Meta:
        model = Evaluation_frequency
        fields = '__all__'
        
class Evaluation_frequencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Evaluation_frequency
        fields = '__all__'
#hardasa islenibse ayri serializer elvae edersen. deyisirem. note to me in future
class MainSkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MainSkill
        fields = ('name','weight','norm')

class PeriodSerializer(serializers.ModelSerializer):
    frequency = Evaluation_frequencySerializer(many=True)
    position_count = serializers.SerializerMethodField()
    class Meta:
        model = Period
        fields = '__all__'
        
    def get_position_count(self,obj):
        count = 0
        a = obj.project
        for x in a.departments.all():
            for y in x.departmentpositions.all():
                count += 1
        return count
        
class employeeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('first_name','last_name','positionName')
        
class ProjectSerializerr(serializers.ModelSerializer):
    
    period = PeriodSerializer(many=True)
    class Meta:
        model = Project
        fields = '__all__'
    
class AllScoresPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AllScores
        fields = '__all__'
        
class AllScoressSerializer(serializers.ModelSerializer):
    employee = employeeeSerializer()
    class Meta:
        model = AllScores
        fields = '__all__'
        

    
class UserSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkill
        fields = '__all__'
        
class UserSkillForEvaEvaCompSerializer(serializers.ModelSerializer):
    skill = MainSkillSerializer()
    score = serializers.SerializerMethodField()
    class Meta:
        model = UserSkill
        fields = '__all__'
        
    def get_score(self,obj):
        score = 'undefined'
        if obj.skill.norm and obj.price and obj.price>0:
            score = obj.price/obj.skill.norm
        return score    
    
class AllScoresForEvaluateSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    
    employee = employeeeSerializer()
    comptency = UserSkillForEvaEvaCompSerializer(many=True)
    class Meta:
        model = AllScores
        fields = '__all__'     
        
    def get_total(self,obj):
        total_weight = 0
        score,total_score,score_number = 0,0,0
        for x in obj.comptency.all():
            total_weight += x.skill.weight
            if x.price:
                print(x.price,x.skill.norm)
                score += x.price/x.skill.norm
                score_number += 1
        if score_number > 0:
            total_score = score/score_number
        else:
            total_score = 1
        
        return {'total_weight':total_weight,'total_score':total_score}
            
           
        
        
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
        print(competencies)
        return competencies
    
    def get_get_allSkills(self,obj):
        return obj.get_allSkills()
    
class employeeSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    class Meta:
        model = Employee
        fields = '__all__'
        
    def get_total_score(self,obj):
        return obj.get_total_score()
    
        
        

class AllScoreUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserSkill
        fields = ('id','price','comment')
    
    # def get_score(self,obj):
    #     score = obj.skill.norm/obj.price
    #     return score    

class DepartmentPositionSerializer(serializers.ModelSerializer):
    positionskills = MainSkillSerializer(many=True)
    class Meta:
        model = DepartmentPosition
        fields = '__all__'
        
    
        
      
class EmployeeSerializerForUserPerformance(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    position = DepartmentPositionSerializer()
    class Meta:
        model = Employee
        fields = '__all__'
        
    def get_total_score(self,obj):
        total = obj.get_total_score()
        return total
        
    