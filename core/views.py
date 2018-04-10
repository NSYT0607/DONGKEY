from django.shortcuts import render

# Create your views here.
from member.models import Member
from club.models import Club


def main_page(request):
    admin_member = Member.objects.filter(user__pk=request.user.pk, is_admin=True)
    as_member = Member.objects.filter(user__pk=request.user.pk, is_admin=False)

    ctx = {
        'search_result': search(request)[1],
        'q': search(request)[0],
        'admin_club_list': admin_member,
        'member_club_list': as_member,
    }
    return render(request, 'main.html', ctx)


def search(request):
    search_text = request.GET.get('q', '')
    if search_text:
        club_result = Club.objects.filter(name__icontains=search_text)

        for club in club_result:

            if request.user.id is not None:
                club.is_member = club.member_set.filter(user=request.user).exists()
                club.is_applied = club.applylist_set.filter(user=request.user).exists()
            else:
                club.is_member = False
                club.is_applied = False

        return (search_text, club_result)
    else:
        club_result = None
        return (search_text, club_result)
