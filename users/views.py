from django.shortcuts import reverse

from django.views.generic import (ListView, CreateView, DeleteView, UpdateView)

from users.models import Patients, Doctors



# -----------------------------------------------------------------------------------------------------
# Patients Views

class PatientsCreateView(CreateView):
    model = Patients
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'
  
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # add/create a new context variable called "table_title"
        # this variable can then be accessed on the template
        context['table_title'] = 'Add New Patient'
        return context
    def get_success_url(self):
        return reverse('patients-list')



class PatientsListView(ListView):
    model = Patients
    template_name = 'users/users_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Patients'
        context['objects_update'] = 'patients-update'
        context['objects_delete'] = 'patients-delete'
        return context


class PatientsDeleteView(DeleteView):
    model = Patients
    success_url = '/users/patients'
    template_name = 'users/confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Patient'
        name = Patients.objects.get(pk=self.kwargs.get('pk')).get_full_name()
        context['message'] = f'Are you sure you want to delete the patient "{name}"'
        context['cancel_url'] = 'patients-list'
        return context


class PatientsUpdateView(UpdateView):
    model = Patients
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('patients-list')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Update Patient'
        return context


# Doctors Views
# -----------------------------------------------------------------------------------------------------------------------------------------

class DoctorsCreateView(CreateView):
    model = Doctors
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('doctors-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Add New Doctor'
        return context

class DoctorsListView(ListView):
    model = Doctors
    template_name = 'users/users_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Doctors'
        context['objects_update'] = 'doctors-update'
        context['objects_delete'] = 'doctors-delete'
        return context


class DoctorsDeleteView(DeleteView):
    model = Doctors
    template_name = 'users/confirm_delete.html'

    def get_success_url(self):
        return reverse('doctors-list')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Doctor'
        name = Doctors.objects.get(pk=self.kwargs.get('pk')).get_full_name()
        context['message'] = f'Are you sure you want to delete the doctor "{name}"'
        context['cancel_url'] = 'doctors-list'
        return context


class DoctorsUpdateView(UpdateView):
    model = Doctors
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('doctors-list')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Update Doctor'
        return context
