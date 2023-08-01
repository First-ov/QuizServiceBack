from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from quizzes.models import Quiz, QuizQuestion, UserResult

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password",)


class CreateUserView(CreateAPIView):
    model = UserModel
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class CompleteTest(CreateAPIView):
    serializer_class = serializers.Serializer

    def post(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(id=request.data['test'])
        questions = list(quiz.questions.order_by('order'))
        correct = 0
        for i in range(len(questions)):
            if set(request.data['answers']
                   [i]) == set([x.id for x in list(questions[i].answers.filter(correct=True))]):
                correct+=1
        user_result = UserResult.objects.create(
            user=request.user,
            quiz=quiz,
            num_of_answers=len(questions),
            num_of_correct_answers=correct
        )
        return Response('ok', status=status.HTTP_200_OK)



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'text']


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = ['quiz', 'order', 'multiple', 'text', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions']


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['name', 'id']


class QuizListViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResult
        fields = [
            'quiz',
            'num_of_answers',
            'num_of_correct_answers',
        ]


class ResultListViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer

    def get_queryset(self):
        return UserResult.objects.filter(user__id=self.request.user.id)


router = routers.DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quizzes')
router.register(r'quizzeslist', QuizListViewSet, basename='quizzeslist')
router.register(r'results', ResultListViewSet, basename='results')
