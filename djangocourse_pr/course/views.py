from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from .models import *
from auth_reg.models import *
import pandas
import json

# Create your views here.
def main_view(request):
    context = {}
    # если пользователь авторизован
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['signed_in'] = True
        
    return render(request, 'course/main.html', context)

# для страницы курса со всеми заданиями
def course_view(request):
    context = {}
    sentences_dict_list = []
    
    try:
        user_status = UserProfile.objects.get(user=request.user)
        
        if user_status.role == 'teacher':
            context['user_status'] = 'teacher'
        elif user_status.role == 'student':
            context['user_status'] = 'student'
    except UserProfile.DoesNotExist: pass
        
    # если пользователь авторизован
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['signed_in'] = True
        
    if request.method == 'POST':
        # если добавляем задание
        if 'add_task' in request.POST:
            task_name = request.POST.get('taskname')
            task_file = request.FILES.get('taskfile')
            additional_words_file = request.FILES.get('additional_words_file')
            selected_lesson_value = request.POST.get('selected_lesson_value')
            
            if task_name and task_file and additional_words_file and selected_lesson_value:
                sentences = pandas.read_excel(task_file)
                additional_words = pandas.read_excel(additional_words_file)
                
                english_sentences = []
                ukrainian_sentences = []
                additional_words_list = []

                for row in sentences.itertuples(index=False):
                    column1_value = row[0] # английское предложение
                    column2_value = row[1] # украинское предложение
                    
                    # Подготавливаем предложения и списки с ними для загрузки в модель при создании урока
                    cleaned_value_column1 = column1_value.strip()
                    lines_column1 = cleaned_value_column1.split('\n')
                    cleaned_value_column2 = column2_value.strip()
                    lines_column2 = cleaned_value_column2.split('\n')

                    lines_eng = []
                    lines_ukr = []

                    for line in lines_column1:
                        stripped_line = line.strip()
                        if stripped_line:
                            lines_eng.append(stripped_line)
                            
                    for line in lines_column2:
                        stripped_line = line.strip()
                        if stripped_line:
                            lines_ukr.append(stripped_line)

                    if lines_eng and lines_ukr:
                        english_sentences.extend(lines_eng)
                        ukrainian_sentences.extend(lines_ukr)

                for row in additional_words.itertuples(index=False):
                    word_value = row[0]
                    lines_word = [line.strip() for line in word_value.strip().split('\n') if line.strip()]
                    
                    if lines_word:
                        additional_words_list.extend(lines_word)

                # print(english_sentences)
                # print(ukrainian_sentences)
                # print(additional_words_list)
                
                selected_lesson = Lesson.objects.get(id=selected_lesson_value)
                
                task = UserProgress.objects.create(
                    lesson = selected_lesson,
                    task_name = task_name,
                    english_sentences = english_sentences,
                    ukrainian_sentences = ukrainian_sentences,
                    additional_words = additional_words_list,
                )
                
                task_url = reverse('task_detail', args=[task.id])
                print(task_url)
                
                task_html = render_to_string('course/task_block.html', {
                    'task': task,
                    'task_url': task_url,
                }, request=request)
        
                return JsonResponse({
                    'addName': True,
                    'error': '',
                    'task_html': task_html,
                })
            else:
                return JsonResponse({'error': 'Заповніть усі поля'})
        
        # если удаляем задание
        if 'delete_task' in request.POST:
            # узначем, какое задание надо удалять
            task_id = request.POST.get('task_id')
            try:
                # получаем его из бд и удаляем на стороне сервера
                task = UserProgress.objects.get(id=task_id)
                task.delete()
                # отправляем ajax-у, что можно удалять задание на стороне клиента
                return JsonResponse({'deleteTask': True})
            # на крайняк, если задания каким-то образом не будет
            except UserProgress.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Завдання не знайдено'})
            
        if 'add_lesson' in request.POST:
            lesson_name = request.POST.get('lessonname')
            lesson_id = request.POST.get('lesson_id')
            
            if lesson_name:
                lesson = Lesson.objects.create(lesson_name=lesson_name)
                lesson_id = lesson.id
                
                lesson_html = render_to_string('course/lesson_block.html', {
                    'lesson': lesson    
                }, request=request)
                
                return JsonResponse({
                    'addLesson': True,
                    'lessonId': lesson_id,
                    'lessonName': lesson_name,
                    'lesson_html': lesson_html,
                })
            else:
                return JsonResponse({'error': 'Заповніть поле з назвою уроку'})
        
        if 'delete_lesson' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                lesson.delete()
                return JsonResponse({'deleteLesson': True})
            except Lesson.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Урок не знайдений'})
            
    all_lessons = Lesson.objects.all()
    lessons_with_tasks = []
    
    for lesson in all_lessons:
        tasks = UserProgress.objects.filter(lesson=lesson)
        lessons_with_tasks.append({
            'lesson': lesson,
            'tasks': tasks,
        })
    
    context['lessons_with_tasks'] = lessons_with_tasks
    
    return render(request, 'course/course.html', context)

# Для страницы каждого задания
def task_detail_view(request, task_id):
    context = {}
    # если пользователь авторизован
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['signed_in'] = True
        
    task = get_object_or_404(UserProgress, id=task_id)
    
    english_sentences = task.english_sentences
    ukrainian_sentences = task.ukrainian_sentences
    additional_words = task.additional_words
    
    if request.method == 'POST':
        # Получаем задание на котором находимся
        current_index = int(request.POST.get('current_index', 0))

        if current_index < len(english_sentences) - 1:
            next_english_sentence = english_sentences[current_index + 1]
            next_ukrainian_sentence = ukrainian_sentences[current_index + 1]
            
            response_data = {
                'english_sentence': next_english_sentence,
                'ukrainian_sentence': next_ukrainian_sentence,
                'next_index': current_index + 1,
                'additional_words': additional_words,
            }
        else:
            response_data = {'error': True}

        return JsonResponse(response_data)

    # получаем первое предложение
    first_english_sentence = english_sentences[0]
    first_ukrainian_sentence = ukrainian_sentences[0]
    context['task'] = task  # передаем конкретное задание, на котором находимся через контекст
    context['first_english_sentence'] = first_english_sentence  # передаем первое предложение на английском через контекст
    context['first_ukrainian_sentence'] = first_ukrainian_sentence  # передаем первое предложение на украинском через контекст
    context['sentences_len'] = range(1, len(english_sentences) + 1)  # передаем количество предложений через контекст
    context['additional_words_first'] = additional_words  # передаем дополнительные слова через контекст
    
    # context['task_after_restart'] = user_progress.current_index
    
    return render(request, 'course/task_detail.html', context)
