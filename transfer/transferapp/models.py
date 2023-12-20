from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    dept_name = models.CharField(max_length=100,blank=False, null=True,unique=True)


    def __str__(self):
        return  self.dept_name

class Employee(models.Model):
    employee_name = models.CharField(max_length=100,blank=False,null=False)
    #employee_name = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey("Department",blank=True,null=True,to_field="dept_name",on_delete=models.CASCADE,related_name="departments",default=None)
    def __str__(self):
        if self.department:
                return f"{self.employee_name} ({self.department})"
        else:
            return self.employee_name

    def assign_to(self,department):
        self.department = department
        self.save()
