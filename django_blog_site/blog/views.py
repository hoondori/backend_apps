from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

def post_list(request, tag_slug=None):
  all_posts = Post.published.all()
  tag = None
  if tag_slug: # if tag is given, filter by tag
    tag = get_object_or_404(Tag, slug=tag_slug)
    all_posts = all_posts.filter(tags__in=[tag])

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
                {'posts': posts, 'tag': tag})

def post_detail(request, year, month, day, slug):
  # for better SEO
  post = get_object_or_404(
    Post, 
    status=Post.Status.PUBLISHED,
    slug=slug,
    publish__year=year,
    publish__month=month,
    publish__day=day)
  
  # retrieve comments related to this post
  comments = post.comments.filter(active=True)

  # comment form 
  form = CommentForm()

  # fine similiar posts based on tags
  post_tags_ids = post.tags.values_list('id', flat=True)

  similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                .exclude(id=post.id)

  similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                               .order_by('-same_tags', '-publish')[:4]
  return render(request, 
                'blog/post/detail.html', 
                {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})

def post_share(request, post_id):

  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
  sent = False 
  if request.method == 'POST': # if form was submitted
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(
        post.get_absolute_url())
      subject = f"{cd['name']} recommends you to read {post.title}"
      message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']} \'s comments: {cd['comments']}" 
      send_mail(subject, message, 'awshoondori@gmail.com', [cd['to']])
      sent = True
  else:
    form = EmailPostForm()
  
  
  return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)  
  comment = None

  form = CommentForm(data=request.POST)
  if form.is_valid():
    
    # make foreign relatioship to post and commit to db
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
  
  return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})
  
def post_search(request):
  form = SearchForm()
  query = None
  results = []

  if 'query' in request.GET:
    form = SearchForm(request.GET)
    if form.is_valid():
      query = form.cleaned_data['query']

      # 형태소, 불용어 처리 후의 query로 찾고, rank를 매겨서 높은 rank를 반환
      search_vector = SearchVector('title', weight='A') + \
                      SearchVector('body', weight='B')
      search_query = SearchQuery(query)
      search_rank = SearchRank(search_vector, search_query)

      results = Post.published\
        .annotate(search=search_vector, rank=search_rank)\
        .filter(rank__gte=0.3)\
        .order_by('-rank')

      # results = Post.published.annotate(similarity=TrigramSimilarity('title', query),)\
      #               .filter(similarity__gt=0.1).order_by('-similarity')

  return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})