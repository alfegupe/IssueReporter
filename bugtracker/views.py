# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, \
    update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, \
    RedirectView, View
from django.views.generic.edit import UpdateView
from bugtracker.utils.tools import *
from forms import LoginForm, CreateIssueForm, UpdateIssueForm, SearchIssueForm, \
    UpdateDataUserForm, UpdatePasswordUserForm, UpdateIssueAdminForm, \
    CreateEvaluationComment, CreateIssueEvaluation
from models import Issue, StatusIssue, EvaluationComment, IssueEvaluation
from .models import Person
from utils.mixins import JSONResponseMixin
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

# names Groups:
reporters_group = 'Reporter'
developers_group = 'Developer'


def is_member(user, group):
    return user.groups.filter(name=group).exists()


def send_notification_bug_email(request, issue, is_update=None):
    try:
        id_issue = issue.id
        op = 'actualizada' if is_update else 'creada'
        title = 'La incidencia #' + str(id_issue) + ' ha sido ' + op

        plaintext = get_template('email/bug.txt')
        htmly = get_template('email/bug.html')

        d = Context({
            'cdf': issue, 'id_issue': id_issue,
            'main_message': 'La incidencia #' + str(id_issue) + ' ha sido ' + op
        })

        text_content = plaintext.render(d)
        html_content = htmly.render(d)

        f_from = ''
        to = [request.user.email]
        if issue.reporter:
            rep = issue.reporter
            if issue.status.id == 5:
                htmly2 = get_template('email/bug_link_evaluation.html')
                html_content2 = htmly2.render(d)
                to2 = [rep.user.email]
                print "Cerrando - enviando a: ", to2
                if mail(title, text_content, html_content2, f_from, to2):
                    print 'An email has been sent whit evaluation link.'
            else:
                if rep.user.email not in to:
                    to.append(rep.user.email)

        if issue.dev:
            dev = issue.dev
            if dev.user.email not in to:
                to.append(dev.user.email)

        if mail(title, text_content, html_content, f_from, to):
            print 'An email has been sent.'

        return True
    except Exception as e:
        print e.message
        return None


def send_notification_new_evaluation_comment_email(issue_id, comments):
    issue = Issue.objects.get(pk=issue_id)
    f_from = ''
    to = []
    if issue.dev:
        if issue.dev.user.email not in to:
            to.append(issue.dev.user.email)

    htmly = get_template('email/evaluation_comment.html')

    d = Context({
        'user': comments['user'],
        'comment': comments['comment'],
        'main_message': 'La incidencia #' + str(issue_id) +
                        ' tiene un nuevo comentario'
    })

    text_content = ""
    html_content = htmly.render(d)

    if mail('Nuevo comentario en la incidencia ' + str(issue.id), text_content,
            html_content, f_from, to):
        print 'An email has been sent.'
    pass


class IndexView(View):
    template = "bugtracker/index.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login')

        if self.request.user.is_superuser or \
                is_member(self.request.user, developers_group):
            context = {}
            status = Issue.objects.all().values(
                'status_id', 'status__status'
            ).annotate(total=Count('status_id')).order_by('-total')

            priority = Issue.objects.values(
                'priority__id', 'priority__priority'
            ).filter(
                status__id__lt=4
            ).annotate(total=Count('priority__id')).order_by('-total')

            type_i = Issue.objects.all().values(
                'type_issue_id', 'type_issue__type_issue'
            ).filter(
                status__id__lt=4
            ).annotate(total=Count('type_issue_id')).order_by('-total')

            context['status_issues'] = status
            context['priority_issues'] = priority
            context['type_issues'] = type_i

            return render(request, self.template, context)

        return redirect('home')


class LoginView(View):
    form = LoginForm()
    message = None
    template = "auth/login.html"
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            self.message = 'Usuario o password incorrectos'
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message': self.message}


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'u_name'
    login_url = 'login'


class UpdateDataUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/edit.html'
    login_url = 'login'
    form_class = UpdateDataUserForm

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'u_name': self.request.user.username}
        )

    def get_object(self, queryset=None):
        return self.request.user

    def get_username(self):
        return self.request.user.username


def update_password(request):
    message = None
    form = UpdatePasswordUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_pass = form.cleaned_data['password']
            new_pass = form.cleaned_data['new_password']
            if authenticate(
                    username=request.user.username, password=current_pass
            ):
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user)
                message = 'Password actualizado.'
            else:
                message = 'El password actual es incorrecto'

    context = {'form': form, 'message': message}
    return render(request, 'user/update_password.html', context)


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'bugtracker/issues.html'
    login_url = 'login'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        context['form_search'] = SearchIssueForm(data=self.request.GET)
        context['is_dev'] = True if is_member(
            self.request.user, developers_group
        ) or self.request.user.is_superuser else None
        context['paginator_params'] = self.get_params_pagination()
        return context

    def get_queryset(self):
        query = self.get_params_search()
        date = ""
        issues = ""
        show_in_main_list = True
        if 'is_closed' in query:
            show_in_main_list = False if query['is_closed'] == 'on' else True
            del query['is_closed']

        if 'date' in query:
            date = query['date']
            del query['date']

        if not self.request.user.is_superuser and \
                not is_member(self.request.user, developers_group):
            query['reporter'] = Person.objects.get(user=self.request.user)
        query['status__show_in_main_list'] = show_in_main_list

        if date == "asc":
            issues = self.model.objects.filter(**query).order_by('created_at')
        elif date == "dsc":
            issues = self.model.objects.filter(**query).order_by('-created_at')
        else:
            issues = self.model.objects.filter(**query).order_by(
                'priority', 'type_issue', 'created_at')

        return issues

    def get_params_search(self):
        params = {}
        try:
            for key in self.request.GET:
                if self.request.GET[key] != '' and key != 'page':
                    k = key + '__contains' if key == 'issue' else key
                    params[k] = self.request.GET[key]
        except Exception as e:
            print e.message
        finally:
            return params

    def get_params_pagination(self):
        params = ""
        try:
            for key in self.request.GET:
                if self.request.GET[key] != '' and key != 'page':
                    params += "&" + key + "=" + self.request.GET[key]
        except Exception as e:
            print e.message
        finally:
            return params


class IssueCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateIssueForm
    template_name = 'bugtracker/create.html'
    login_url = 'login'
    message = None
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            person = Person.objects.get(user=self.request.user)
            if not person:
                messages.error(
                    self.request,
                    'Usuario no existe como Persona en la base de datos.'
                )
                return super(IssueCreateView, self).form_invalid(form)
            if not self.request.user.is_superuser and \
                    not is_member(self.request.user, developers_group) and \
                    not is_member(self.request.user, reporters_group):
                messages.error(
                    self.request,
                    'Usuario no tiene permisos para reportar incidencias.'
                )
                return super(IssueCreateView, self).form_invalid(form)

            messages.success(
                self.request,
                'Incidencia ha sido creada correctamente.'
            )
            form.instance.reporter = person
            form.instance.status = StatusIssue.objects.get(status__regex='uev')

            return super(IssueCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(IssueCreateView, self).form_invalid(form)

    def get_success_url(self):
        send_notification_bug_email(self.request, self.object)
        return super(IssueCreateView, self).get_success_url()


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issue
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'
    template_name = 'bugtracker/update.html'
    form_class = UpdateIssueForm
    login_url = 'login'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or \
                is_member(self.request.user, developers_group):
            self.form_class = UpdateIssueAdminForm
        form = super(IssueUpdateView, self).get_context_data()
        form['formcomment'] = CreateEvaluationComment()
        form['comments'] = EvaluationComment.objects.select_related('user') \
            .filter(issue__id=self.kwargs['id_issue']) \
            .order_by('-created_at').all()
        return form

    def form_valid(self, form):
        try:
            if not self.request.user.is_superuser and \
                    not is_member(self.request.user, developers_group) and \
                    not is_member(self.request.user, reporters_group):
                messages.error(
                    self.request,
                    'Usuario no tiene permisos para actualizar incidencias.'
                )
                return super(IssueUpdateView, self).form_invalid(form)

            messages.success(
                self.request,
                'Incidencia ha sido actualizada.'
            )
            return super(IssueUpdateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(IssueUpdateView, self).form_invalid(form)

    def get_success_url(self):
        send_notification_bug_email(self.request, self.object, True)
        return super(IssueUpdateView, self).get_success_url()

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser or \
                is_member(self.request.user, developers_group):
            self.form_class = UpdateIssueAdminForm
        return super(IssueUpdateView, self).post(request, *args, **kwargs)


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'bugtracker/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'

    def get_context_data(self, **kwargs):
        form = super(IssueDetailView, self).get_context_data()
        form['formcomment'] = CreateEvaluationComment()
        form['formissueevaluation'] = CreateIssueEvaluation()
        form['comments'] = EvaluationComment.objects.select_related('user') \
            .filter(issue__id=self.kwargs['id_issue']) \
            .order_by('-created_at').all()
        evaluated = IssueEvaluation.objects. \
            filter(issue__id=self.kwargs['id_issue']).all()
        form['is_evaluated'] = True if len(evaluated) > 0 else False
        return form


class EvaluationCommentCreate(JSONResponseMixin, CreateView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            user = self.request.user
            ev = EvaluationComment.objects.create(comment=comment, issue_id=id,
                                                  user_id=user.id)
            count_comments = EvaluationComment.objects.select_related('user') \
                .filter(issue__id=id) \
                .order_by('-created_at').count()
            comments = {
                'comment': ev.comment,
                'user': user.first_name + " " + user.last_name,
                'created_at': ev.created_at,
                'count': count_comments,
            }
            send_notification_new_evaluation_comment_email(id, comments)
            return JsonResponse(comments, safe=False)
        except Exception as e:
            print type(e)
            print e.message
            return self.render_to_json_response({'code': 540,
                                                 'msj': 'No se ha almacenado'})


class ExportXlsx(JSONResponseMixin, CreateView):
    model = Issue

    def get(self, request, *args, **kwargs):
        from xlsxwriter.workbook import Workbook
        from io import BytesIO

        query = self.get_params_search()
        if query:
            output = BytesIO()

            book = Workbook(output)
            header = book.add_format({
                'bg_color': '#F7F7F7',
                'color': 'black',
                'align': 'center',
                'valign': 'top',
                'border': 1
            })
            sheet = book.add_worksheet('Listado')
            row = 1
            sheet.write(0, 0, "ID", header)
            sheet.write(0, 1, "NOMBRE", header)
            sheet.write(0, 2, "REPORTADA", header)
            sheet.write(0, 3, "TIPO", header)
            sheet.write(0, 4, "ESTADO", header)
            sheet.write(0, 5, "SOFTWARE", header)
            sheet.write(0, 6, "ASIGNADO A", header)
            data = self.model.objects.all().filter(**query)
            for issue in data:
                sheet.write(row, 0, issue.id, header)
                sheet.write(row, 1, issue.issue)
                sheet.write(row, 2, str(issue.created_at).split(" ")[0])
                sheet.write(row, 3, issue.type_issue.type_issue)
                sheet.write(row, 4, issue.status.status)
                sheet.write(row, 5, issue.software.software)
                if issue.dev:
                    sheet.write(row, 6, str(issue.dev).decode('utf-8'))
                else:
                    sheet.write(row, 6, '--')
                row += 1
            book.close()
            output.seek(0)
            response = HttpResponse(output.read(),
                                    content_type="application/vnd.openxmlformats" +
                                                 "-officedocument.spreadsheetml." +
                                                 "sheet")
            return response

        return None

    def get_params_search(self):
        params = {}
        try:
            params['status__id__lt'] = 4
            for i in self.request.GET:
                if self.request.GET.get(i):
                    params[i] = self.request.GET.get(i)
        except Exception as e:
            return None
        finally:
            return params


class IssueEvaluationView(JSONResponseMixin, CreateView):
    model = IssueEvaluation

    def post(self, request, *args, **kwargs):
        id = request.POST.get('issue_id')
        q1 = request.POST.get('resolve')
        q2 = request.POST.get('time_evaluation')
        q3 = request.POST.get('difficulty')
        q4 = request.POST.get('contact')
        q5 = request.POST.get('satisfied')
        user = self.request.user
        ev = IssueEvaluation(satisfied=q5, time_evaluation=q2, resolve=q1,
                             difficulty=q3, contact=q4, user_id=user.id,
                             issue_id=id)
        ev.save()
        if ev:
            # send_notification_new_evaluation_comment_email(id, comments)
            return JsonResponse(
                {'code': 200, 'msg': 'Se ha creado...'}, safe=False)
        else:
            return JsonResponse(
                {'code': 400, 'msg': 'No se ha creado...'}, safe=False)


class IssueEvaluationResultView(View):
    model = IssueEvaluation
    fields = ['observations', 'time_evaluation', 'resolve', 'notify',
              'satisfied']
    template = "bugtracker/result_evaluations.html"

    @method_decorator(permission_required(
        'bugtracker.can_view_results_evaluations', reverse_lazy('home')))
    def get(self, request, *args, **kwargs):
        resolve = {'1': 0, '5': 0}
        time = {'1': 0, '2': 0, '3': 0, '5': 0}
        difficulty = {'1': 0, '2': 0, '3': 0, '5': 0}
        contact = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        satisfied = {'1': 0, '2': 0, '3': 0, '5': 0}
        issue_evaluations = IssueEvaluation.objects.all()
        for ev in issue_evaluations:
            time[ev.time_evaluation] = time[ev.time_evaluation] + 1
            resolve[ev.resolve] = resolve[ev.resolve] + 1
            difficulty[ev.difficulty] = difficulty[ev.difficulty] + 1
            contact[ev.contact] = contact[ev.contact] + 1
            satisfied[ev.satisfied] = satisfied[ev.satisfied] + 1
        return render(request, "bugtracker/result_evaluations.html",
                      {'difficulty': difficulty, 'time': time,
                       'resolve': resolve, 'contact': contact,
                       'satisfied':satisfied, 'cant': issue_evaluations.count()})

    def __data_result_evaluations__(self, data, type):
        pass

class IssueEvaluationResulExportXlsx(JSONResponseMixin, CreateView):

    model = IssueEvaluation

    def get(self, request, *args, **kwargs):

        from xlsxwriter.workbook import Workbook
        from io import BytesIO

        resolve = {'1': 0, '5': 0}
        time = {'1': 0, '2': 0, '3': 0, '5': 0}
        difficulty = {'1': 0, '2': 0, '3': 0, '5': 0}
        contact = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        satisfied = {'1': 0, '2': 0, '3': 0, '5': 0}
        issue_evaluations = IssueEvaluation.objects.all()

        output = BytesIO()

        book = Workbook(output)
        header = book.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })
        sheet = book.add_worksheet('Listado')
        row = 1

        for ev in issue_evaluations:
            time[ev.time_evaluation] = time[ev.time_evaluation] + 1
            resolve[ev.resolve] = resolve[ev.resolve] + 1
            difficulty[ev.difficulty] = difficulty[ev.difficulty] + 1
            contact[ev.contact] = contact[ev.contact] + 1
            satisfied[ev.satisfied] = satisfied[ev.satisfied] + 1

        sheet.write(0, 0, "Numero de evaluaciones presentadas:", header)
        sheet.write(0, 1, issue_evaluations.count(), header)

        sheet.write(2, 0, "Su solicitud fue resuelta", header)
        sheet.write(3, 0, "No resuelta", header)
        sheet.write(3, 1, resolve['1'], header)
        sheet.write(4, 0, "Fue resuelta completamente", header)
        sheet.write(4, 1, resolve['5'], header)

        sheet.write(6, 0, "El Tiempo en atender su solicitud fue:", header)
        sheet.write(7, 0, "Muy lento", header)
        sheet.write(7, 1, time['1'], header)
        sheet.write(8, 0, "Lento", header)
        sheet.write(8, 1, time['2'], header)
        sheet.write(9, 0, "Rapido", header)
        sheet.write(9, 1, time['3'], header)
        sheet.write(10, 0, "Muy rapido", header)
        sheet.write(10, 1, time['5'], header)

        sheet.write(12, 0, "EL nivel de dificultad para usar el software de " +
            "reporte de incidencias fue:", header)
        sheet.write(13, 0, "Muy facil", header)
        sheet.write(13, 1, difficulty['1'], header)
        sheet.write(14, 0, "Facil", header)
        sheet.write(14, 1, difficulty['2'], header)
        sheet.write(15, 0, "Dificil", header)
        sheet.write(15, 1, difficulty['3'], header)
        sheet.write(16, 0, "Muy dificil", header)
        sheet.write(16, 1, difficulty['5'], header)

        sheet.write(18, 0, "Fue contactado por alguno de estos medios para "+
            "resolver su solicitud", header)
        sheet.write(19, 0, "Extension telefonica", header)
        sheet.write(19, 1, contact['1'], header)
        sheet.write(20, 0, 'Correo electronico', header)
        sheet.write(20, 1, contact['2'], header)
        sheet.write(21, 0, "Celular", header)
        sheet.write(21, 1, contact['3'], header)
        sheet.write(22, 0, 'Chat', header)
        sheet.write(22, 1, contact['4'], header)
        sheet.write(23, 0, "Ninguno", header)
        sheet.write(23, 1, contact['5'], header)

        sheet.write(25, 0, 'Nivel de satisfaccion con la atencion recibida:', header)
        sheet.write(26, 0, 'Muy insatisfecho', header)
        sheet.write(26, 1, satisfied['1'], header)
        sheet.write(27, 0, "Insatisfecho", header)
        sheet.write(27, 1, satisfied['2'], header)
        sheet.write(28, 0, "Satisfecho", header)
        sheet.write(28, 1, satisfied['3'], header)
        sheet.write(29, 0, "Muy satisfecho", header)
        sheet.write(29, 1, satisfied['5'], header)

        book.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats" +
                                             "-officedocument.spreadsheetml." +
                                             "sheet")
        return response
