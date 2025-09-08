from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import question, answer
from django.views import View

from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse

class MainView(View):
    def get(self, request):
        list_last_questions = answer.objects.order_by("-Posted on")
        context = {'answers': list_last_questions}
        return render(request, 'forum/index.html', context)

class QuestionView(View):
    def get(self, request, question_id):
        try:
            Question = question.objects.get(pk=question_id)
        except question.DoesNotExist:
            raise Http404("Question does not exist")
        context = {'question': Question}
        return render(request, 'forum/details.html', context)
    
class VoteView(View):
    def get(self, request, Question_id):
        try:
            Question = question.objects.get(pk=Question_id)
        except question.DoesNotExist:
            raise Http404("question does not exist")
        return HttpResponse(str(Question) + "; votes: " + str(Question.votes))

    def post(self, request, Question_id):
        try:
            Question = question.objects.get(pk=Question_id)
        except question.DoesNotExist:
            raise Http404("question does not exist")
        Question.votes += 1
        Question.save()
        return redirect(reverse('forum:details', args=[Question.pergunta.id]))

class MakeQuestionView(View):
    def get(self, request):
        return render(request, 'forum/AskQuestion.html')

    def post(self, request):
        if request.user.is_authenticated:
            User = request.user.username
        else:
            User = 'anonymous'
        title = request.POST.get('title')
        details = request.POST.get('details')
        trying = request.POST.get('trying')
        cdate = timezone.now()
        
        Question = question(title=title, details=details, 
        trying=trying, 	cdate=cdate, User=User)
        Question.save()

        return redirect(reverse('forum:detalhe', args=[Question.id]))
    
class AnswerSomething(View):
    def get(self, request, Question_id):
        try:
            Question = question.objects.get(pk=Question_id)
        except question.DoesNotExist:
            raise Http404("Question does not exist")
        context = {'Question' : question}
        return render(request, 'forum/answersomething.html', context)

    def post(self, request, pergunta_id):
        try:
            Question = question.objects.get(pk=pergunta_id)
        except question.DoesNotExist:
            raise Http404("Question does not exist")

        if request.user.is_authenticated:
            User = request.user.username
        else:
            User = 'anonymous'
        text = request.POST.get('text')
        cdate = timezone.now()
        
        Question.answer_set.create(text=text, cdate=cdate, User=User)

        return redirect(reverse('forum:details', args=[Question.id]))

