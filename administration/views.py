from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, UpdateView, FormView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group
from .forms import UserCreateForm, UserPasswordForm
from django.core.urlresolvers import reverse_lazy
from backorder_manager.models import Supplier
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404


# View when you click on 'Admin'
@user_passes_test(lambda u: u.is_superuser)
def administration(request):
    return render(request, 'administration/administration.html')


# View when you click on 'users' on the admin view
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    return render(request, 'administration/users.html')


# View when you click on 'groups' on the admin view
@user_passes_test(lambda u: u.is_superuser)
def groups(request):
    return render(request, 'administration/groups.html')


# View when you click on 'suppliers' on the admin view
@permission_required('backorder_manager.view_supplier')
def suppliers(request):
    return render(request, 'administration/suppliers.html')


# View when you click on 'create user' on the user view
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'administration/user-create.html'

    def form_valid(self, form):
        form.save()
        form.save_m2m()
        return redirect(reverse_lazy('administration:user_list'))


# View when you click on 'edit or delete user' on the user view
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'administration/user-list.html'
    fields = ['username', 'id', 'groups']


# This view deletes an user
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'administration/user-delete.html'
    success_url = reverse_lazy('administration:user_list')


# This view displays the form to update a user
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'groups']
    template_name = 'administration/user-update.html'
    success_url = reverse_lazy('administration:user_list')


# This view is used to change a user's password
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserPasswordView(FormView):
    form_class = UserPasswordForm
    template_name = 'administration/user-change-password.html'
    success_url = reverse_lazy('administration:user_list')

    def get_context_data(self, **kwargs):
        context = super(UserPasswordView, self).get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        user = get_object_or_404(
            User.objects.get(pk=user_id)
        )
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        return context

    def form_valid(self, form):
        user_id = self.kwargs['pk']
        password = form.cleaned_data['password1']
        user = get_object_or_404(
            User.objects.get(pk=user_id)
        )
        user.set_password(password)
        user.save()

        return redirect(reverse_lazy('administration:user_list'))


# This view shows the form to create a new group
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class GroupCreateView(CreateView):
    model = Group
    template_name = 'administration/group-create.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('administration:groups')


# This view is used when you click on 'edit or delete groups' in the groups view
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'administration/group-list.html'
    fields = ['name', 'id']


# View to delete a group
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'administration/group-delete.html'
    success_url = reverse_lazy('administration:group_list')


# This view displays the form to update a group
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'administration/group-update.html'
    success_url = reverse_lazy('administration:group_list')
    fields = ['name', 'permissions']


# Shows all suppliers when you click on 'edit or delete supplier' in the suppliers view
class SupplierListView(PermissionRequiredMixin, ListView):
    permission_required = 'backorder_manager.view_supplier'
    model = Supplier
    template_name = 'administration/supplier-list.html'
    fields = ['name', 'id']


# Shows the form to create a new supplier
class SupplierCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'backorder_manager.add_supplier'
    model = Supplier
    template_name = 'administration/supplier-create.html'
    fields = ['name', 'customer_number', 'email', 'phone']
    success_url = reverse_lazy('administration:supplier_list')


# Shows the form to update supplier information
class SupplierUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'backorder_manager.change_supplier'
    model = Supplier
    template_name = 'administration/supplier-update.html'
    fields = ['name', 'customer_number', 'email', 'phone']
    success_url = reverse_lazy('administration:supplier_list')


# Is used to delete a supplier
class SupplierDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'backorder_manager.delete_supplier'
    model = Supplier
    template_name = 'administration/supplier-delete.html'
    success_url = reverse_lazy('administration:supplier_list')
