from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponse

from club.models import Club
from .models import AdminResume, ApplicantResume, Question
from .forms import QuestionForm, AdminResumeForm, ApplicantResumeForm, ShortAnswerForm, LongAnswerForm, AcceptForm

@login_required
def admin_resume_list_for_admin(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    resume_list = AdminResume.objects.filter(club=club)
    ctx = {
        'club': club,
        'resume_list': resume_list,
    }
    return render(request, 'recruiting/admin_resume_list_for_admin.html', ctx)

@login_required
def create_admin_resume(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    admin_resume_form = AdminResumeForm(request.POST or None)
    if request.method =="POST" and admin_resume_form.is_valid():
        resume = admin_resume_form.save(commit=False)
        resume.club = club
        resume.save()
        return redirect(reverse('recruiting:read_admin_resume', kwargs={
            'club_pk': club.pk,
            'resume_pk': resume.pk,
        }))
    ctx ={
        'club': club,
        'admin_resume_form': admin_resume_form,
    }
    return render(request,'recruiting/create_admin_resume.html', ctx)

@login_required
def read_admin_resume(request, club_pk, resume_pk):
    club = get_object_or_404(Club, pk=club_pk)
    admin_resume = get_object_or_404(AdminResume, pk=resume_pk)
    ctx = {
        'club': club,
        'admin_resume': admin_resume,
        'question_form': QuestionForm(),
    }
    return render(request, 'recruiting/read_admin_resume.html', ctx)

@login_required
def create_question(request, club_pk, resume_pk):
    if request.method == "POST":
        club = Club.objects.get(pk=club_pk)
        resume = get_object_or_404(AdminResume, pk=resume_pk)
        question_form = QuestionForm(request.POST)

        if question_form.is_valid(): # 추가 질문 내용이 추가 안됨
            question = question_form.save(commit=False)
            question.admin_resume = resume
            question.save()

            return render(request, 'recruiting/question.html', {'question': question, })
            # return HttpResponseRedirect("recruiting/question.html", {'question': question})
    return HttpResponse(status=405)
    # return render_to_response('recruiting/question.html', {'question': question })

def update_question(request, question_pk):
    form = QuestionForm(
        request.POST or None,
        instance= Question.objects.get(pk=question_pk),
    )
    if request.method == 'POST' and form.is_valid():
        question = form.save()
        # return redirect(reverse('recruiting:read_admin_resume', kwargs={
        #     'club_pk': question.admin_resume.club.pk,
        #     'resume_pk': question.admin_resume.pk,
        # }))
    ctx = {
        'form': form,
    }
    return render(request, 'recruiting/update_question.html', ctx)


def delete_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    question.delete()
    return redirect(reverse('recruiting:read_admin_resume',  kwargs={
            'club_pk': question.admin_resume.club.pk,
            'resume_pk': question.admin_resume.pk,
            }))


@login_required
def read_applicant_resume_list(request, club_pk, resume_pk):
    club = get_object_or_404(Club, pk=club_pk)
    applicant_resume_list = ApplicantResume.objects.filter(admin_resume__pk=resume_pk)
    admin_resume =AdminResume.objects.get(pk=resume_pk)
    ctx = {
        'club':club,
        'admin_resume': admin_resume,
        'applicant_resume_list': applicant_resume_list,
    }
    return render(request, 'recruiting/read_applicant_resume_list.html', ctx)

@login_required
def read_applicant_resume_for_admin(request, club_pk, resume_pk):
    club = Club.objects.get(pk=club_pk)
    resume = ApplicantResume.objects.get(pk=resume_pk)
    ctx ={
        'club': club,
        'resume': resume,
        'accept_form': AcceptForm(request.POST or None, instance=resume),
    }
    return render(request, 'recruiting/read_applicant_resume_for_admin.html', ctx)

@login_required
def admin_resume_list_for_applicant(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    admin_resume_list = AdminResume.objects.filter(club=club)
    is_member = request.user.member_set.filter(club__pk=club_pk).exists()
    ctx ={
        'club': club,
        'admin_resume_list': admin_resume_list,
        'is_member': is_member,
    }
    return render(request, 'recruiting/admin_resume_list_for_applicant.html', ctx)


def answer_formset_factory(question_list, data=None):
    formset = []
    for question in question_list:
        if question.is_short_answer:
            form = ShortAnswerForm(data, prefix=question.pk)
        else:
            form = LongAnswerForm(data, prefix=question.pk)
        form.question = question
        formset.append(form)
    return formset

@login_required
def create_applicant_resume(request, club_pk, resume_pk):
    club = Club.objects.get(pk=club_pk)
    admin_resume = get_object_or_404(AdminResume, pk=resume_pk)
    question_list = Question.objects.filter(admin_resume__pk=resume_pk)

    applicant_resume_form = ApplicantResumeForm(request.POST or None, request.FILES or None)

    short_question_list = [q for q in question_list if q.is_short_answer]
    short_answer_formset = answer_formset_factory(short_question_list, data=request.POST or None)

    long_question_list = [q for q in question_list if not q.is_short_answer]
    long_answer_formset = answer_formset_factory(long_question_list, data=request.POST or None)

    if request.method == 'POST' and applicant_resume_form.is_valid():
        if request.user.applicantresume_set.filter(admin_resume=admin_resume).exists():
            return HttpResponse(status=404)
        else:
            resume = applicant_resume_form.save(commit=False)
            resume.admin_resume = admin_resume
            resume.applicant = request.user
            resume.save()

            for short_answer_form in short_answer_formset:
                short_answer = short_answer_form.save(commit=False)
                short_answer.applicant_resume = resume
                short_answer.question = short_answer_form.question
                short_answer.save()
            for long_answer_form in long_answer_formset:
                long_answer = long_answer_form.save(commit=False)
                long_answer.applicant_resume = resume
                long_answer.question = long_answer_form.question
                long_answer.save()

            return redirect(reverse('recruiting:read_applicant_resume_for_applicant', kwargs={
                'club_pk': club.pk,
                'resume_pk': resume.pk,
            }))
    ctx = {
        'club': club,
        'resume': admin_resume,
        'applicant_resume_form': applicant_resume_form,
        'short_answer_formset': short_answer_formset,
        'long_answer_formset': long_answer_formset,
    }
    return render(request, 'recruiting/create_applicant_resume.html', ctx)


@login_required
def read_applicant_resume_for_applicant(request, club_pk, resume_pk):
    club = Club.objects.get(pk=club_pk)
    resume = ApplicantResume.objects.get(pk=resume_pk)
    ctx ={
        'club': club,
        'resume': resume,
    }
    return render(request, 'recruiting/read_applicant_resume_for_applicant.html', ctx)


def accept_applicant(request, resume_pk):
    applicant_resume = get_object_or_404(ApplicantResume, pk=resume_pk)
    form = AcceptForm(request.POST or None, instance=applicant_resume)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('recruiting:read_applicant_resume_list', kwargs={
            'club_pk': applicant_resume.admin_resume.club.pk,
            'resume_pk': applicant_resume.admin_resume.pk,
        }))
    else:
        return HttpResponse(status=405)


def delete_applicant_resume(request, resume_pk):
    if request.method == "POST":
        applicant_resume = get_object_or_404(ApplicantResume, pk=resume_pk)
        applicant_resume.delete()
        return redirect(reverse('recruiting:admin_resume_list_for_applicant', kwargs={
            'club_pk': applicant_resume.admin_resume.club.pk,
        }))
    else:
        return HttpResponse(status=400)