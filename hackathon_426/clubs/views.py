from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, UserClubInteraction
from django.contrib.auth.decorators import login_required
from accounts.models import newSubmission
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q

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

    # Filter by category if provided
    selected_category = request.GET.get('category')
    if selected_category:
        clubs = clubs.filter(category=selected_category)

    show_empty_message = clubs.count() == 0
    return render(request, "clubs/explore.html", {
        "clubs": clubs,
        "show_empty_message": show_empty_message,
        "selected_category": selected_category,
        "categories": dict(Club.CATEGORY_CHOICES)  # Send categories to template
    })

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
    
    # Get or create an interaction for this user and club
    interaction, created = UserClubInteraction.objects.get_or_create(
        user=user, 
        club_id=club_id,
        defaults={'liked': True}
    )
    
    # Mark as joined
    interaction.joined = True
    interaction.save()
    
    # Redirect back to home page to see updated recommendations
    #return redirect("cart")
    return redirect("clubs_home")
    

def club_detail(request, club_id):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/explore/')
    club = get_object_or_404(Club, id=club_id)
    return render(request, "clubs/club_detail.html", {"club": club})

def home(request):
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/homeclubs/')
    
    # Get user profile
    user = get_object_or_404(newSubmission, id=submission_id)
    
    # Get user's joined clubs (through interactions)
    joined_clubs = Club.objects.filter(
        userclubinteraction__user=user,
        userclubinteraction__joined=True
    )
    
    # Base query for all clubs
    all_clubs = Club.objects.all()
    
    # Create personalized recommendations based on user profile
    recommended_clubs = []
    included_categories = set()  # Track categories we've already included
    
    # 1. Filter by gender for women-focused clubs
    if user.gender == 'female':
        # Look for women's clubs (social sororities, etc.)
        women_clubs = all_clubs.filter(
            Q(category='Social Sorority') |
            Q(description__icontains='women') |
            Q(description__icontains='woman') |
            Q(description__icontains='female') |
            Q(description__icontains='girl') |
            Q(name__icontains='women') |
            Q(name__icontains='woman') |
            Q(name__icontains='girl') |
            Q(name__icontains='sorority')
        ).exclude(id__in=joined_clubs.values_list('id', flat=True))[:1]
        
        for club in women_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # 2. Filter by sports interest
    if user.sports == 'yes' or user.sports == 'maybe':
        sports_terms = [
            'sport', 'athletic', 'fitness', 'gym', 'exercise', 'workout',
            'soccer', 'football', 'basketball', 'baseball', 'volleyball', 
            'tennis', 'swim', 'rugby', 'golf', 'lacrosse', 'hockey', 
            'intramural', 'cycling', 'climb', 'hike', 'run', 'outdoor'
        ]
        
        sports_query = Q()
        for term in sports_terms:
            sports_query |= Q(description__icontains=term) | Q(name__icontains=term)
        
        # Look for sports-related clubs
        sports_clubs = all_clubs.filter(
            sports_query | Q(category='Recreational')
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        for club in sports_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # 3. Filter by major if provided
    if user.major and user.major != '':
        # Clean up the major string for search
        cleaned_major = user.major.lower().replace('_', ' ')
        major_parts = cleaned_major.split()
        
        major_query = Q()
        # Search for each part of the major name
        for part in major_parts:
            if len(part) > 3:  # Only use meaningful parts (skip "and", "of", etc.)
                major_query |= Q(description__icontains=part) | Q(name__icontains=part)
        
        major_related_clubs = all_clubs.filter(
            major_query | Q(category='Academic Major Related') | Q(category='Honor Society')
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        for club in major_related_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # 4. Filter by ethnicity/race if provided
    if user.race and user.race != '' and user.race != 'prefer_not_to_say':
        cultural_mapping = {
            'asian': ['asian', 'chinese', 'japanese', 'korean', 'filipino', 'vietnamese', 'indian', 'pakistani', 'taiwanese'],
            'black': ['black', 'african', 'caribbean', 'afro'],
            'hispanic': ['hispanic', 'latino', 'latina', 'mexican', 'spanish', 'latinx', 'chicanx'],
            'white': ['european', 'slavic', 'italian', 'german', 'french', 'british', 'irish'],
            'native_american': ['native', 'indigenous', 'american indian', 'tribal', 'first nations'],
            'pacific_islander': ['pacific', 'hawaiian', 'islander', 'polynesian', 'samoa']
        }
        
        # Get terms for the user's race
        search_terms = cultural_mapping.get(user.race, [user.race.replace('_', ' ')])
        
        cultural_query = Q()
        for term in search_terms:
            cultural_query |= Q(description__icontains=term) | Q(name__icontains=term)
            
        cultural_clubs = all_clubs.filter(
            cultural_query | Q(category='Cultural')
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        for club in cultural_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # 5. Add religious clubs if we haven't yet
    if 'Religious Based' not in included_categories:
        religious_clubs = all_clubs.filter(
            category='Religious Based'
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        for club in religious_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # 6. Add service clubs if we haven't yet
    if 'Service & Support' not in included_categories:
        service_clubs = all_clubs.filter(
            category='Service & Support'
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        for club in service_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # 7. Add leadership clubs if we haven't yet
    if 'Leadership' not in included_categories and len(recommended_clubs) < 6:
        leadership_clubs = all_clubs.filter(
            category='Leadership'
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        for club in leadership_clubs:
            recommended_clubs.append(club)
            included_categories.add(club.category)
    
    # If we still need more recommendations, add popular clubs
    # from categories we haven't included yet
    remaining_categories = [cat for cat, _ in Club.CATEGORY_CHOICES 
                           if cat not in included_categories]
    
    while len(recommended_clubs) < 6 and remaining_categories:
        next_category = remaining_categories.pop(0)
        next_clubs = all_clubs.filter(
            category=next_category
        ).exclude(id__in=[club.id for club in recommended_clubs + list(joined_clubs)])[:1]
        
        if next_clubs.exists():
            recommended_clubs.append(next_clubs[0])
            included_categories.add(next_category)
    
    # If we STILL don't have enough recommendations, fall back to default hardcoded ones
    if len(recommended_clubs) < 6:
        default_clubs = [
            {
                'id': 'recommended1',
                'name': 'SDSU Strong Girls',
                'description': 'A movement empowering girls to be strong, confident, and believe in themselves through fitness and mentorship.',
                'image': 'sdsustronggirls.jpg'
            },
            {
                'id': 'recommended2',
                'name': 'Intramural Sports Co-ed',
                'description': 'Join our championship-winning intramural sports program for fun, competitive play across multiple sports and make lifelong friends.',
                'image': 'intramuralSportsCo-ed.png'
            },
            {
                'id': 'recommended3',
                'name': 'SDSU Salsa Club',
                'description': 'Learn to dance salsa and experience Latin culture through music, events, and performances with an enthusiastic community.',
                'image': 'salsaclub.jpeg'
            },
            {
                'id': 'recommended4',
                'name': 'SDSU Gaming Guild',
                'description': 'Connect with fellow gamers for tournaments, casual play, and discussions about all types of games from tabletop to digital.',
                'image': 'default_club.jpg'
            },
            {
                'id': 'recommended5',
                'name': 'Future Business Leaders',
                'description': 'Develop professional skills through networking events, workshops, and mentorship opportunities with industry leaders.',
                'image': 'default_club.jpg'
            },
            {
                'id': 'recommended6',
                'name': 'Aztec Engineers Society',
                'description': 'Join a community of engineering students collaborating on projects, competitions, and professional development.',
                'image': 'default_club.jpg'
            }
        ]
        
        needed = 6 - len(recommended_clubs)
        recommended_clubs.extend(default_clubs[:needed])
    
    # Make sure we only return exactly 6 recommendations
    recommended_clubs = recommended_clubs[:6]
    
    return render(request, 'clubs/home.html', {
        'recommended_clubs': recommended_clubs,
        'joined_clubs': joined_clubs
    })

def remove_club(request, club_id):
    """
    Remove a club from the user's joined clubs list
    """
    submission_id = request.session.get('submission_id')
    if not submission_id:
        return redirect('/accounts/login/?next=/clubs/homeclubs/')
    
    user = get_object_or_404(newSubmission, id=submission_id)
    
    # Find the interaction for this club
    interaction = get_object_or_404(
        UserClubInteraction, 
        user=user, 
        club_id=club_id,
        joined=True
    )
    
    # Set joined to False
    interaction.joined = False
    interaction.save()
    
    return redirect("clubs_home")
