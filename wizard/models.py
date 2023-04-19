from django.db import models
from account.utils import create_slug_shortcode
from django.contrib.auth import get_user, get_user_model
from django.db.models import Q

User = get_user_model()

skilltype=(
    ('Soft','Soft'),
    ('Hard','Hard'),
)

industries=(
    ('IT','IT'),
    ('Construction','Construction'),
)

class Hirponorms(models.Model):
    skill = models.CharField(max_length=255,verbose_name='Bacariq')
    skilltype = models.CharField(choices=skilltype,max_length=5,null=True,blank=True,verbose_name='skilltype')
    department = models.CharField(max_length=255,verbose_name='Department')
    position = models.CharField(max_length=255,verbose_name='Position')
    norm = models.IntegerField()
    
    def __str__(self):
        return f'{self.department}-{self.position}-{self.skill}'
    


"""{"companyleader": 110, "project_name": "TEST","employee_number": 25, "industry": "IT", "objects": [{"name": "TEST","employee_number":3},{"name": "TEWST","employee_number":3},{"name": "TESTT","employee_number":3}]}"""

class Project(models.Model):
    project_name = models.CharField(max_length=255,verbose_name='Project adi')
    employee_number = models.PositiveIntegerField(verbose_name='Isci sayi')
    industry = models.CharField(max_length=30, choices=industries, verbose_name='Company field')
    companyLeader = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="project")
    
    def __str__(self):
        return f'{self.project_name}'
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    
class Period(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name="period")
    period_number= models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    period_position = models.CharField(max_length=150,null=True,blank=True)
    
    def __str__(self):
        return self.project.project_name
    
    class Meta:
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'


class Evaluation_frequency(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE,related_name='frequency')
    start_date = models.DateField()
    end_date = models.DateField()
    
    
class ProjectDepartment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True,related_name='departments')
    name = models.CharField(max_length=255,verbose_name='Department adi')
    description = models.TextField(verbose_name='Department haqqinda',null=True,blank=True)
    employee_number = models.PositiveIntegerField(null=True,blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        
    def get_allSkills(self):
        Skills = []
        for y in self.departmentpositions.all():
            
            for x in MainSkill.objects.filter(position=y):
                Skills.append({"id":x.id,"name":x.name,'type':x.skilltype,"weight":x.weight,'position':x.position.id})
        return Skills
    
    
        
    # def get_compatencies(self,obj):
    #     competencies = []
    #     for y in obj.departmentpositions.all():           
    #         for norm in MainSkill.objects.filter(position=y,position__department__id=obj.id):
    #             competencies.append({'id':norm.id,'weight':norm.weight,'norm':norm.norm,'position':{'name':y.name,'id':y.id,'department':obj.id},'department':{'name':obj.name,'id':obj.id,'project':obj.project.id},'skill':{'name':norm.name,'id':norm.id,'department':norm.position.department.id}})
    #     return competencies
          
    def get_compatencies(self):
        comptencies = []
        position = DepartmentPosition.objects.filter(department=self)
        for y in position:
            for c in MainSkill.objects.filter(position=y):
                comptencies.append({'norm':c.norm,"id":c.id,"department":{"name":c.position.department.name,"id":c.position.department.id},'skill':{"name":c.name,"id":c.id},'position':{'name':c.position.name,'id':c.position.id}})
        return comptencies
    
    
class DepartmentPosition(models.Model):
    name = models.CharField(max_length=20,verbose_name='Position adi')    
    description = models.TextField(verbose_name='Position haqqinda',null=True,blank=True)
    department = models.ForeignKey(ProjectDepartment,on_delete=models.CASCADE,null=True,blank=True,related_name='departmentpositions')
    report_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.department.name} - {self.department.project.project_name}"
    
    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        
        
    
        

class MainSkill(models.Model):
    name = models.CharField(max_length=255,verbose_name='Bacariq adi')
    skilltype = models.CharField(choices=skilltype,max_length=5,null=True,blank=True,verbose_name='skilltype')
    description = models.TextField(null=True,blank=True)
    position = models.ForeignKey(DepartmentPosition, on_delete=models.CASCADE)
    norm = models.PositiveIntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return f'{self.name}-{self.position.name}' 
       
    class Meta:
        verbose_name = 'Main SKill'
        verbose_name_plural = 'Main Skills'
        
        
        
    # def save(self, *args, **kwargs):
    #     oldobject = SkillNorm.objects.filter(position__name=self.position.name,skill__name=self.skill.name,position__department=self.position.department)
    #     print(self.position,self.skill)

    #     if oldobject.exists():
    #         print(oldobject)
    #         oldobject.delete()
    #     super(SkillNorm, self).save(*args, **kwargs)
    

class Employee(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,related_name='employee',on_delete=models.SET_NULL)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='employee',null=True,blank=True)
    first_name = models.CharField(max_length=20,verbose_name='User adi',null=True,blank=True)
    last_name = models.CharField(max_length=20,verbose_name='User soyadi',null=True,blank=True)
    position = models.ForeignKey(DepartmentPosition,related_name='user',on_delete=models.CASCADE,verbose_name='position level',null=True,blank=True)
    salary = models.PositiveIntegerField(null=True,blank=True)
    hire_date = models.DateField(null=True,blank=True,auto_now_add=True)
    is_systemadmin = models.BooleanField(default=False,null=True,blank=True)
    positionName = models.CharField(max_length=40,null=True,blank=True)
    phone = models.PositiveIntegerField(null=True,blank=True)
    report_to = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return f'{self.user}-'
    
    class Meta:
        ordering = ['-position']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def get_compatencies(self):
        comptencies = []
        for c in MainSkill.objects.filter(position=self.position):
            comptencies.append({'weight':c.weight,"skilltype":c.skilltype,'norm':c.norm,"id":c.id,'skill':{"name":c.name,"id":c.id}})
        return comptencies
    
    def get_total_score(self):
        cowerker,selfscore,sub,manager = [],[],[],[]
        for x in self.skills.all():
            if x.employee.report_to == x.rater.report_to:
                cowerker.append(x.skill.weight*(x.price/x.norm))
            elif x.employee.report_to == x.rater:
                manager.append(x.skill.weight*(x.price/x.norm))
            elif x.employee == x.rater.report_to:
                sub.append(x.skill.weight*(x.price/x.norm))
            elif x.employee == x.rater:
                selfscore.append(x.skill.weight*(x.price/x.norm))
            else:
                pass
            
        result = {}
        result['cowerker'] = sum(cowerker)/len(cowerker)
        result['selfscore'] = sum(selfscore)/len(selfscore)
        result['sub'] = sum(sub)/len(sub)
        result['manager'] = sum(manager)/len(manager)
        result['total'] = result['cowerker']*0.3+result['selfscore']*0.1+result['sub']*0.2+result['manager']*0.4
        return result
    
    # def get_hard_goal(self):
    #     hard_goal_skill = {}
    #     for x in MainSkill.objects.all():
    #         if UserSkill.objects.filter(skill=x):

    #             goal = UserSkill.objects.get(skill=x).price/MainSkill.objects.get(skill=x,position=self.position).norm
    #             if x.skilltype == 'Hard':
    #                 hard_goal_skill[x.name] = int(goal*100)
    #     if len(hard_goal_skill)>0:        
    #         hard_goal_skill['average'] = sum(hard_goal_skill.values())/len(hard_goal_skill.values())  
    #     else:
    #         hard_goal_skill['average'] = 0   
    #     return hard_goal_skill
    
    
    # def get_soft_goal(self):
    #     soft_goal_skill = {}
    #     for x in MainSkill.objects.all():
    #         if UserSkill.objects.filter(skill=x):

    #             goal = UserSkill.objects.get(skill=x).price/MainSkill.objects.get(skill=x,position=self.position).norm
    #             if x.skilltype == 'Soft':
    #                 soft_goal_skill[x.name] = int(goal*100)
    #     if len(soft_goal_skill)>0:        
    #         soft_goal_skill['average'] = sum(soft_goal_skill.values())/len(soft_goal_skill.values())
    #     else:
    #         soft_goal_skill['average'] = 0
    #     return soft_goal_skill
    
    # def get_goal(self):    
    #     soft,hard = self.get_soft_goal()['average'],self.get_hard_goal()['average']
    #     if self.position:
    #         if soft == 0 or hard>100:
    #             soft = 100
    #         if hard == 0 or hard>100:
    #             hard = 100
    #         if self.position.name == 'Junior':
    #             return int((soft + hard*3)/4)
    #         if self.position.name == 'Specialist':
    #             return int((soft*4+hard*6)/10)
    #         if self.position.name == 'Senior':
    #             return int((soft+hard)/2)
    #         if self.position.name == 'Manager':
    #             return int((soft*6+hard*4)/10)
    #         if self.position.name == 'TopManager':
    #             return int((soft*3+hard)/4)
    #         return 'Set employee position'    
                    
class AllScores(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='myscore')
    rater = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='mycomment')
    evaluation_frequency = models.ForeignKey(Evaluation_frequency,on_delete=models.CASCADE,related_name='freq')
    is_visible = models.BooleanField(default=False)
            
class UserSkill(models.Model):
    card = models.ForeignKey(AllScores,on_delete=models.CASCADE)
    skill = models.ForeignKey(MainSkill, on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)
    price = models.PositiveIntegerField()
    
    
    def __str__(self):
        return f'{self.user}-{self.price}'
    
    def position_weight(self):
        if self.employee.report_to == self.rater.report_to:
            return {"rank":"cowerker","rankweight":30}
        elif self.employee.report_to == self.rater:
            return {"rank":"manager","rankweight":40}
        elif self.employee == self.rater.report_to:
            return {'rank':'sub',"rankweight":20}
        elif self.employee == self.rater:
            return {'rank':'selfscore',"rankweight":10}
        else:
            return {'rank':'undefined',"rankweight":0}
    
    def save(self, *args, **kwargs):
        oldobject = UserSkill.objects.filter(user=self.user,skill=self.skill,evaluation_frequency=self.evaluation_frequency)
        if oldobject.exists():
            print(oldobject)
            
            oldobject.delete()
        super(UserSkill, self).save(*args, **kwargs)
        

