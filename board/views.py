from django.shortcuts import render, redirect, get_object_or_404
from .models import Article,  Comment, Category
from .forms import ArticleForm, CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from club.models import Club


@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST or None)
    if request.method == "POST" and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.author = request.user
        new_comment.save()
        return redirect(article.get_absolute_url())
    ctx = {
            'article': article,
            'form': comment_form,
    }
    return render(request, 'board/article_detail.html', ctx)


@login_required
def article_detail_admin(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST or None)
    if request.method == "POST" and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.author = request.user
        new_comment.save()
        return redirect(reverse('board:article_detail_admin', kwargs={'pk': pk, }))
    ctx = {
            'article': article,
            'form': comment_form,
    }
    return render(request, 'board/article_detail_admin.html', ctx)


def article_list(request, club_pk, ctg_pk=None):
    club = get_object_or_404(Club, pk=club_pk)
    if ctg_pk is not None:
        article_list = Article.objects.filter(category__pk=ctg_pk).filter(club=club_pk).order_by('-updated_at')
        ctg = get_object_or_404(Category, pk=ctg_pk)
    else:
        article_list = Article.objects.filter(club=club_pk).order_by('category__pk', '-updated_at')
        ctg = None
    ctx = {
            'article_list': article_list,
            'ctg_notice': Category.objects.get(name='공지사항'),
            'category_list': Category.objects.exclude(name='공지사항'),
            'ctg_selected': ctg,
            'club': club,
    }
    return render(request, 'board/article_list.html', ctx)


@login_required
def article_create(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    member = club.member_set.get(user=request.user)
    form = ArticleForm(member, request.POST or None)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.club = club
        article.author = request.user
        article.save()
        return redirect(article.get_absolute_url())
    ctx = {
            'form': form
    }
    return render(request, 'board/article_create.html', ctx)


@login_required
def article_create_admin(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    member = club.member_set.get(user=request.user)
    form = ArticleForm(member, request.POST or None)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.club = club
        article.author = request.user
        article.save()
        return redirect(reverse('board:article_detail_admin', kwargs={'pk': article.pk, }))
    ctx = {
            'form': form
    }
    return render(request, 'board/article_create_admin.html', ctx)


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    member = request.user.member_set.get(club__pk=article.club.pk)
    form = ArticleForm(member, request.POST or None, instance=article)
    if request.method == "POST" and form.is_valid():
        article = form.save()
        return redirect(article.get_absolute_url())
    ctx = {
            'form': form
    }
    return render(request, 'board/article_create.html', ctx)


@login_required
def article_update_admin(request, pk):
    article = get_object_or_404(Article, pk=pk)
    member = request.user.member_set.get(club__pk=article.club.pk)
    form = ArticleForm(member, request.POST or None, instance=article)
    if request.method == "POST" and form.is_valid():
        article = form.save()
        return redirect(reverse('board:article_detail_admin', kwargs={'pk': pk, }))
    ctx = {
            'form': form
    }
    return render(request, 'board/article_create_admin.html', ctx)


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect(reverse('club:read_non_admin_club', kwargs={'club': article.club.name, }))


@login_required
def article_delete_admin(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect(reverse('club:read_admin_club', kwargs={'club': article.club.name, }))


def article_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.liked_article_set.filter(pk=pk).exists():
        article.liker_set.remove(request.user)
    else:
        article.liker_set.add(request.user)
    return redirect(article.get_absolute_url())


def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article = comment.article
    if request.user.liked_comment_set.filter(pk=pk).exists():
        comment.liker_set.remove(request.user)
    else:
        comment.liker_set.add(request.user)
    return redirect(article.get_absolute_url())


