# -*- encoding: utf-8 -*-

import datetime
import xlsxwriter
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
solved_status = StatusIssue.objects.get(status='Solucionada')
closed_status = StatusIssue.objects.get(status='Cerrada')


def is_member(user, group):
    return user.groups.filter(name=group).exists()


def send_notification_bug_email(request, issue, is_update=None):
    try:
        id_issue = issue.id
        if issue.status_id == 5:
            op = "Solucionada"
        elif is_update:
            op = "actualizada"
        else:
            op = "creada"

        print(op)
        # op = 'actualizada' if is_update else 'creada'
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
        to = [request.user.email, 'edisonml@campus.udes.edu.co']
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
    f_from = 'edisonml@campus.udes.edu.co'
    to = [issue.reporter.user.email, 'edisonml@campus.udes.edu.co',
          issue.dev.user.email]
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
        if 'filter' in self.request.session:
            del self.request.session['filter']
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
            evaluated = Issue.objects.filter(reporter__user=self.request.user, evaluated=False, status_id=5,
                                             ).exclude(reporter__user__date_joined__year__lt='2017',
                                                       reporter__user__date_joined__month__lt='7').count()
            context['evalue'] = evaluated == 0
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
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        if self.request.GET:
            self.request.session['filter'] = self.request.GET
        elif not'filter' in self.request.session:
            self.request.session['filter'] = {}
        context['form_search'] = SearchIssueForm(data=self.request.session['filter'])
        context['is_dev'] = True if is_member(
            self.request.user, developers_group
        ) or self.request.user.is_superuser else None
        context['paginator_params'] = self.get_params_pagination()
        context['formissueevaluation'] = CreateIssueEvaluation()
        evaluated = Issue.objects.filter(reporter__user=self.request.user, evaluated=False, status_id=5,
                                         ).exclude(reporter__user__date_joined__year__lt='2017',
                                         reporter__user__date_joined__month__lt='7').count()
        context['evalue'] = evaluated == 0
        paginator = context['paginator']
        page = int(self.request.GET.get('page', 1))
        upper_limit = page + 5 if page > 6 else 11

        if page == paginator.num_pages or page > (paginator.num_pages - 5):
            lower_limit = paginator.num_pages - 10
        elif page > 5:
            lower_limit = page - 5
        else:
            lower_limit = 1

        context['custom_page_range'] = xrange(lower_limit, upper_limit)
        return context

    def get_queryset(self):
        query = self.get_params_search()
        date = ""
        issues = ""
        show_in_main_list = True
        if 'is_evaluated' in query:
            # show_in_main_list = False if query['is_evaluated'] == 'on' else True
            query['evaluated'] = False if query['is_evaluated'] == 'on' else True
            query['status'] = solved_status
            query['reporter'] = Person.objects.get(user=self.request.user)

            del query['is_evaluated']
        if 'date_init' in query:
            date_init = query['date_init'].split('/')
            year = int(date_init[2])
            month = int(date_init[1])
            day = int(date_init[0])
            date = datetime.datetime(year, month, day)
            query['created_at__gte'] = date
            del query['date_init']
        if 'date_end' in query:
            date_end = query['date_end'].split('/')
            year = int(date_end[2])
            month = int(date_end[1])
            day = int(date_end[0])
            date = datetime.datetime(year, month, day, 23)
            query['created_at__lte'] = date
            del query['date_end']

        if not self.request.user.is_superuser and \
                not is_member(self.request.user, developers_group):
            query['reporter'] = Person.objects.get(user=self.request.user)
        # query['status__show_in_main_list'] = show_in_main_list

        if date == "asc":
            issues = self.model.objects.filter(**query).order_by('created_at')
        elif date == "dsc":
            issues = self.model.objects.filter(**query).order_by('-created_at')
        else:
            issues = self.model.objects.filter(**query).order_by('-created_at')
            # 'priority', 'type_issue',

        return issues

    def get_params_search(self):
        if self.request.GET:
            self.request.session['filter'] = self.request.GET
        elif not 'filter' in self.request.session:
            self.request.session['filter'] = {}
        params = {}
        try:
            for key in self.request.session['filter']:
                if self.request.session['filter'][key] != '' and key != 'page':
                    k = key + '__icontains' if key == 'issue' else key
                    params[k] = self.request.session['filter'][key]
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
    developers_group = 'is_dev'

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
        form['is_dev'] = (is_member(self.request.user, developers_group) or
                          self.request.user.is_superuser)
        self.request.session['http_referer'] = self.request.META['HTTP_REFERER']
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
            header5 = book.add_format({
                'align': 'center',
                'border': 1,
                'bold': 'True',
                'bg_color': '#F2F2F2'

            })
            header4 = book.add_format({
                'align': 'center',
                'border': 1,
                'bold': 'True',
                'bg_color': '#D8D8D8'


            })
            header3 = book.add_format({
                'border': 1
            })
            header2 = book.add_format({
                'align': 'center',
                'border': 1
            })
            header = book.add_format({
                'bg_color': '#F7F7F7',
                'color': 'black',
                'align': 'center',
                'bold': 'True',
                'valign': 'auto',
                'border': 1
            })

            sheet = book.add_worksheet('Listado')
            row = 6

            sheet.merge_range('B2:J2', 'REPORTEADOR DE INCIDENCIAS OPTIMUS APP', header4)
            sheet.merge_range('B4:J4', 'LISTADO DE INCIDENCIAS', header5)
            sheet.write(5, 1, "ID", header)
            sheet.write(5, 2, "NOMBRE", header)
            sheet.write(5, 3, "REPORTADA POR", header)
            sheet.write(5, 4, "TIPO", header)
            sheet.write(5, 5, "ESTADO", header)
            sheet.write(5, 6, "SISTEMA", header)
            sheet.write(5, 7, "ASIGNADO A", header)
            sheet.write(5, 8, "FECHA REPORTE", header)
            sheet.write(5, 9, "SPRINT", header)
            data = self.model.objects.all().filter(**query).order_by('-created_at')
            for issue in data:
                sheet.write(row, 1, issue.id, header2)
                sheet.write(row, 2, issue.issue, header3)
                sheet.write(row, 3, str(issue.reporter.user), header3)
                sheet.write(row, 4, issue.type_issue.type_issue, header3)
                sheet.write(row, 5, issue.status.status, header3)
                sheet.write(row, 6, issue.software.software, header3)
                sheet.write(row, 8, str(issue.created_at).split(" ")[0], header2)
                sheet.write(row, 9, issue.sprint, header2)

                if issue.dev:
                    sheet.write(row, 7, str(issue.dev).decode('utf-8'), header3)
                else:
                    sheet.write(row, 10, '')
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
            params['status__id__lt'] = 8
            for i in self.request.GET:
                if self.request.GET.get(i):
                    params[i] = self.request.GET.get(i)
        except Exception as e:
            return None
        finally:
            return params


class IssueEvaluationView(JSONResponseMixin, CreateView):

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
            cerrado = StatusIssue.objects.get(status='Cerrada')
            Issue.objects.filter(pk=id).update(evaluated=True, status=cerrado)
            messages.success(
                self.request,
                'Incidencia evaluada.'
            )
            return JsonResponse(
                {'code': 200, 'msg': 'Se ha creado...'}, safe=False)
        else:
            messages.error(
                self.request,
                'Incidencia no se pudo evaluada.'
            )
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
        resolve = {'1': 0, '3': 0, '5': 0}
        time = {'1': 0, '2': 0, '3': 0, '5': 0}
        difficulty = {'1': 0, '2': 0, '3': 0, '5': 0}
        contact = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
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
                       'satisfied': satisfied, 'cant': issue_evaluations.count()})


class IssueEvaluationResulExportXlsx(JSONResponseMixin, CreateView):
    model = IssueEvaluation

    def get(self, request, *args, **kwargs):

        from xlsxwriter.workbook import Workbook
        from io import BytesIO

        resolve = {'1': 0, '3': 0, '5': 0}
        time = {'1': 0, '2': 0, '3': 0, '5': 0}
        difficulty = {'1': 0, '2': 0, '3': 0, '5': 0}
        contact = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        satisfied = {'1': 0, '2': 0, '3': 0, '5': 0}

        init_date = request.GET['init_date']
        end_date = request.GET['end_date']

        if init_date and end_date:
            issue_evaluations = IssueEvaluation.objects.filter(
                issue__created_at__lte=end_date,
                issue__created_at__gte=init_date)
        else:
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
        datax = book.add_format({
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
        sheet.merge_range(2, 0, 2, 1, "Su solicitud fue resuelta",
                          header)
        sheet.write(3, 0, "No resuelta", header)
        sheet.write(3, 1, resolve['1'], datax)
        sheet.write(4, 0, "Fue resuelta completamente", header)
        sheet.write(4, 1, resolve['5'], datax)

        sheet.merge_range(6, 0, 6, 1, "El Tiempo en atender su solicitud fue:", header)
        sheet.write(7, 0, "Muy lento", header)
        sheet.write(7, 1, time['1'], datax)
        sheet.write(8, 0, "Lento", header)
        sheet.write(8, 1, time['2'], datax)
        sheet.write(9, 0, "Rapido", header)
        sheet.write(9, 1, time['3'], datax)
        sheet.write(10, 0, "Muy rapido", header)
        sheet.write(10, 1, time['5'], datax)

        sheet.merge_range(12, 0, 12, 1, "EL nivel de dificultad para usar el software de " +
                          "reporte de incidencias fue:", header)
        sheet.write(13, 0, "Muy facil", header)
        sheet.write(13, 1, difficulty['1'], datax)
        sheet.write(14, 0, "Facil", header)
        sheet.write(14, 1, difficulty['2'], datax)
        sheet.write(15, 0, "Dificil", header)
        sheet.write(15, 1, difficulty['3'], datax)
        sheet.write(16, 0, "Muy dificil", header)
        sheet.write(16, 1, difficulty['5'], datax)

        sheet.merge_range(18, 0, 18, 1, "Fue contactado por alguno de estos medios para " +
                          "resolver su solicitud", header)
        sheet.write(19, 0, "Extension telefonica", header)
        sheet.write(19, 1, contact['1'], datax)
        sheet.write(20, 0, 'Correo electronico', header)
        sheet.write(20, 1, contact['2'], datax)
        sheet.write(21, 0, "Celular", header)
        sheet.write(21, 1, contact['3'], datax)
        sheet.write(22, 0, 'Chat', header)
        sheet.write(22, 1, contact['4'], datax)
        sheet.write(23, 0, "Personalmente", header)
        sheet.write(23, 1, contact['5'], datax)
        sheet.write(23, 0, "Ninguno", header)
        sheet.write(23, 1, contact['5'], datax)

        sheet.merge_range(25, 0, 25, 1, 'Nivel de satisfaccion con la atencion recibida:', header)
        sheet.write(26, 0, 'Muy insatisfecho', header)
        sheet.write(26, 1, satisfied['1'], datax)
        sheet.write(27, 0, "Insatisfecho", header)
        sheet.write(27, 1, satisfied['2'], datax)
        sheet.write(28, 0, "Satisfecho", header)
        sheet.write(28, 1, satisfied['3'], datax)
        sheet.write(29, 0, "Muy satisfecho", header)
        sheet.write(29, 1, satisfied['5'], datax)

        book.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats" +
                                             "-officedocument.spreadsheetml." +
                                             "sheet")
        return response


class IssueEvaluationDetails(LoginRequiredMixin, DetailView):
    model = IssueEvaluation
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'

    def get(self, request, *args, **kwargs):
        time_opc = {"1": "Muy lento", "2": "Lento", "3": "Rápido",
                    "5": "Muy rápido"}
        resolve_opc = {"1": "No resuelta", "3": "Resuelta", "5": "Fue resuelta completamente"}
        difficulty_opc = {"1": "Muy fácil", "2": "Fácil", "3": "Difícil",
                          "5": "Muy difícil"}
        contact_opc = {"1": "Extensión telefónica", "2": "Correo electrónico",
                       "3": "Celular", "4": "Chat", "5": "Ninguno", "6": "Personalmente"}
        satisfied_opc = {"1": "Muy insatisfecho", "2": "Insatisfecho",
                         "3": "Satisfecho", "5": "Muy satisfecho"}

        id_issue = self.kwargs['id_issue']
        issue_evaluation = IssueEvaluation.objects.get(issue_id=id_issue)
        issue_evaluation_arr = {
            'time': time_opc[issue_evaluation.time_evaluation],
            'resolve': resolve_opc[issue_evaluation.resolve],
            'difficulty': difficulty_opc[issue_evaluation.difficulty],
            'contact': contact_opc[issue_evaluation.contact],
            "satisfied": satisfied_opc[issue_evaluation.satisfied]
        }
        return JsonResponse(issue_evaluation_arr)


class IssueEvaluationFilter(JSONResponseMixin, CreateView):
    model = IssueEvaluation

    def get(self, request, *args, **kwargs):

        init_date = request.GET['init_date']
        end_date = request.GET['end_date']

        resolve = {'1': 0, '3': 0, '5': 0}
        time = {'1': 0, '2': 0, '3': 0, '5': 0}
        difficulty = {'1': 0, '2': 0, '3': 0, '5': 0}
        contact = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        satisfied = {'1': 0, '2': 0, '3': 0, '5': 0}

        if init_date and end_date:
            issue_evaluations = IssueEvaluation.objects.filter(
                issue__created_at__lte=end_date,
                issue__created_at__gte=init_date)
        else:
            issue_evaluations = IssueEvaluation.objects.all()

        for ev in issue_evaluations:
            time[ev.time_evaluation] = time[ev.time_evaluation] + 1
            resolve[ev.resolve] = resolve[ev.resolve] + 1
            difficulty[ev.difficulty] = difficulty[ev.difficulty] + 1
            contact[ev.contact] = contact[ev.contact] + 1
            satisfied[ev.satisfied] = satisfied[ev.satisfied] + 1

        return JsonResponse({
            "time": time,
            "resolve": resolve,
            "difficulty": difficulty,
            "contact": contact,
            "satisfied": satisfied,
            "cant": len(issue_evaluations)
        })
