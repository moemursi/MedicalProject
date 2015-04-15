from django import forms
from django.contrib.auth.models import User, Group
from oneclickvitals.models import Appointment,UserDetail, EmergencyContact, PatientMedicalHistory, Radiology, DoctorDetail, PharmacyDetail, Prescription
from datetimewidget.widgets import DateWidget, DateTimeWidget, TimeWidget

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        widgets = {'date_of_birth': DateWidget(attrs={'id':"yourdateid"}, usel10n = True, bootstrap_version=3)}
        fields = ('date_of_birth','insurance','phone_number','address','city',)

class NewPatientForm(forms.ModelForm):

    class Meta:
        # Provide an association between the ModelForm and a model
        model = User
        fields = ('username','first_name','last_name','email', 'password', 'groups',)

class AppointmentForm(forms.ModelForm):

    #appointment_date = forms.DateTimeField(widget = DateTimeWidget(usel10n = True, bootstrap_version = 3))
    class Meta:
        model = Appointment
        widgets = {'appointment_date': DateWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3),
                  'appointment_time': TimeWidget(attrs= {'id':"yourtimeid"}, usel10n = True, bootstrap_version=3)}
        fields = ('user','reason', 'phone_number','appointment_date','appointment_time',)

class EmergencyContactForm(forms.ModelForm):

    class Meta:
        # Provide an association between the ModelForm and a model
        model = EmergencyContact
        fields = ('first_name','last_name','relationship', 'phone_number', 'address','city',)

class PatientMedicalHistoryForm(forms.ModelForm):

    class Meta:
        # Provide an association between the ModelForm and a model
        model = PatientMedicalHistory
        fields = ('allergies','current_medications','chief_complaint', 'surgical_history', 'medical_history','social_habits',)

class PatientRadiologyImageForm(forms.ModelForm):
    
    class Meta:
        model = Radiology
        widgets = {
            'created_date': DateWidget(attrs={'id':"yourcreateddateid"}, usel10n = True, bootstrap_version=3)}
        fields = ('user', 'title', 'created_date', 'caption', 'image',)
        
        
class DoctorDetailForm(forms.ModelForm):
    class Meta:
        model = DoctorDetail
        fields = ('doctor_first_name', 'doctor_last_name', 'name_suffix', 'prescription_network_id', 'dea', 'doctor_phone_number', 'doctor_address', 'doctor_city',)
        
class PharmacyDetailForm(forms.ModelForm):
    class Meta:
        model = PharmacyDetail
        fields = ('pharmacy_name', 'pharmacy_address', 'pharmacy_city', 'pharmacy_phone_number', 'ncpdp_id','pharmacy_email',)
        
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        widgets = {
            'date_of_issuance': DateWidget(attrs={'id':"yourissuancedate"}, usel10n = True, bootstrap_version=3)}
        fields = ('patient', 'gender', 'date_of_issuance', 'day_supply', 'drug_name', 'drug_strength', 'dosage_form', 'frequency', 'quantity', 'npi_number', 'ndc_number', 'refills',)