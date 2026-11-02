from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .models import Choice, Course, Enrollment, Submission


class CourseListView(ListView):
    model = Course
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'
    ordering = ('-pub_date',)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled'] = self.request.user.is_authenticated and Enrollment.objects.filter(
            user=self.request.user, course=self.object
        ).exists()
        return context


@login_required
def enroll(request, course_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('onlinecourse:course_details', pk=course.pk)


@login_required
def submit(request, course_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    choices_by_question = {}
    for question in course.question_set.all():
        selected_ids = request.POST.getlist(f'choice{question.pk}')
        if selected_ids:
            choices_by_question[question.pk] = selected_ids

    valid_choices = Choice.objects.filter(
        question__course=course,
        question_id__in=choices_by_question,
        pk__in=[choice_id for ids in choices_by_question.values() for choice_id in ids],
    )
    valid_by_question = {}
    for choice in valid_choices:
        valid_by_question.setdefault(choice.question_id, set()).add(str(choice.pk))
    if any(set(ids) != valid_by_question.get(question_id, set())
           for question_id, ids in choices_by_question.items()):
        return render(
            request,
            'onlinecourse/course_detail_bootstrap.html',
            {'course': course, 'enrolled': True, 'invalid_choices': True},
            status=400,
        )

    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(valid_choices)
    return redirect(
        'onlinecourse:show_exam_result',
        course_id=course.pk,
        submission_id=submission.pk,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course,
        enrollment__user=request.user,
    )
    selected_choices = submission.choices.all()
    selected_ids_by_question = {}
    for choice in selected_choices:
        selected_ids_by_question.setdefault(choice.question_id, set()).add(choice.pk)

    questions = course.question_set.prefetch_related('choice_set')
    max_score = sum(question.grade for question in questions)
    grade = sum(
        question.grade
        for question in questions
        if question.is_get_score(selected_ids_by_question.get(question.pk, set()))
    )
    context = {
        'course': course,
        'submission': submission,
        'selected_choices': selected_choices,
        'grade': grade,
        'max_score': max_score,
        'passed': max_score > 0 and grade / max_score >= 0.8,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)