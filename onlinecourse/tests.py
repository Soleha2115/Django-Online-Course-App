from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from onlinecourse.models import Choice, Course, Enrollment, Question, Submission


class ExamWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='learner', password='test-pass-123')
        self.course = Course.objects.create(name='Django', description='Learn Django')
        self.question = Question.objects.create(course=self.course, question_text='Select Django', grade=10)
        self.correct = Choice.objects.create(question=self.question, choice_text='Django', is_correct=True)
        self.wrong = Choice.objects.create(question=self.question, choice_text='Flask', is_correct=False)
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course)

    def test_exact_correct_choices_pass(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('onlinecourse:submit', args=[self.course.pk]),
            {f'choice{self.question.pk}': [str(self.correct.pk)]},
        )
        submission = Submission.objects.get(enrollment=self.enrollment)
        self.assertRedirects(
            response,
            reverse('onlinecourse:show_exam_result', args=[self.course.pk, submission.pk]),
        )
        result = self.client.get(
            reverse('onlinecourse:show_exam_result', args=[self.course.pk, submission.pk])
        )
        self.assertContains(result, 'Congratulations! You passed.')
        self.assertContains(result, '10 / 10')

    def test_wrong_choice_does_not_pass(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('onlinecourse:submit', args=[self.course.pk]),
            {f'choice{self.question.pk}': [str(self.wrong.pk)]},
        )
        submission = Submission.objects.get(enrollment=self.enrollment)
        result = self.client.get(
            reverse('onlinecourse:show_exam_result', args=[self.course.pk, submission.pk])
        )
        self.assertContains(result, 'You did not pass.')
        self.assertContains(result, '0 / 10')

    def test_cannot_submit_for_another_users_enrollment(self):
        other_user = get_user_model().objects.create_user(username='other', password='test-pass-123')
        self.client.force_login(other_user)
        response = self.client.post(
            reverse('onlinecourse:submit', args=[self.course.pk]),
            {f'choice{self.question.pk}': [str(self.correct.pk)]},
        )
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Submission.objects.exists())

    def test_choice_from_another_course_is_rejected(self):
        other_course = Course.objects.create(name='Other', description='Another course')
        other_question = Question.objects.create(course=other_course, question_text='Other question')
        foreign_choice = Choice.objects.create(question=other_question, choice_text='Foreign')
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('onlinecourse:submit', args=[self.course.pk]),
            {f'choice{self.question.pk}': [str(foreign_choice.pk)]},
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Submission.objects.exists())