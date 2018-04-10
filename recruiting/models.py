from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from club.models import Club


class InterviewRating(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    got_point = models.IntegerField()
    full_point = models.IntegerField()
    evaluation_text = models.TextField()


class AdminResume(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='지원서 양식 제목',
        max_length=30,
    )
    use_image = models.BooleanField(
        verbose_name='이미지 첨부 여부',
        default=True,
    )
    bottom_msg = models.TextField(
        default="지원해주셔서 감사합니다."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} 동아리의 {1} 지원서 양식'.format(self.club.name, self.title)


class ApplicantResume(models.Model):
    admin_resume = models.ForeignKey(
        AdminResume,
        on_delete=models.CASCADE,
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name='사진 첨부하기',
        upload_to='resume_img/%Y/%m/%d/',
        blank=True,
        null=True,
    )
    interview_rating = models.OneToOneField(
        InterviewRating,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_accepted = models.BooleanField(
        verbose_name='합격 여부',
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} 동아리의 {1} 버전의 지원서 by {2} '.format(
            self.admin_resume.club.name, self.admin_resume.title, self.applicant)

    def image_url(self):
        if self.image:
            image_url = self.image.url
        else:
            image_url = '/static/img/orangered_donkey.png'
        return image_url


class Question(models.Model):
    admin_resume = models.ForeignKey(
        AdminResume,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        verbose_name='질문',
        max_length=100,
    )
    is_short_answer = models.BooleanField(
        verbose_name='단답형 항목 만들기',
        default=False,
    )

    def __str__(self):
        return '{0} 동아리의 {1} 지원서 양식의 질문 "{2}" (단답형 여부 {3})'.format(
            self.admin_resume.club.name, self.admin_resume.title, self.content, self.is_short_answer)


class ShortAnswer(models.Model):
    applicant_resume = models.ForeignKey(
        ApplicantResume,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        verbose_name='내용',
        max_length=50,
    )

    def __str__(self):
        return '{0} 동아리의 {1} 지원서 양식의 항목 "{2}"의 답 by {3}'.format(
            self.question.admin_resume.club.name, self.question.admin_resume.title, self.question.content,
            self.applicant_resume.applicant)


class LongAnswer(models.Model):
    applicant_resume = models.ForeignKey(
        ApplicantResume,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        verbose_name='내용',
    )

    def __str__(self):
        return '{0} 동아리의 {1} 지원서 양식의 질문 "{2}"의 답 by {3}'.format(
            self.question.admin_resume.club.name, self.question.admin_resume.title, self.question.content,
            self.applicant_resume.applicant)