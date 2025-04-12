from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .models import Post


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

