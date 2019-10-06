from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

def index(request):
    latest_ques_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_ques_list': latest_ques_list,
    }
    return  render(request, 'polls/index.html', context)

def detail(request, question_id):

    '''
    The get_object_or_404() function takes a Django model as its first argument
    and an arbitrary number of keyword arguments, which it passes to the get()
    function of the model’s manager. It raises Http404 if the object doesn’t
    exist.

    There’s also a get_list_or_404() function, which works just as
    get_object_or_404() – except using filter() instead of get(). It raises
    Http404 if the list is empty.

    --Philosophy--
    Why do we use a helper function get_object_or_404() instead of automatically
    catching the ObjectDoesNotExist exceptions at a higher level,
    or having the model API raise Http404 instead of ObjectDoesNotExist?

    Because that would couple the model layer to the view layer. One of the
    foremost design goals of Django is to maintain loose coupling.
    Some controlled coupling is introduced in the django.shortcuts module.
    '''

    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    # try:
    #     question = Question.objects.get(pk=question_id)
    #     context = {
    #         'question': question
    #     }
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    response = "You are looking at results of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice".
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        '''
        Always return an HttpResponseRedirect after successfully dealing
        with POST data. This prevents data from being posted twice if a
        user hits the Back button.

        You should always return an HttpResponseRedirect after successfully 
        dealing with POST data. This tip isn’t specific to Django; it’s just
        good Web development practice.
        '''
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
