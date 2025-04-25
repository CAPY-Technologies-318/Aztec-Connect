from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, UserClubInteraction
from django.contrib.auth.decorators import login_required
from accounts.models import newSubmission
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count

# Create your views here.
def explore_clubs(request):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/explore/')
    user = get_object_or_404(newSubmission, id=submission_id)

    interactions = UserClubInteraction.objects.filter(user=user)
    liked_or_joined = interactions.filter(liked=True) | interactions.filter(joined=True)
    liked_or_joined_club_ids = liked_or_joined.values_list('club_id', flat=True)
    disliked_club_ids = list(interactions.filter(disliked=True).values_list('club_id', flat=True))
    if disliked_club_ids:
        clubs = Club.objects.filter(id__in=disliked_club_ids).exclude(id__in=liked_or_joined_club_ids)
    else:
        clubs = Club.objects.exclude(id__in=liked_or_joined_club_ids)
    show_empty_message = clubs.count() == 0
    return render(request, "clubs/explore.html", {"clubs": clubs, "show_empty_message": show_empty_message})

@csrf_exempt
def reset_swipes(request):
    if request.method == 'POST':
        submission_id = request.session.get('submission_id')
        if submission_id:
            user = get_object_or_404(newSubmission, id=submission_id)
            UserClubInteraction.objects.filter(user=user, disliked=True).update(disliked=False)
    return redirect('explore')


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
    cart = UserClubInteraction.objects.filter(user=user, liked=True, joined=False)
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

def dashboard_view(request):
    return render(request, "clubs/dashboard.html")

def home(request):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/homeclubs/')

    stem_clubs = Club.objects.filter(category='STEM')[:4]
    sports_clubs = Club.objects.filter(category='SPORTS')[:4]
    culture_clubs = Club.objects.filter(category='CULTURE')[:4]

    context = {
        'stem_clubs': stem_clubs,
        'sports_clubs': sports_clubs,
        'culture_clubs': culture_clubs,
    }
    
    return render(request, 'clubs/home.html', context)
