from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date
from calendar import monthrange
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum

from .forms import *
from .forms import *
from .decorators import *

def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

def register_company(request):
    form = CompanyForm()
    heading = 'Register'

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.joining_date = datetime.now()
            fs.save()
            request.session['company_contact'] = form.cleaned_data.get('contact_number')

            return redirect('register_user')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/company/company.html', context)

def update_company(request):
    company = get_object_or_404(Company, id = request.user.company_name.id)
    form = CompanyUpdateForm(instance = company)
    heading = 'Update Company'

    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance = company)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = datetime.now()
            fs.save()

            return redirect('home')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/member/member.html', context)


def register_user(request):
    form = CustomUserRegistrationForm()
    heading = 'Create User'
    company_contact = request.session['company_contact']
    company_name = Company.objects.get(contact_number=company_contact)

    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.company_name = company_name
            fs.save()
            newuser  = fs
            
            group = Group.objects.get(name='admin')
            newuser.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, username + ', Thank you for registering with us. Please login to use the application.')
            return redirect('login')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/company/user.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'gyms/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    active_member = Member.objects.filter(is_active=True, gym=request.user.company_name).aggregate(amount=Count('id'))
    inactive_member = Member.objects.filter(is_active=False, gym=request.user.company_name).aggregate(amount=Count('id'))


    income_today = Income.objects.filter(gym = request.user.company_name, added_date__date=date.today()).aggregate(amount=Sum('payment_amount'))
    income_month = Income.objects.filter(gym = request.user.company_name, added_date__month=date.today().month).aggregate(amount=Sum('payment_amount'))
    income_year = Income.objects.filter(gym = request.user.company_name, added_date__year=date.today().year).aggregate(amount=Sum('payment_amount'))

    expense_today = Expense.objects.filter(gym = request.user.company_name, added_date__date=date.today()).aggregate(amount=Sum('amount'))
    expense_month = Expense.objects.filter(gym = request.user.company_name, added_date__month=date.today().month).aggregate(amount=Sum('amount'))
    expense_year = Expense.objects.filter(gym = request.user.company_name, added_date__year=date.today().year).aggregate(amount=Sum('amount'))

    due_members = Member.objects.filter(is_active=True, gym = request.user.company_name).exclude(income__payment_month__month=date.today().month)

    context = {'active_member': active_member, 'inactive_member': inactive_member, 'income_today': income_today,
                'income_month': income_month, 'income_year': income_year, 'expense_today': expense_today,
                'expense_month': expense_month, 'expense_year': expense_year, 'due_members': due_members }
    return render(request, 'gyms/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def users(request):
    users = get_user_model().objects.filter(company_name = request.user.company_name)

    context = {'users': users}
    return render(request, 'gyms/user/users.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def user_create(request):
    form = CustomUserCreationForm()
    heading = 'Create User'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.company_name = request.user.company_name
            fs.save()
            newuser  = fs
            
            group = Group.objects.get(name='user')
            newuser.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, 'User  was created for ' + username + '.')
            return redirect('users')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/user/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def user_update(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    form = CustomUserChangeForm(instance=user)
    heading = 'Update User'

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.company_name = request.user.company_name            
            fs.save()          
            fs.groups.clear()
            group = form.cleaned_data.get('groups')
            fs.groups.add(group[0].id)
            username = form.cleaned_data.get('username')
            messages.success(request, 'User  was updated for ' + username + '.')
            return redirect('users')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/user/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def members(request):
    members = Member.objects.filter(gym = request.user.company_name, is_active = True)

    context = {'members': members}
    return render(request, 'gyms/member/members.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def members_inactive(request):
    members = Member.objects.filter(gym = request.user.company_name, is_active = False)

    context = {'members': members}
    return render(request, 'gyms/member/members_inactive.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_create(request):
    form = MemberForm()
    heading = 'Create Member'

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES,)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.gym = request.user.company_name
            fs.added_by = request.user
            fs.added_date = datetime.now()
            fs.save()

            member = form.cleaned_data.get('name')
            messages.success(request, 'Member  was created for ' + member + '.')
            return redirect('members')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/member/member.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_detail(request, pk):
    member = get_object_or_404(Member, id=pk)
    incomes = Income.objects.filter(member = member.id)

    heading = 'Member Detail'

    context = {'member': member, 'incomes': incomes, 'heading': heading}
    return render(request, 'gyms/member/member_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_details(request, pk):
    member = get_object_or_404(Member, id=pk)
    heading = 'Member Details'

    context = {'member': member, 'heading': heading}
    return render(request, 'gyms/member/member_details.html', context)

    


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_income_create(request, pk):
    member = get_object_or_404(Member, id=pk)
    form = MemberIncomeForm()
    heading = 'Create Payment'

    if request.method == 'POST':
        form = MemberIncomeForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.member = member
            fs.gym = request.user.company_name
            fs.added_by = request.user
            fs.added_date = datetime.now()
            fs.save()

            messages.success(request, 'Payment  was created for ' + member.name + '.')
            return redirect('member_detail', pk=member.id)

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/income/income.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_income_update(request, mb, ik):
    member = get_object_or_404(Member, id=mb)
    income = get_object_or_404(Income, id=ik)
    form = MemberIncomeForm(instance=income)
    heading = 'Update Payment'

    if request.method == 'POST':
        form = MemberIncomeForm(request.POST, instance=income)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.member = member
            fs.updated_by = request.user
            fs.updated_date = datetime.now()
            fs.save()

            messages.success(request, 'Payment  was updated for ' + member.name + '.')
            return redirect('member_detail', pk=member.id)

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/income/income.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_update(request, pk):
    member = get_object_or_404(Member, id=pk)
    form = MemberForm(instance=member)
    heading = 'Update Member'

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = datetime.now()
            fs.save()

            member = form.cleaned_data.get('name')
            messages.success(request, 'Member  was updated for ' + member + '.')
            return redirect('members')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/member/member.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def member_delete(request, pk):
    member = get_object_or_404(Member, id=pk)
    item = member.name
    heading = 'Delete Member'

    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Deleted Member was ' + item + '.')
        return redirect('members')

    context = {'member': member, 'heading': heading}
    return render(request, 'gyms/member/member_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def trainers(request):
    trainers = Trainer.objects.filter(gym = request.user.company_name)

    context = {'trainers': trainers}
    return render(request, 'gyms/trainer/trainers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def trainer_create(request):
    form = TrainerForm()
    heading = 'Create Trainer'

    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.gym = request.user.company_name
            fs.added_by = request.user
            fs.added_date = datetime.now()
            fs.save()

            trainer = form.cleaned_data.get('name')
            messages.success(request, 'Trainer  was created for ' + trainer + '.')
            return redirect('trainers')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/trainer/trainer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def trainer_update(request, pk):
    trainer = get_object_or_404(Trainer, id=pk)
    form = TrainerForm(instance=trainer)
    heading = 'Update Trainer'

    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = datetime.now()
            fs.save()

            trainer = form.cleaned_data.get('name')
            messages.success(request, 'Trainer  was updated for ' + trainer + '.')
            return redirect('trainers')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/trainer/trainer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def trainer_delete(request, pk):
    trainer = get_object_or_404(Trainer, id=pk)
    item = trainer.name
    heading = 'Delete Trainer'

    if request.method == 'POST':
        trainer.delete()
        messages.warning(request, 'Deleted Trainer was ' + item + '.')
        return redirect('trainers')

    context = {'trainer': trainer, 'heading': heading}
    return render(request, 'gyms/trainer/trainer_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def incomes(request):
    given_date = datetime.today().date()
    start_date = given_date.replace(day=1)
    end_date = last_day_of_month(given_date)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date') 
        incomes = Income.objects.filter(gym = request.user.company_name, payment_date__gte = start_date, payment_date__lte = end_date)
        total_income = incomes.aggregate(amount=Sum('payment_amount'))

        context = {'incomes': incomes, 'total_income': total_income}
        return render(request, 'gyms/income/incomes.html', context)

    incomes = Income.objects.filter(gym = request.user.company_name, payment_date__gte = start_date, payment_date__lte = end_date)
    total_income = incomes.aggregate(amount=Sum('payment_amount'))
    context = {'incomes': incomes, 'total_income': total_income}
    return render(request, 'gyms/income/incomes.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def income_create(request):
    form = IncomeForm()
    heading = 'Create Payment'

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.gym = request.user.company_name
            fs.added_by = request.user
            fs.added_date = datetime.now()
            fs.save()

            income = form.cleaned_data.get('member')
            messages.success(request, 'Payment  was created for ' + income.name + '.')
            return redirect('incomes')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/income/income.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def income_update(request, pk):
    income = get_object_or_404(Income, id=pk)
    form = IncomeForm(instance=income)
    heading = 'Update Payment'

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = datetime.now()
            fs.save()

            income = form.cleaned_data.get('member')
            messages.success(request, 'Payment  was updated for ' + income.name + '.')
            return redirect('incomes')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/income/income.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def income_delete(request, pk):
    income = get_object_or_404(Income, id=pk)
    item = income.member
    heading = 'Delete Payment'

    if request.method == 'POST':
        income.delete()
        messages.warning(request, 'Deleted income was ' + item.name + '.')
        return redirect('incomes')

    context = {'income': income, 'heading': heading}
    return render(request, 'gyms/income/income_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def expenses(request):
    given_date = datetime.today().date()
    start_date = given_date.replace(day=1)
    end_date = last_day_of_month(given_date)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date') 
        expenses = Expense.objects.filter(gym = request.user.company_name, expense_date__gte = start_date, expense_date__lte = end_date)
        total_expense = expenses.aggregate(amount=Sum('amount'))

        context = {'expenses': expenses, 'total_expense': total_expense}
        return render(request, 'gyms/expense/expenses.html', context)

    expenses = Expense.objects.filter(gym = request.user.company_name)
    total_expense = expenses.aggregate(amount=Sum('amount'))
    context = {'expenses': expenses, 'total_expense': total_expense}
    return render(request, 'gyms/expense/expenses.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def expense_create(request):
    form = ExpenseForm()
    heading = 'Create Expense'

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.gym = request.user.company_name
            fs.added_by = request.user
            fs.added_date = datetime.now()
            fs.save()

            expense = form.cleaned_data.get('particular')
            messages.success(request, 'Expense  was created for ' + expense + '.')
            return redirect('expenses')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/expense/expense.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def expense_update(request, pk):
    expense = get_object_or_404(Expense, id=pk)
    form = ExpenseForm(instance=expense)
    heading = 'Update Expense'

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = datetime.now()
            fs.save()

            expense = form.cleaned_data.get('particular')
            messages.success(request, 'Expense  was updated for ' + expense + '.')
            return redirect('expenses')

    context = {'form': form, 'heading': heading}
    return render(request, 'gyms/expense/expense.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, id=pk)
    item = expense.particular
    heading = 'Delete Expense'

    if request.method == 'POST':
        expense.delete()
        messages.warning(request, 'Deleted Expense was for ' + item + '.')
        return redirect('expenses')

    context = {'expense': expense, 'heading': heading}
    return render(request, 'gyms/expense/expense_delete.html', context)