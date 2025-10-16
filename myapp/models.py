from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=True, null=True, default="new user")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.png')

     # 🆕 Add streak tracking fields
    daily_streak = models.IntegerField(default=0)
    last_quiz_date = models.DateField(blank=True, null=True)

    def update_streak(self):
        """Updates daily streak when a user completes a quiz."""
        today = timezone.now().date()

        if self.last_quiz_date == today:
            return  # already played today

        elif self.last_quiz_date == today - timedelta(days=1):
            self.daily_streak += 1  # continue streak
        else:
            self.daily_streak = 1  # reset streak

        self.last_quiz_date = today
        self.save()

    def __str__(self):
        return self.user.username
    

    
class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    questions = models.JSONField(default=list)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaderboard_entries")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="leaderboard")
    score = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="bi bi-book")  # Bootstrap icon

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile for every new user
        Profile.objects.create(user=instance)
    else:
        # Save existing profile when user is updated
        instance.profile.save()
