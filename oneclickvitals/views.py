from django.shortcuts import render, get_object_or_404, redirect, render_to_response, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from oneclickvitals.models import * 
#Appointment, PageAdmin, UserDetail, EmergencyContact, PatientMedicalHistory, Radiology, DoctorDetail, PharmacyDetail, Prescription
from oneclickvitals.forms import * 
#UserForm, UserDetailForm, NewPatientForm, AppointmentForm, EmergencyContactForm, PatientMedicalHistoryForm, PatientRadiologyImageForm, DoctorDetailForm, PharmacyDetailForm, PrescriptionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.contrib import auth
from medical_project.settings import MEDIA_URL, MEDIA_ROOT
from django.utils import timezone
from django.template import RequestContext
from django.contrib import messages
from medical_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage
import smtplib



def is_patient(user):
    return user.groups.filter(name="patient").exists()

def is_doctor(user):
    return user.groups.filter(name="doctor").exists()

def is_staff(user):
    return user.groups.filter(name="staff").exists()


def index(request):
    return render(request, 'index.html')

def index_patient(request):
    me = request.user
    pharmacy = PharmacyDetail.objects.get(user=me)
    return render(request, 'index_patient.html', {'pharmacy': pharmacy})

def index_doctor(request):
    return render(request, 'index_doctor.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:

            if user.groups.filter(name="patient").exists():
                # Correct password, and the user is marked "active"
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/patient/")
                
            else:
                # Correct password, and the user is marked "active"
                login(request, user)
                return HttpResponseRedirect("/oneclickvitals/")
        else:
            return render(request, "registration/invalid_login.html")
    else:
        return render(request, 'registration/login.html')



def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return render(request, 'registration/logout.html')

def invalid_login_view(request):
    if not user.is_authenticated():
         return render(request, 'registration/invalid_login.html')


def about(request):
    #appointment_list = Appointment.objects.order_by('appointment_date')
    #context_dict = {'appointments': appointment_list}
    return render(request, 'oneclickvitals/about.html')

def add_newpatient(request):
    if request.method == 'POST':
        formA = NewPatientForm(request.POST)
        formB = UserDetailForm(request.POST)
        formC = EmergencyContactForm(request.POST)
        formD = PatientMedicalHistoryForm(request.POST)
        formE = FamilyMedicalHistoryForm(request.POST)
        formF = PharmacyDetailForm(request.POST)
        
        if formA.is_valid() and formB.is_valid() and formC.is_valid() and formD.is_valid() and formE.is_valid() and formF.is_valid():
            # Save the new category to the database.
            patientUser = formA.save(commit=False)
            patientUser.save()
            patientInfo = formB.save(commit=False)
            patientInfo.user = patientUser
            patientInfo.save()
            emergencyContact = formC.save(commit = False)
            emergencyContact.user = patientUser
            emergencyContact.save()
            patientMedicalHistory = formD.save(commit = False)
            patientMedicalHistory.user = patientUser
            patientMedicalHistory.save()
            familyMedicalHistory = formE.save(commit = False)
            familyMedicalHistory.user = patientUser
            familyMedicalHistory.save()
            pharmacy = formF.save(commit = False)
            pharmacy.user = patientUser
            pharmacy.save()
            patientUser.groups.add(Group.objects.get(name='patient'))

            # The user will be shown the patient profile page view.
            return patient_details(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            #print(formA.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        formA = NewPatientForm()
        formB = UserDetailForm()
        formC = EmergencyContactForm()
        formD = PatientMedicalHistoryForm()
        formE = FamilyMedicalHistoryForm()
        formF = PharmacyDetailForm()
        
    # Render the form with error messages (if any), if no form supplied
    return render(request, 'oneclickvitals/add_newpatient.html', {'formA': formA, 'formB': formB, 'formC': formC, 'formD': formD, 'formE': formE, 'formF': formF})

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            appointment = form.save(commit=False)
            appointment.save()

            # The user will be shown the appointment detail page view.
            return appointment_details(request)
        else:
            #print (form.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        form = AppointmentForm()

    # Render the form with error messages (if any)
    return render(request, 'oneclickvitals/appointment.html', {'form': form})

@login_required
def patient_details(request):
    details_list = UserDetail.objects.all()

    return render(request, 'oneclickvitals/patient_details.html', {'details': details_list})

@login_required
def appointment_details(request):
    appointment_list = Appointment.objects.all()
    return render(request, 'oneclickvitals/appointment_details.html', {'appointment': appointment_list})



@login_required
def patient_profile(request, pk):
    me = User.objects.get(id=pk)
    profile = UserDetail.objects.get(user=me)
    #profile_list = UserDetail.objects.all()
    emergency_contact= EmergencyContact.objects.get(user=me)
    medical_history = PatientMedicalHistory.objects.get(user=me)
    family_history = FamilyMedicalHistory.objects.get(user=me)
    pharmacy = PharmacyDetail.objects.get(user=me)
    vitalsigns_info = VitalSigns.objects.filter(user=me).latest('visit_date') 
    diagnosis_info = Diagnosis.objects.filter(patient=me).latest('diagnosis_date')
    context_dict = {'profile':profile, 'emergency': emergency_contact, 'medical_history': medical_history, 'family_history': family_history,'pharmacy': pharmacy,'vitalsigns_info': vitalsigns_info,'diagnosis_info': diagnosis_info}
    #print("in patient profile: ", diagnosis_info[0].date)
    return render(request, 'oneclickvitals/patient_profile.html', context_dict)

@login_required
def personal_appointment(request):
    me = request.user
    appointment_list = Appointment.objects.all()
    pharmacy = PharmacyDetail.objects.get(user=me)
    return render(request, 'oneclickvitals/personal_appointment.html', {'appointment': appointment_list, 'pharmacy': pharmacy})

def profile_edit(request, pk):
    profile = get_object_or_404(UserDetail, pk=pk)
    if request.method == "POST":
        form = UserDetailForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            #profile.author = request.user
            profile.save()
            return redirect('oneclickvitals.views.patient_profile', pk=profile.pk)
        else:
            #print(form.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        form = UserDetailForm(instance=profile)
    return render(request, 'oneclickvitals/edit_patient.html', {'form': form})

@login_required
def personal_profile(request):
    #me = User.objects.get(id=pk)
    me = request.user
    #print (me.username)
    profile = UserDetail.objects.get(user=me)
    #profile_list = UserDetail.objects.all()
    emergency_contact= EmergencyContact.objects.get(user=me)
    medical_history = PatientMedicalHistory.objects.get(user=me)
    family_history = FamilyMedicalHistory.objects.get(user=me)
    pharmacy = PharmacyDetail.objects.get(user=me)
    vitalsigns_info = VitalSigns.objects.filter(user=me)
    diagnosis_info = Diagnosis.objects.filter(patient=me)
    context_dict = {'profile':profile, 'emergency': emergency_contact, 'medical_history': medical_history,'family_history': family_history, 'pharmacy': pharmacy, 'vitalsigns_info': vitalsigns_info, 'diagnosis_info':diagnosis_info }
    #print("in patient profile: ", profile.pharmacy_name)
    return render(request, 'oneclickvitals/personal_profile.html', context_dict)


def edit_patient(request, pk):
    newpatient_instance = get_object_or_404(User, pk=pk)
    userdetail_instance = get_object_or_404(UserDetail, pk=pk)
    emergencycontact_instance = get_object_or_404(EmergencyContact, pk=pk)
    patientmedicalhistory_instance = get_object_or_404(PatientMedicalHistory, pk=pk)
    familymedicalhistory_instance = get_object_or_404(FamilyMedicalHistory, pk=pk)
    if request.method == 'POST':
        formA = NewPatientForm(request.POST, instance = newpatient_instance)
        formB = UserDetailForm(request.POST, instance = userdetail_instance)
        formC = EmergencyContactForm(request.POST, instance = emergencycontact_instance)
        formD = PatientMedicalHistoryForm(request.POST, instance = patientmedicalhistory_instance)
        formE = FamilyMedicalHistoryForm(request.POST, instance = familymedicalhistory_instance)
        formF = PharmacyDetailForm(request.POST)

        if formA.is_valid() and formB.is_valid() and formC.is_valid():
            # Save the new category to the database.
            patientUser = formA.save()
            patientInfo = formB.save(commit=False)
            patientInfo.user = patientUser
            patientInfo.save()
            emergencyContact = formC.save(commit = False)
            emergencyContact.user = patientUser
            emergencyContact.save()
            patientMedicalHistory = formD.save(commit = False)
            patientMedicalHistory.user = patientUser
            patientMedicalHistory.save()
            familyMedicalHistory = formE.save(commit = False)
            familyMedicalHistory.user = patientUser
            familyMedicalHistory.save()
            pharmacy = formF.save(commit = False)
            pharmacy.user = patientUser
            pharmacy.save()
            patientUser.groups.add(Group.objects.get(name='patient'))
            print("saved new patient")

            # The user will be shown the patient profile page view.
            return patient_details(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            #print(formA.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        formA = NewPatientForm(instance = newpatient_instance)
        formB = UserDetailForm(instance = userdetail_instance)
        formC = EmergencyContactForm(instance = emergencycontact_instance)
        formD = PatientMedicalHistoryForm(instance = patientmedicalhistory_instance)
        formE = FamilyMedicalHistoryForm(instance = familymedicalhistory_instance)
        formF = PharmacyDetailForm()
        
    # Render the form with error messages (if any), if no form supplied
    return render(request, 'oneclickvitals/edit_patient.html', {'formA': formA, 'formB': formB, 'formC': formC, 'formD': formD, 'formE': formE, 'formF': formF})

@login_required
def add_lab_test(request):
    if request.method == 'POST':
        formK = LabTestForm(request.POST)

        if formK.is_valid():
            # Save the new category to the database.
            lab_test = formK.save(commit=False)
            lab_test.save()

            # The user will be shown the appointment detail page view.
            #return diagnosis_details(request)
            #print ("Do I have the user id: ", diagnosis.pk)
            return diagnosis_details(request, diagnosis.pk)
        else:
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
            #print (formK.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        formK = LabTestForm()

    # Render the form with error messages (if any)
    return render(request, 'oneclickvitals/add_lab_test.html', {'formK': formK})

def vitalsigns(request):
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            vitalsigns = form.save(commit=False)
            vitalsigns.save()

            # The user will be shown the appointment detail page view.
            #return diagnosis_details(request)
            print ("Do I have the user id: ", vitalsigns.pk)
            #return redirect ('vitalsigns_list')
            return vitalsigns_list(request)
        else:
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
            #print (form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = VitalSignsForm()

    # Render the form with error messages (if any)
    return render(request, 'oneclickvitals/vitalsigns.html', {'form': form})

def vitalsigns_details(request, pk):
    #me = User.objects.get(id=pk)
    vitalsigns_info = get_object_or_404(VitalSigns, pk=pk)
    return render(request, 'oneclickvitals/vitalsigns_details.html', {'vitalsigns_info': vitalsigns_info})

def vitalsigns_list(request):
    vitalsigns = VitalSigns.objects.all()
    return render(request, 'oneclickvitals/vitalsigns_list.html', {'vitalsigns': vitalsigns})
    

def visit_records(request):
    diagnosis = Diagnosis.objects.all()
    return render(request, 'oneclickvitals/visit_records.html', {'diagnosis':diagnosis})

def diagnosis(request, pk):
    vitalsigns_info = get_object_or_404(VitalSigns, pk=pk)
    #diagnosis should be connected to vital signs of the current visit
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            diagnosis = form.save(commit=False)
            diagnosis.save()

            # The user will be shown the appointment detail page view.
            #return diagnosis_details(request)
            print ("Do I have the user id: ", diagnosis.pk)
            return diagnosis_details(request, diagnosis.pk)
        else:
            #print (form.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        form = DiagnosisForm()

    # Render the form with error messages (if any)
    return render_to_response('oneclickvitals/diagnosis.html', {'vitalsigns_info': vitalsigns_info, 'form': form}, context_instance=RequestContext(request))


def diagnosis_details(request, pk):
    #me = User.objects.get(id=pk)
    diagnosis_info = get_object_or_404(Diagnosis, pk=pk)
    return render(request, 'oneclickvitals/diagnosis_details.html', {'diagnosis_info': diagnosis_info})


def personal_diagnosis(request):
    me = request.user
    diagnosis_info = Diagnosis.objects.filter(patient=me)
    pharmacy = PharmacyDetail.objects.get(user=me)
    return render(request, 'oneclickvitals/personal_diagnosis.html', {'diagnosis_info': diagnosis_info, 'pharmacy':pharmacy})


@login_required
def patient_radiology_image(request):
    if request.method == 'POST':
        form = PatientRadiologyImageForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the new image to the database.
            radiology_image = form.save(commit=False)
            radiology_image.save()

            # The user will be shown the radiology list.
            #messages.success(request, 'Radiology image added.')
        
            return redirect('radiology_list')
        else:
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
            
#            print (form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = PatientRadiologyImageForm()

    # Render the form with error messages (if any)
    return render(request, 'oneclickvitals/add_radiology.html', {'form': form})

@login_required
def radiology_list(request):
    radiology_images = Radiology.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'oneclickvitals/radiology_list.html', {'radiology_images': radiology_images})
        

@login_required
def view_radiology(request, pk):
    img = get_object_or_404(Radiology, pk=pk)
    return render_to_response('oneclickvitals/view_radiology.html', {'img':img}, context_instance=RequestContext(request) )

@login_required
def edit_radiology(request, pk):
    img = get_object_or_404(Radiology, pk=pk)
    if request.method == 'POST':
        form = PatientRadiologyImageForm(request.POST, instance=img)

        if form.is_valid():
            # Save the new image to the database.
            radiology_image = form.save(commit=False)
            radiology_image.save()

            # The user will be shown the image list.
            return redirect('view_radiology', pk=img.pk)
        else:
            #print (form.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        form = PatientRadiologyImageForm(instance=img)

    # Render the form with error messages (if any)
    return render(request, 'oneclickvitals/edit_radiology.html', {'form': form})

@login_required
def add_prescription(request):
    if request.method == 'POST':
        
        form = PrescriptionForm(request.POST)
        
        
        if form.is_valid():
            prescriptionDetail = form.save(commit=False)
            prescriptionDetail.save()
            
            #messages.success(request, 'Prescription added.')
            return redirect('prescription_list')
        else:
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        form = PrescriptionForm()
        

    # Render the form with error messages (if any), if no form supplied
    return render(request, 'oneclickvitals/add_prescription.html', {'form': form })


def prescription_list(request):
    prescription = Prescription.objects.all()
    return render(request, 'oneclickvitals/prescription_list.html', {'prescription': prescription})
 

def prescription_details(request, pk):
    me = User.objects.get(id=pk)
    profile = UserDetail.objects.filter(user=me)
    print("profile: " + str(profile))
    #print("profile.user:",profile.user.first_name)
    prescription = Prescription.objects.filter(user=me)
    pharmacy = PharmacyDetail.objects.filter(user=me)
    doctor = DoctorDetail.objects.all()[0]
    context_dict = {'profile':profile, 'prescription': prescription, 'pharmacy':pharmacy, 'doctor': doctor}
    return render(request, 'oneclickvitals/prescription_details.html', context_dict)


def personal_prescription(request):
    me = request.user
    prescription_info = Prescription.objects.filter(user=me)
    pharmacy = PharmacyDetail.objects.get(user=me)
    context_dict = {'prescription_info': prescription_info, 'pharmacy': pharmacy }
    return render(request, 'oneclickvitals/personal_prescription.html',context_dict)

def visit_summary(request):
    me = request.user
    #form = SummaryForm(request.POST)
    appointment_list = Appointment.objects.filter(user=me)
    prescription_info = Prescription.objects.filter(user=me)
    diagnosis_info = Diagnosis.objects.filter(patient=me)
    context_dict = {'appointment_list': appointment_list, 'prescription_info': prescription_info, 'diagnosis_info':diagnosis_info }

    return render(request, 'oneclickvitals/visit_summary.html', context_dict)

def add_doctor_information(request):
    if request.method == 'POST':
        form = DoctorDetailForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            doctorDetail = form.save(commit=False)
            doctorDetail.save()

            # The user will be shown the appointment detail page view.
            return view_doctor_information(request)
        else:
            #print (form.errors)
            messages.error(request, "Oops! You missed some fields. Please fill the required fields.")
    else:
        # If the request was not a POST, display the form to enter details.
        form = DoctorDetailForm()

    # Render the form with error messages (if any)
    return render(request, 'oneclickvitals/add_doctor_information.html', {'form': form})
    
@login_required
def view_doctor_information(request):
    doctor_details = DoctorDetail.objects.all()[0]
    return render(request, 'oneclickvitals/view_doctor_information.html', {'doctor_details':doctor_details})    


    
    
    