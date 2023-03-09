from django.db import models
from account.utils import create_slug_shortcode
from django.contrib.auth import get_user, get_user_model
from norm.models import *
CompanyLeader = get_user_model()

skilltype=(
    ('Soft','Soft'),
    ('Hard','Hard'),
)

industries=(
    ('IT','IT'),
    ('Construction','Construction'),
)

"""{"companyleader": 110, "project_name": "TEST","employee_number": 25, "industry": "IT", "objects": [{"name": "TEST","employee_number":3},{"name": "TEWST","employee_number":3},{"name": "TESTT","employee_number":3}]}"""

class Project(models.Model):
    companyleader = models.ForeignKey(CompanyLeader,on_delete=models.CASCADE, null=True,blank=True)
    project_name = models.CharField(max_length=255,verbose_name='Project adi')
    employee_number = models.PositiveIntegerField(verbose_name='Isci sayi')
    industry = models.CharField(max_length=30, choices=industries, verbose_name='Company field')
    
    
    def __str__(self):
        return f'{self.project_name}'
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projectler'        


class ProjectDepartment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255,verbose_name='Department adi')
    description = models.TextField(verbose_name='Department haqqinda',null=True,blank=True)
    employee_number = models.PositiveIntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Company departamenti'
        verbose_name_plural = 'Company departamentleri'
    
    def get_compatencies(self):
        return SkillNorm.objects.filter(department=self)    


class DepartmentPosition(models.Model):
    name = models.CharField(max_length=20,verbose_name='Position adi')    
    description = models.TextField(verbose_name='Position haqqinda',null=True,blank=True)
    department = models.ForeignKey(ProjectDepartment,on_delete=models.CASCADE,null=True,blank=True,related_name='departmentpositions')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Company position'
        verbose_name_plural = 'Company positions'
    
    
        


        
class SkillNorm(models.Model):
    department = models.ForeignKey(ProjectDepartment,on_delete=models.CASCADE)
    position = models.ForeignKey(DepartmentPosition,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE)
    norm = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.department.name}-{self.skill.name}'
    
    class Meta:
        verbose_name = 'Sirket normasi'
        verbose_name_plural = 'Sirket normalari'
    

class User(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,verbose_name='User adi')
    surname = models.CharField(max_length=20,verbose_name='User soyadi')
    position = models.ForeignKey(DepartmentPosition,related_name='user',on_delete=models.CASCADE,verbose_name='User position')
    department = models.ForeignKey(ProjectDepartment,related_name='user',on_delete=models.CASCADE,verbose_name='User departmenti')
    
    
    def __str__(self):
        return f'{self.name}-{self.surname}'
    
    class Meta:
        ordering = ['-position']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        
    def get_hard_goal(self):
        hard_goal_skill = {}
        for x in Skill.objects.all():
            if UserSkill.objects.filter(skill=x):

                goal = UserSkill.objects.filter(skill=x).values('price')[0]['price']/SkillNorm.objects.filter(department=self.department,skill=x,position=self.position).values('norm')[0]['norm']
                if x.skilltype == 'Hard':
                    hard_goal_skill[x.name] = int(goal*100)
        if len(hard_goal_skill)>0:        
            hard_goal_skill['average'] = sum(hard_goal_skill.values())/len(hard_goal_skill.values())  
        else:
            hard_goal_skill['average'] = 0   
        return hard_goal_skill
    
    def get_soft_goal(self):
        soft_goal_skill = {}
        for x in Skill.objects.all():
            if UserSkill.objects.filter(skill=x):

                goal = UserSkill.objects.filter(skill=x).values('price')[0]['price']/SkillNorm.objects.filter(department=self.department,skill=x,position=self.position).values('norm')[0]['norm']
                if x.skilltype == 'Soft':
                    soft_goal_skill[x.name] = int(goal*100)
        if len(soft_goal_skill)>0:        
            soft_goal_skill['average'] = sum(soft_goal_skill.values())/len(soft_goal_skill.values())
        else:
            soft_goal_skill['average'] = 0
        return soft_goal_skill
    
    def get_goal(self):    
        soft,hard = self.get_soft_goal()['average'],self.get_hard_goal()['average']
        if soft == 0 or hard>100:
            soft = 100
        if hard == 0 or hard>100:
            hard = 100
        if self.position.name == 'Junior':
            return int((soft + hard*3)/4)
        if self.position.name == 'Specialist':
            return int((soft*4+hard*6)/10)
        if self.position.name == 'Senior':
            return int((soft+hard)/2)
        if self.position.name == 'Manager':
            return int((soft*6+hard*4)/10)
        if self.position.name == 'TopManager':
            return int((soft*3+hard)/4)
        return 'Set employee position'    
                    
            
            

    
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE,related_name='userskill')
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.user}-{self.price}'
    
    def save(self, *args, **kwargs):
        oldobject = UserSkill.objects.filter(user=self.user,skill=self.skill)
        if oldobject.exists():
            oldobject.delete()
        super(UserSkill, self).save(*args, **kwargs)
        
