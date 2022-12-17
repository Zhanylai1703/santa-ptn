import random
from threading import Thread

from django.apps import apps
from django.contrib.auth.decorators import login_required                     
'''
 Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
    на страницу входа, если это необходимо.'''
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import Owner, Group, Field, FieldAnswer, SimpleUser
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        auth_form = RegistrationForm(request.POST)

        if auth_form.is_valid():
            auth_form.save()
            return redirect('app:login')
    else:
        auth_form = RegistrationForm()

    context = {'form': auth_form}
    return render(request, 'registration/register.html', context)


@login_required()
def index(request):
    context = {
        'groups': request.user.owned_groups.all(),
    }
    return render(request, 'views/index.html', context)


def get_simple_users(id):
    group = Group.objects.filter(id=id)
    fields = Field.objects.filter(group__in=group)
    field_answers = FieldAnswer.objects.filter(field__in=fields)
    simple_users = SimpleUser.objects.filter(fieldanswer__in=field_answers).distinct()

    return {
        'group': group.first(),
        'fields': fields,
        'simple_users': simple_users,
    }


@login_required()
def group_detail(request, id):
    context = get_simple_users(id)

    return render(request, 'views/group_detail.html', context)


def edit_or_create(request, object, **args):
    group = Group.objects.filter(id=request.GET.get('group_id')).first()
    model_object = ''
    id = args.get('id', False)

    if not group and id:
        group = Group.objects.filter(fields__in=Field.objects.filter(id=id)).first()
        model_object = apps.get_model('app', object).objects.filter(id=id).first()

    return {
        'object': object,
        'group': group,
        'model_object': model_object,
    }


def save_data(request, object, is_new=False, **args):
    form = request.POST
    owner = Owner.objects.filter(id=form['owner_id'])
    name = form['name']
    group_id = request.GET.get('group', form.get('group_id', False))
    group = Group.objects.filter(id=group_id).first()
    id = args.get('id', False)
    is_required = request.POST.get('is_required', '') == 'on'

    if is_new:
        if object == 'group':
            group = Group.objects.create(name=name)
            request.user.owned_groups.add(group)

        elif object == 'field':
            group.fields.create(name=name, is_required=is_required)
    else:
        model_object = apps.get_model('app', object).objects.filter(id=id).first()
        model_object.name = name
        model_object.is_required = is_required
        model_object.save()

        if object == 'group':
            group = model_object
        else:
            group = Group.objects.filter(fields__in=Field.objects.filter(id=id)).first()

    return group


@login_required()
def new(request, object):
    if request.method == "POST":
        group = save_data(request, object, is_new=True)
        return redirect('app:group_detail', id=group.id)

    context = edit_or_create(request, object)
    return render(request, 'views/new.html', context)


@login_required()
def edit(request, object, id):
    if request.method == "POST":
        group = save_data(request, object, is_new=False, id=id)
        return redirect('app:group_detail', id=group.id)

    context = edit_or_create(request, object, id=id)
    return render(request, 'views/new.html', context)


@login_required()
def delete(request, object, group_id, id):
    Model = apps.get_model('app', object)
    groups = Group.objects.filter(owner=request.user).values_list('id', flat=True)
    group = Group.objects.filter(id=group_id)

    if group.filter(id__in=groups):
        if object == 'group':
            Group.objects.filter(id=id).delete()
            return redirect('app:index')

        else:
            model_object = Model.objects.filter(id=id).first()
            model_object.delete()
            return redirect('app:group_detail', group_id)


@login_required()
def finish(request, id):
    context = get_simple_users(id)
    users_before = context.get('simple_users', '')
    tracked_users = users_before

    for simple_user in users_before:
        assigned = random.choice(tracked_users)
        while assigned == simple_user:
            assigned = random.choice(tracked_users)

        simple_user.assigned = assigned
        simple_user.save()

        body = 'Спасибо за участие ' + context['group'].name + '\' Secret Santa! \n\n' \
               'Тебе попался(сь): ' + assigned.name + '.\n\n'

        if context['fields'].count() > 0:
            body += 'пожелания [assigned.name]:\n'

            for field in context['fields'].filter():
                body += field.name.title() + ': ' \
                        '' + assigned.fieldanswer_set.filter(field=field).last().answer + '\n'

        Thread(target=send_mail, args=('Secret Santa Assignment', body, settings.EMAIL_HOST_USER, [simple_user.email])).start()
        tracked_users = tracked_users.exclude(id=assigned.id)

    return redirect('app:group_detail', id=context['group'].id)


def form(request, id):
    group = Group.objects.filter(id=id).first()

    if request.method == 'POST':
        form = request.POST
        group = Group.objects.filter(id=id).first()
        email = form.get('email', '')
        name = form.get('name', '')

        fields = Field.objects.filter(group__in=Group.objects.filter(id=id))
        field_answers = FieldAnswer.objects.filter(field__in=fields)
        simple_users = SimpleUser.objects.filter(email=email, fieldanswer__in=field_answers)

        if simple_users.count() > 0:
            simple_user = simple_users.first()
            simple_user.name = name
            simple_user.email = email
            simple_user.save()
        else:
            simple_user = SimpleUser.objects.create(name=name, email=email)

        for field in group.fields.all():
            answer = form.get('field-' + str(field.id), '')
            field_answer = FieldAnswer.objects.create(answer=answer)
            field_answer.user.add(simple_user)
            field_answer.field.add(field)
            field_answer.save()

        return redirect('app:form_submit')

    context = {
        'group': group,
        'fields': group.fields.all(),
    }

    return render(request, 'views/form.html', context)


def form_submit(request):
    return render(request, 'views/form_submit.html')
