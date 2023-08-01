from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
__all__ = [
    'Quiz', 'QuizQuestion', 'QuizAnswer', 'UserResult'
]

User = get_user_model()


class Quiz(models.Model):
    """
    Тест

    Attributes:
        name(models.CharField): название теста
    """

    name = models.CharField(max_length=255, verbose_name='Название теста')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    """
    Вопрос в тесте

    Attributes:
        quiz (models.ForeignKey): тест в котором находится вопрос
        order (models.IntegerField): порядок появления вопроса в тесте
        multiple (models.BooleanField): присутствует ли возможность выбрать нескольки вариантов ответов
        text (models.TextField): текст вопроса
    """

    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    order = models.IntegerField()
    multiple = models.BooleanField(verbose_name='Более одного ответа?')
    text = models.TextField(verbose_name='Текст вопроса')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuizAnswer(models.Model):
    """
    Ответ на вопрос в тесте

    Attributes:
        text (models.CharField): текст ответа
        question (models.ForeignKey): тест в котором находится вопрос
        correct (models.ForeignKey): является ли ответ верным
    """
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    question = models.ForeignKey(QuizQuestion, related_name='answers', on_delete=models.CASCADE)
    correct = models.BooleanField()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


# Так как в приложении присутствует функционал изменения тестов, то для сохранения результатов на пройденную версию
# теста будем хранить результат, как артефакт не привязываясь к моделям вопросов и ответов
class UserResult(models.Model):
    """
    Тест

    Attributes:
        user(models.ForeignKey): пользователь прошедший тест
        quiz(models.ForeignKey): тест
    """
    user = models.ForeignKey(User, related_name='user_results', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='quiz_results', on_delete=models.CASCADE)
    num_of_answers = models.IntegerField()
    num_of_correct_answers = models.IntegerField()

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


