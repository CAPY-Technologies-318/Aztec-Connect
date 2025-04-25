from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, UserClubInteraction
from django.contrib.auth.decorators import login_required
from accounts.models import newSubmission
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def explore_clubs(request):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/explore/')
    user = get_object_or_404(newSubmission, id=submission_id)

    excluded_clubs = UserClubInteraction.objects.filter(user=user, disliked=True).values_list('club_id', flat=True)
    clubs = Club.objects.exclude(id__in=excluded_clubs)[:10]
    return render(request, "clubs/explore.html", {"clubs": clubs})

@csrf_exempt  # optionally replace with @require_POST + CSRF middleware if needed
def swipe_club(request, club_id, action):
    if request.method == 'POST':
        submission_id = request.session.get('submission_id')
        if not submission_id:
            return redirect('/accounts/login/?next=/clubs/explore/')
        user = get_object_or_404(newSubmission, id=submission_id)

        club = get_object_or_404(Club, id=club_id)
        interaction, _ = UserClubInteraction.objects.get_or_create(user=user, club=club)

        if action == "like":
            interaction.liked = True
            interaction.disliked = False
        elif action == "dislike":
            interaction.liked = False
            interaction.disliked = True
        interaction.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)

def cart_view(request):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/explore/')
    user = get_object_or_404(newSubmission, id=submission_id)

    cart = UserClubInteraction.objects.filter(request.user, liked=True, joined=False)
    return render(request, "clubs/cart.html", {"cart": cart})

def join_club(request, club_id):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/explore/')
    user = get_object_or_404(newSubmission, id=submission_id)
    interaction = get_object_or_404(UserClubInteraction, user=user, club_id=club_id)
    interaction.joined = True
    interaction.save()
    return redirect("cart")

def club_detail(request, club_id):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/explore/')
    club = get_object_or_404(Club, id=club_id)
    return render(request, "clubs/club_detail.html", {"club": club})