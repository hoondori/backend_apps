from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


def post_list(request):
  all_posts = Post.published.all()

  # restrict number of posts displayed in one page to enhance readability
  paginator = Paginator(all_posts, 3)
  page_number = request.GET.get('page', 1)
  try:
    posts = paginator.page(page_number)
  except EmptyPage:
    # if the requested page number is not valid, use last available page instead.
    posts = paginator.page(paginator.num_pages)

  return render(request, 
                'blog/post/list.html', 
                {'posts': posts})

def post_detail(request, year, month, day, slug):
  # try:
  #   post = Post.published.get(id=id)
  # except Post.DoesNotExist:
  #   raise Http404("No Post found.")

  # for better SEO
  post = get_object_or_404(
    Post, 
    status=Post.Status.PUBLISHED,
    slug=slug,
    publish__year=year,
    publish__month=month,
    publish__day=day)

  return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):

  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
  sent = False 
  if request.method == 'POST': # if form was submitted
    print(request.POST)
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(
        post.get_absolute_url())
      subject = f"{cd['name']} recommends you to read {post.title}"
      message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']} \'s comments: {cd['comments']}" 
      print(message)
      send_mail(subject, message, 'awshoondori@gmail.com', [cd['to']])
      sent = True
      
  else:
    print("babo#1")
    form = EmailPostForm()
  
  
  return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})




