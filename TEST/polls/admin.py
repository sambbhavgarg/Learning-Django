from django.contrib import admin

from .models import Question, Choice

'''
Just one thing to do: we need to tell the admin
that Question objects have an admin interface.
'''
# admin.site.register(Question)
# admin.site.register(Choice)

# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    '''
    Choice objects are edited on the Question admin page.
    By default, provide enough fields for 3 choices
    '''

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['pub_date'] # add a filter by type mentioned
    search_fields = ['question_text'] # search bar
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date Information',    {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    '''
    The first element of each tuple in fieldsets is the title of the fieldset.
    '''
admin.site.register(Question, QuestionAdmin)

'''
This particular change above makes the
“Publication date” come before the “Question” field:
'''
