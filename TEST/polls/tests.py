'''
INTRODUCTION

In effect, we are using the tests
to tell a story of admin input and user experience
on the site, and checking that at every state and for
every new change in the state of the system, the expected
results are published.
'''

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.new() + datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    '''
     doesn’t create any questions, but checks the message:
     “No polls are available.”
     and verifies the latest_question_list is empty.
     Note that the django.test.TestCase class provides
     some additional assertion methods. In these examples,
     we use assertContains() and assertQuerysetEqual().
    '''
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_ques_list'],[])

    '''
    we create a question and verify that it appears in the list.
    '''
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_ques_list'],
            ['<Question: Past Question.>']
        )

        '''
        we create a question with a pub_date in the future.
        The database is reset for each test method, so the first
        question is no longer there, and so again the index shouldn’t
        have any questions in it.
        '''

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future Question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['latest_ques_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past Question", days=-30)
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_ques_list'],
            ['<Question: Past Question.>']
        )
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past Question 1.", days=-30)
        create_question(question_text="Past Question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_ques_list'],
            ['<Question: Past Question 2.>', '<Question: Past Question 1>']

        )
class QuestionDetailVIewTests(TestCase):
    def test_future_question(self):
        """
        detail view of a ques with a pub_date in the future returns a
        404.
        """
        future_question = create_question(question_text="Future Question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        detail view of a ques with pub date in the past displays the questions txt
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

'''
SimpleTestCase.assertContains(
                                response,
                                text,
                                count=None,
                                status_code=200,
                                msg_prefix='',
                                html=False,
                            )[source]

Asserts that a Response instance produced the given status_code and that text
appears in the content of the response. If count is provided, text must occur
exactly count times in the response.

Set html to True to handle text as HTML. The comparison with the response
content will be based on HTML semantics instead of character-by-character
equality. Whitespace is ignored in most cases, attribute ordering is not
significant. See assertHTMLEqual() for more details.

TransactionTestCase.assertQuerysetEqual(
                                            qs,
                                            values,
                                            transform=repr,
                                            ordered=True,
                                            msg=None
                                        )[source]

Asserts that a queryset qs returns a particular list of values values.

The comparison of the contents of qs and values is performed using the
function transform; by default, this means that the repr() of each value
is compared. Any other callable can be used if repr() doesn’t provide a
unique or helpful comparison.

By default, the comparison is also ordering dependent. If qs doesn’t
provide an implicit ordering, you can set the ordered parameter to False,
which turns the comparison into a collections.Counter comparison.
If the order is undefined (if the given qs isn’t ordered and the comparison
is against more than one ordered values), a ValueError is raised.

Output in case of error can be customized with the msg argument.
'''
