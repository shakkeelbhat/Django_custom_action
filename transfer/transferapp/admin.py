from collections import OrderedDict
from typing import Any
from django.contrib import admin
from transferapp.models import Department, Employee
from django import forms
from django.shortcuts import render

from django.urls import path


class DepartmentChoiceForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all())


class EmployeeAdmin(admin.ModelAdmin):
    actions =['change_department']
    department_choice_form = DepartmentChoiceForm


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('change_department/', self.admin_site.admin_view(self.change_department), name='change_department'),
        ]
        return custom_urls + urls

    def change_department(self, request,queryset):
        if "do_action" in request.POST:
            form = self.department_choice_form(request.POST)
            if form.is_valid():
                department_id = form.cleaned_data['department']
                department = Department.objects.get(dept_name=department_id)
                queryset.update(department=department)
                self.message_user(request,"Department updated.")
                return
        else:
            self.message_user(request,"Select a valid department")
            form = self.department_choice_form()

            
        return render(request, 'department_changeForm.html',
                        {'department': u'Choose department',
                        'objects': queryset,
                        'form': form})
        
        
    change_department.short_description = "Change department to"


'''
#Departments as form pop up
class ChangeDepartmentForm(forms.Form):
    new_department = forms.ModelChoiceField(queryset=Department.objects.all())



class EmployeeAdmin(admin.ModelAdmin):

    list_display =('employee_name','department')
    change_department_form = ChangeDepartmentForm
    actions=['change_department']

    def change_department(self,request,queryset):

        print(request.POST)
        if 'apply' in request.POST:
            print(request.POST)
            form  = self.change_department_form(request.POST)
            
            if form.is_valid():
                selected_department = form.cleaned_data["new_department"]
                count = queryset.update(department=selected_department)

                self.message_user(request,"Department changed")
                return
            #submitted without  a department
            else:
                    form = self.change_department_form()
                    context  = {
                        'form':form,
                        'queryset':queryset,
                    }
            return self.changeform_view(request,context)




#Without a separate 2nd dropdown for  list of departments
#changelist_view > get_actions > 
def moveto_DepartmentAction(department):
    def move_to_Department(self, request, queryset):
        for employee in queryset:
           employee.assign_to(department)
    if department is not None:      
        move_to_Department.short_description ="Assign to {0}".format(department.dept_name)
        move_to_Department.__name__ = 'move_to_Department_{0}'.format(department.dept_name)
    else:
        move_to_Department.short_description ="Remove department"

        move_to_Department.__name__ = 'remove department'

    return move_to_Department
            


class EmployeeAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(EmployeeAdmin,self).get_actions(request)

        for dept in Department.objects.all().order_by('dept_name'):
            action = moveto_DepartmentAction(dept)
            actions[action.__name__] = (action,action.__name__,action.short_description)
        #set as blank
        action=moveto_DepartmentAction(None)    
        actions[action.__name__]=(action,action.__name__,action.short_description)

        return actions
 '''             
class DepartmentInline(admin.StackedInline):#or StackedInline
    model = Employee

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [DepartmentInline,]
##################################




              
'''
class MoveToDepartment(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

@admin.action(description="Move to department")
def moveto_Department(modeladmin,request, queryset):
    department = request.POST["department"]
    if department:
        department = Department.objects.get(id=department)
        for emp in queryset:
            emp.assign_to(department)


        modeladmin.message_user(request, f"Selected {queryset.count()} employees moved to {department}")
    else:
        modeladmin.message_user(request, "Please select a department", level="error")

class EmployeeAdmin(admin.ModelAdmin):
    list_display =["employee_name","department"]
    actions = [moveto_Department]

    def changelist_view(self, request, extra_context=None):
        if request.method =="POST" and request.POST.get("action") == "moveto_department":
            return self.response_action(request)
        
        else:
            return super().changelist_view(request, extra_context)

    def render_change_form(self, request, context, *args, **kwargs):
        context["form"] = MoveToDepartment()
        return super().render_change_form(request, context, *args, **kwargs)





    

'''

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department,DepartmentAdmin)


