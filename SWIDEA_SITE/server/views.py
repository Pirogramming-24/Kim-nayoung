import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import Idea, IdeaStar, DevTool
from .forms import IdeaForm, DevToolForm
from django.core.paginator import Paginator
from django.db.models import Count

# Create your views here.
def main(request):
    sort = request.GET.get('sort', 'recent')
    ideas = Idea.objects.annotate(star_count=Count('stars'))

    if sort == 'name':
        # 이름 가나다순
        ideas_list = ideas.order_by('title')
    elif sort == 'stars':
        # 찜한거 먼저 그 다음엔 최신순
        ideas_list = ideas.order_by('-star_count', '-created_at')
    elif sort == 'old':
        # 등록순
        ideas_list = ideas.order_by('created_at')
    else:
        # 최신순
        ideas_list = ideas.order_by('-created_at')

    paginator = Paginator(ideas_list, 4)
    page = request.GET.get('page', 1)
    ideas = paginator.get_page(page)
    
    context = {
        'ideas': ideas,
        'sort': sort
    }
    return render(request, 'server/idea_list.html', context)

#  1. 아이디어 생성
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('server:main')
    else:
        form = IdeaForm()
    
    context = {
        'form': form
    }
    return render(request, 'server/idea_create.html', context)

#  2. 아이디어 디테일
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    context = {'idea': idea}
    return render(request, 'server/idea_detail.html', context)

#  3. 아이디어 수정
def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if request.method == 'POST':
        # 기존 내용(instance=idea)을 가져와서 수정된 내용(request.POST)을 덮어씌움
        form = IdeaForm(request.POST, request.FILES, instance=idea) 
        if form.is_valid():
            form.save()
            return redirect('server:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
        
    context = {'form': form, 'idea': idea}
    return render(request, 'server/idea_update.html', context)

#  4. 아이디어 삭제
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if request.method == 'POST':
        idea.delete()
        return redirect('server:main')
        
    return redirect('server:idea_detail', pk=pk)

# ------------------

# 1. 개발툴 리스트
def devtool_list(request):
    devtools = DevTool.objects.all()
    context = {'devtools': devtools}
    return render(request, 'server/devtool_list.html', context)

# 2. 개발툴 등록
def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('server:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    
    context = {'form': form}
    return render(request, 'server/devtool_form.html', context)

# 3. 개발툴 상세
def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    
    related_ideas = devtool.idea_set.all()
    
    context = {
        'devtool': devtool,
        'related_ideas': related_ideas
    }
    return render(request, 'server/devtool_detail.html', context)

# 4. 개발툴 수정
def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect('server:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    
    context = {'form': form, 'devtool': devtool}
    return render(request, 'server/devtool_form.html', context)

# 5. 개발툴 삭제
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        devtool.delete()
        return redirect('server:devtool_list')
    return redirect('server:devtool_detail', pk=pk)

@require_POST
def idea_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    star, created = IdeaStar.objects.get_or_create(idea=idea)
    if created:
        is_starred = True
    else:
        star.delete()
        is_starred = False

    return JsonResponse({'is_starred': is_starred})

@require_POST
def idea_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    data = json.loads(request.body)
    action = data.get('action')

    if action == 'inc':
        idea.interest += 1
    elif action == 'dec':
        idea.interest -= 1
        
    idea.save()

    return JsonResponse({'interest': idea.interest})