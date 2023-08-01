from django.contrib import admin
import nested_admin
from django.core.exceptions import ValidationError
from .models import Quiz, QuizQuestion, QuizAnswer, UserResult


admin.site.register(UserResult)


class QuizAnswerInline(nested_admin.NestedTabularInline):
    model = QuizAnswer
    extra = 0
    min_num = 2


class QuizQuestionForm(nested_admin.NestedModelAdmin.form):
    def clean(self):
        super().clean()
        if hasattr(self.nested_formsets[0], 'cleaned_data'):
            if len([answer for answer in self.nested_formsets[0].cleaned_data if not answer['DELETE']]) < 2:
                raise ValidationError("Должно быть по крайней мере два ответа на вопрос")
            num_of_correct = len([answer for answer in self.nested_formsets[0].cleaned_data if
                                  answer['correct'] and not answer['DELETE']])
            if num_of_correct == 0:
                raise ValidationError("Не указан правильный ответ")
            if num_of_correct != 1 and not self.cleaned_data['multiple']:
                raise ValidationError("Более одного правильного ответа в вопросе с одним правильным ответом")


class QuizQuestionInline(nested_admin.SortableHiddenMixin, nested_admin.NestedTabularInline):
    model = QuizQuestion
    inlines = [
        QuizAnswerInline,
    ]
    sortable_field_name = 'order'
    extra = 0
    min_num = 1
    form = QuizQuestionForm


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        QuizQuestionInline,
    ]


admin.site.register(Quiz, QuizAdmin)
# Register your models here.
