from rest_framework import viewsets
from .models import User, Issue, Rating
from .serializers import UserSerializer, IssueSerializer, RatingSerializer
from django.db.models import Avg
from django.shortcuts import render, redirect
import random

def generate_user_id():
    while True:
        user_id = random.randint(1000, 9999)
        if not User.objects.filter(user_id=user_id).exists():
            return user_id


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Issue ViewSet
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


# Rating ViewSet
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


def home_view(request):
    return render(request, 'home.html')

def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Clear previous session
        request.session.flush()

        # Admin login
        if email == "admin@gmail.com" and password == "admin123":
            request.session['admin'] = True
            return redirect('admin_dashboard')

        try:
            # Existing user login
            user = User.objects.get(email=email, password=password)

        except User.DoesNotExist:
            user = User.objects.create(
            user_name=email.split('@')[0],
            email=email,
            password=password
            )

        # Store user session
        request.session['user_id'] = user.user_id
        request.session['user_name'] = user.user_name

        return redirect('userdashboard')

    return render(request, 'signin.html')

def reportissue_view(request):
    if 'user_id' not in request.session:
        return redirect('signin')

    if 'admin' in request.session:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        if not title or not description or not location:
            return render(request, 'reportissues.html', {
                'error': 'Please fill all required fields'
            })

        user_id = request.session.get('user_id')
        user = User.objects.get(user_id=user_id)

        while True:
            issue_id = "ISS" + str(random.randint(1000, 9999))
            if not Issue.objects.filter(issue_id=issue_id).exists():
                break
        # ✅ Rename image (INSIDE POST)
        if image:
            if '.' in image.name:
                ext = image.name.split('.')[-1]
            else:
                ext = 'jpg'

            image.name = f"{issue_id}.{ext}"
        


        Issue.objects.create(
            issue_id=issue_id,
            issue_type=title,
            description=description,
            location=location,
            status='Pending',
            user=user,
            issue_img=image
        )

        return redirect('userdashboard')

    return render(request, 'reportissues.html')

def userdashboard(request):
    if 'user_id' not in request.session:
        return redirect('signin')

    if 'admin' in request.session:
        return redirect('admin_dashboard')
    

    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)

    issues = Issue.objects.filter(user=user)

    total_complaints = issues.count()
    pending_count = issues.filter(status='Pending').count()
    progress_count = issues.filter(status='In Progress').count()
    resolved_count = issues.filter(status='Resolved').count()

        # Attach rating to each issue
    issue_list = []
    for issue in issues:
        rating_obj = Rating.objects.filter(issue=issue).first()
        rating_value = rating_obj.rating_value if rating_obj else 0

        issue_list.append({
            'issue': issue,
            'rating': rating_value
        })

    context = {
        'user_name': user.user_name,
        'issue_list': issue_list,
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'progress_count': progress_count,
        'resolved_count': resolved_count,
    }

    return render(request, 'userdashboard.html', context)

def profile_view(request):
    if 'user_id' not in request.session:
        return redirect('signin')

    # Admin should not open user profile
    if 'admin' in request.session:
        return redirect('admin_dashboard')

    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)

    # SAVE PROFILE DATA
    if request.method == 'POST':
        user.user_name = request.POST.get('user_name')
        user.contact_no = request.POST.get('contact_no')
        user.city = request.POST.get('city')
        user.gender = request.POST.get('gender')
        user.address = request.POST.get('address')
        user.dob = request.POST.get('dob')
        user.save()

        return redirect('profile')

    # Profile statistics
    issues = Issue.objects.filter(user=user)
    total_issues = issues.count()
    resolved = issues.filter(status='Resolved').count()
    progress = issues.filter(status='In Progress').count()

    context = {
        'user': user,
        'total_issues': total_issues,
        'resolved': resolved,
        'progress': progress,
    }

    return render(request, 'profile.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('home')

def give_rating(request, issue_id):
    # User must be logged in
    if 'user_id' not in request.session:
        return redirect('signin')

    if 'admin' in request.session:
        return redirect('admin_dashboard')

    issue = Issue.objects.get(issue_id=issue_id)

    # Only allow rating if issue is resolved
    if issue.status != 'Resolved':
        return redirect('userdashboard')

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))

        existing_rating = Rating.objects.filter(issue=issue).first()

        if existing_rating:
            existing_rating.rating_value = rating_value
            existing_rating.save()
        else:
            rating_id = "RAT" + str(random.randint(1000,9999))
            Rating.objects.create(
                rating_id=rating_id,
                issue=issue,
                rating_value=rating_value
            )

        return redirect('userdashboard')

    return render(request, 'rating.html', {'issue_id': issue_id})

def admin_dashboard(request):
    if 'admin' not in request.session:
        return redirect('signin')

    issues = Issue.objects.all()

    total_issues = issues.count()
    pending = issues.filter(status='Pending').count()
    progress = issues.filter(status='In Progress').count()
    resolved = issues.filter(status='Resolved').count()

    context = {
        'issues': issues,
        'total_issues': total_issues,
        'pending': pending,
        'progress': progress,
        'resolved': resolved,
    }

    return render(request, 'admin_dashboard.html', context)

def update_status(request, issue_id):
    if 'admin' not in request.session:
        return redirect('signin')

    issue = Issue.objects.get(issue_id=issue_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        issue.status = new_status
        issue.save()
        return redirect('admin_dashboard')

    return render(request, 'update_status.html', {'issue': issue})

def admin_logout(request):
    request.session.flush()
    return redirect('home')
