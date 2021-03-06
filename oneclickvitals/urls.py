from django.conf.urls import patterns, url
from oneclickvitals import views
from django.conf import settings
from django.conf.urls.static import static
from oneclickvitals.views import view_radiology
from medical_project.settings import MEDIA_ROOT


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^add_newpatient/$', views.add_newpatient, name='add_newpatient'),
        url(r'^appointment/$', views.appointment, name='appointment'),
        url(r'^patient_details/$', views.patient_details, name='patient_details'),
        url(r'^appointment_details/$', views.appointment_details, name='appointment_details'),

        url(r'^personal_appointment/$', views.personal_appointment, name='personal_appointment'),

        url(r'^add_radiology/$', views.patient_radiology_image, name='patient_radiology_image'),
        url(r'^radiology_list/$', views.radiology_list, name='radiology_list'),
        url(r'^view_radiology/(?P<pk>[0-9]+)/$', views.view_radiology, name='view_radiology'),
        url(r'^view_radiology/(?P<pk>[0-9]+)/edit/$', views.edit_radiology, name='edit_radiology'),
        url(r'^add_prescription/$', views.add_prescription, name='add_prescription'),
        url(r'^prescription_list/$', views.prescription_list, name='prescription_list'),

        url(r'^personal_prescription/$', views.personal_prescription, name='personal_prescription'),
        url(r'^prescription_details/(?P<pk>[0-9]+)/$', views.prescription_details, name='prescription_details'),
        url(r'^visit_summary/$', views.visit_summary, name='visit_summary'),
        url(r'^vitalsigns/$', views.vitalsigns, name='vitalsigns'),
        url(r'^vitalsigns_list/$', views.vitalsigns_list, name='vitalsigns_list'),
        url(r'^vitalsigns_details/(?P<pk>[0-9]+)/$', views.vitalsigns_details, name='vitalsigns_details'),
        url(r'^visit_records/$', views.visit_records, name='visit_records'),
        url(r'^diagnosis/(?P<pk>[0-9]+)/$', views.diagnosis, name='diagnosis'),
        url(r'^diagnosis_details/(?P<pk>[0-9]+)/$', views.diagnosis_details, name='diagnosis_details'),
        url(r'^patient_profile/(?P<pk>[0-9]+)/$', views.patient_profile,name='patient_profile'),
        url(r'^profile/(?P<pk>[0-9]+)/edit/$', views.edit_patient, name='edit_patient'),
        url(r'^personal_profile/$', views.personal_profile, name='personal_profile'),
        url(r'^personal_diagnosis/$', views.personal_diagnosis, name='personal_diagnosis'),
        url(r'^add_doctor_information/$', views.add_doctor_information, name='add_doctor_information'),
        url(r'^view_doctor_information/$', views.view_doctor_information, name='view_doctor_information'),
        url(r'^add_lab_test/$', views.add_lab_test, name='add_lab_test'),
        url(r'^labtest_list/$', views.labtest_list, name='labtest_list'),
        url(r'^personal_labtest/$', views.personal_labtest, name='personal_labtest'),
        url(r'^personal_labresult/$', views.personal_labresult, name='personal_labresult'),
        #url(r'^results/$', views.add_result, name='add_result'),
        url(r'^add_lab_result/(?P<pk>[0-9]+)/$', views.add_lab_result, name='add_lab_result'),
        url(r'^result_list/$', views.result_list, name='result_list'),
        url(r'^result_details/(?P<pk>[0-9]+)/$', views.result_details, name='result_details'),
        url(r'^visit_summary/(?P<pk>[0-9]+)/$', views.visit_summary, name='visit_summary'),
        url(r'^zing/$', views.zing, name='zing'),
                     )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
