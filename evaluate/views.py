from rest_framework import generics
from rest_framework.views import APIView
from wizard.api.serializers import *
from rest_framework.response import Response
import os
import pandas as pd
import openpyxl
from wizard.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.views import LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.utils.timezone import localtime
today = localtime().date()

class ProjectsApiView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerr
    
    
    def get_queryset(self):
        data=self.request.user.id
        if data:
            project=Project.objects.filter(companyLeader=data)
            return project
        
class Frequencies(generics.ListAPIView):
    queryset = Evaluation_frequency.objects.all()
    serializer_class = Evaluation_ffrequencySerializer
    
    
    def get_queryset(self):
        queryset = Evaluation_frequency.objects.all()
        data=self.request.user.id

        if data:
            project=Project.objects.get(companyLeader=data)
            return queryset.filter(period__project_id = project.id)
        
class AddPeriodApiView(generics.CreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PerioddSerializer
    
    
class AddFrequencyApiView(APIView):

    def post(self,request):
        data=request.data
        serializer = Evaluation_frequencySerializer(data=data) 
        serializer.is_valid(raise_exception=True)
        eva = serializer.save()

        for dep in ProjectDepartment.objects.filter(project=eva.period.project.id):
            print(dep.id)
            for emp in Employee.objects.filter(position__department=dep.id):
                print(emp.position.department.id)
                for rater in Employee.objects.filter(position__department=emp.position.department.id):
                    print(rater.position.department.id)
                    Scoreserializer = AllScoresSerializer(data={'employee':emp.id,'rater':rater.id,'evaluation_frequency':eva.id})
                    Scoreserializer.is_valid(raise_exception=True)
                    score = Scoreserializer.save()
               
                    for skill in MainSkill.objects.filter(position=emp.position.id):
                        pointserializer = UserSkillSerializer(data={'card':score.id,'skill':skill.id})
                        pointserializer.is_valid(raise_exception=True)
                        pointserializer.save()
        
    
        
        return Response({'message':'success'})
    
class EvaluationList(generics.ListAPIView):
    serializer_class = AllScoresSerializer
    
    def get_queryset(self,request):
        
        queryset = AllScores.objects.filter(rater = request.user.id)
  
        for x in queryset:
            if x.evaluation_frequency.start_date < today and x.evaluation_frequency.end_date > today:
                queryset.remove(x)
        return queryset
                
            
        
    
class EmployeeListForScores(generics.ListAPIView):
    serializer_class = employeeSerializer
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        queryset = Employee.objects.all()
        data=self.request.user.id
        
        if data:
            project=Project.objects.get(companyLeader=data,id=id)
            return queryset.filter(project=project.id)
        
