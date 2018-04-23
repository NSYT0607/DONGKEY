from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.base import ContextMixin, TemplateView
from schedule.models import Calendar

from .models import ApplyList
from .models import Club
from .models import ClubRule
from .forms import ClubForm
from .forms import ClubRuleForm
from member.models import Member
from board.models import Article, Category


class ClubView(PermissionRequiredMixin, ListView):
    template_name = 'club/admin_club.html'
    context_object_name = 'notice_list'
    paginate_by = 5

    def has_permission(self):
        return Club.objects.filter(pk=self.kwargs['pk'], member__user=self.request.user).exists()

    def get_queryset(self):
        return Article.objects.filter(club__pk=self.kwargs['pk']).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        context['calendar_slug'] = Club.objects.get(pk=self.kwargs['pk']).calendar.slug
        context['club'] = Club.objects.get(pk=self.kwargs['pk'])
        return context


@login_required
def create_club(request):
    club_form = ClubForm(request.POST or None)
    if request.method == 'POST' and club_form.is_valid():
        club = club_form.save(commit=False)
        calendar = Calendar.objects.create(name=club.name, slug=club.name)
        club.calendar = calendar
        club.save()
        member = Member.objects.create(
                club=club,
                user=request.user,
                is_admin=True,
            )
        member.save()

        return redirect(reverse('club:read_admin_club', kwargs={'club': club.name, }))
    ctx = {
        'club_form': club_form,
    }
    return render(request, 'club/club_entry.html', ctx)


@login_required
def read_admin_club(request, club, ctg_pk=None):
    club = Club.objects.get(name=club)
    admin = request.user.member_set.filter(club=club).values('is_admin')
    try:
        notice_list = Article.objects.filter(category__pk=1, club=club)[-5:].get()
    except:
        notice_list = Article.objects.filter(club=club)

    if ctg_pk is not None:
        article_list = Article.objects.filter(category__pk=ctg_pk).filter(club=club).order_by('-updated_at')
        ctg = get_object_or_404(Category, pk=ctg_pk)
    else:
        article_list = Article.objects.filter(club=club).order_by('category__pk', '-updated_at')
        ctg = None
    ctx = {
        'article_list': article_list,
        'ctg_notice': Category.objects.get(name='공지사항'),
        'category_list': Category.objects.exclude(name='공지사항'),
        'ctg_selected': ctg,
        'club': club,
        'notice_list': notice_list,
        'admin': admin,
        'calendar_slug' : club.calendar.slug,
    }
    return render(request, 'club/admin_club.html', ctx)


@login_required
def read_non_admin_club(request, club, ctg_pk=None):
    club = Club.objects.get(name=club)
    if ctg_pk is not None:
        article_list = Article.objects.filter(category__pk=ctg_pk).filter(club=club).order_by('-updated_at')
        ctg = get_object_or_404(Category, pk=ctg_pk)
    else:
        article_list = Article.objects.filter(club=club).order_by('category__pk', '-updated_at')
        ctg = None
    ctx = {
        'article_list': article_list,
        'ctg_notice': Category.objects.get(name='공지사항'),
        'category_list': Category.objects.exclude(name='공지사항'),
        'ctg_selected': ctg,
        'club': club,
    }
    return render(request, 'club/as_member_club.html', ctx)


@login_required
def update_club(request, club_pk):
    club = Club.objects.get(pk=club_pk)
    club_form = ClubForm(request.POST or None, instance=club)
    if request.method == 'POST' and club_form.is_valid():
        club = club_form.save()
        return redirect(reverse('club:read_admin_club', kwargs={'club': club.name, }))
    ctx = {
        'club': club,
        'club_form': club_form,
    }
    return render(request, 'club/update_club.html', ctx)


@login_required
def apply_club(request, club):
    club = Club.objects.get(name=club)
    if request.method == 'POST':
        apply_list = ApplyList.objects.create(
                club=club,
                user=request.user,
            )
        return redirect('core:main_page')

    else:
        return HttpResponse(status=404)


@login_required
def admit(request, pk, club):
    # admit 버튼 클릭 시 해당 계정을 ApplyList에서 지운다.
    # Member에 추가한다.
    # 권한은 0->1로
    apply_user = ApplyList.objects.get(user__pk=pk, club__pk=club)
    if request.method == 'POST':
        Member.objects.create(
                club=apply_user.club,
                user=apply_user.user,
                is_admin=False,
            )
        apply_user.delete()
        return redirect(reverse('club:manage_member', kwargs={'club_pk': club}))

    return HttpResponse(status=404)


@login_required
def update_is_admin(request, club_pk, user_pk):
    club = Club.objects.get(pk=club_pk)
    user = club.member_set.get(user_id=user_pk)
    if request.method == 'POST':
        user.is_admin = True
        user.save()
        return redirect(reverse('club:manage_member', kwargs={'club_pk': club_pk}))

    return HttpResponse(status=404)


@login_required
def exit_club(request, club_pk, user_pk):
    club = Club.objects.get(pk=club_pk)
    user = club.member_set.get(user_id=user_pk)
    if request.method == 'POST':
        member = Member.objects.get(user=user.user)
        member.delete()
        return redirect('core:main_page')

    return HttpResponse(status=404)


@login_required
def manage_member(request, club_pk):
    club = Club.objects.get(pk=club_pk)
    all_member = club.member_set.all()
    applicant_list = club.applylist_set.all()
    ctx = {
        'club': club,
        'all_member': all_member,
        'applicant_list': applicant_list,
    }
    return render(request, 'manage_member.html', ctx)


@login_required
def member_list_for_non_admin(request, club_pk):
    club = Club.objects.get(pk=club_pk)
    all_member = club.member_set.all()
    applicant_list = club.applylist_set.all()
    ctx = {
        'club': club,
        'all_member': all_member,
        'applicant_list': applicant_list,
    }
    return render(request, 'club/member_list_for_non_admin.html', ctx)


def read_apply_list(request, club):
    club = get_object_or_404(Club, name=club)
    apply_list = ApplyList.objects.filter(club__name=club)
    club_member = Member.objects.filter(club__name=club)
    ctx = {
        'club': club,
        'apply_list': apply_list,
        'member_list': club_member,
    }
    return render(request, 'club/read_apply_list.html', ctx)


@login_required
def create_club_rule(request, club):
    club = get_object_or_404(Club, name=club)
    club_rule_form = ClubRuleForm(request.POST or None)

    if request.method == 'POST' and club_rule_form.is_valid():
        form = club_rule_form.save(commit=False)
        form.club = Club.objects.get(name=club)
        form.save()

        return redirect(reverse('club:read_admin_club_rule', kwargs={'club': club.name}))
    return render(request, 'club/club_rule.html', {'club_rule_form': club_rule_form, 'club': club})


def read_admin_club_rule(request, club):
    club = Club.objects.get(name=club)
    club_rule = ClubRule.objects.filter(club=club)
    ctx = {
        'club': club,
        'club_rule': club_rule,
    }
    return render(request, 'club/read_admin_club_rule.html', ctx)


def read_non_admin_club_rule(request, club):
    club = Club.objects.get(name=club)
    club_rule = ClubRule.objects.filter(club=club)
    ctx = {
        'club': club,
        'club_rule': club_rule,
    }
    return render(request, 'club/read_non_admin_club_rule.html', ctx)


@login_required
def update_club_rule(request, club, rule_pk):
    club = get_object_or_404(Club, name=club)
    club_rule = ClubRule.objects.get(club__name=club, pk=rule_pk)
    form = ClubRuleForm(request.POST or None, instance=club_rule)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('club:read_admin_club', kwargs={'club': club}))

    return render(request, 'club/club_rule.html', {'club_rule_form': form, 'club': club})


@login_required
def delete_club_rule(request, club, rule_pk):
    club = Club.objects.get(name=club)
    club_rule = ClubRule.objects.get(club__name=club, pk=rule_pk)
    club_rule.delete()
    return redirect(reverse('club:read_admin_club_rule', kwargs={'club': club}))
