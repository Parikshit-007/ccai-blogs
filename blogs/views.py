from django.shortcuts import redirect, render

# Create your views here.
# views.py
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import BlogPost, Contact
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import SearchForm

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'aboutus.html')

from .forms import SearchForm

from urllib.parse import unquote

class SubscribeView(View):
    template_name = 'subscribe.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        # Here, you can add logic to save the email to your database or send it to an external service.
        # For simplicity, let's just send a confirmation email to the entered email address.

        # Send confirmation email
        send_mail(
            'Subscription Confirmation',
            'Thank you for subscribing to CareChainAI. You will receive updates whenever we publish new content.',
            'carechainai@gmail.com',  # Replace with your email address
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Subscription successful!'})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        results = []

        if form.is_valid():
            try:
                query = form.cleaned_data['q']

                # Perform case-insensitive search in both title and content
                results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
            except KeyError as e:
                print(f"KeyError: {e}")
                print(f"Form cleaned_data: {form.cleaned_data}")

        context = {'form': form, 'results': results}
        return render(request, self.template_name, context)

def contactus(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'contact.html', {'thank': thank})

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'blog.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        BlogPost.objects.create(title=title, content=content, author=author)
        return redirect('blog_list')
    return render(request, 'blog/add_post.html')

def view_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    return render(request, 'fullview.html', {'post': post})

@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('blog_list')
