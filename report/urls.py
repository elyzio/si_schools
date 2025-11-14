from django.urls import path
from report.views import *
from report.views.views_rep_adm import *

urlpatterns = [
    # Dashboards
    path('graphics/', ReportGrafikuADM, name='graphics_dashboard'),
    path('tables/', ReportTableADM, name='tables_dashboard'),

    # Student detail views
    path('students/dept-class/', student_dept_class_detail, name='student_dept_class_detail'),
    path('students/district/', student_district_detail, name='student_district_detail'),
    path('alumni/year-dept/', alumni_year_dept_detail, name='alumni_year_dept_detail'),

    # Teacher detail views
    path('teachers/district/', teacher_district_detail, name='teacher_district_detail'),
    path('teachers/level/', teacher_level_detail, name='teacher_level_detail'),
    path('teachers/subject/', teacher_subject_detail, name='teacher_subject_detail'),

    # Reports
    path('prof/xlsx/', ProfessorExcelReport, name='professor_excel_report'),
    path('prof/pdf/<content>/', ProfessorPDFReport, name='professor_pdf_report'),
    path('prof/pdf/detail/<professor_id>/', ProfessorDetailPDFReport, name='professor_pdf_detail_report'),
]