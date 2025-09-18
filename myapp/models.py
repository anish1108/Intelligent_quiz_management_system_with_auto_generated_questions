from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=True, null=True, default="new user")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.png')

    def __str__(self):
        return self.user.username
    

    
class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class QuizAttempt(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
#     score = models.IntegerField(default=0)
#     started_at = models.DateTimeField(auto_now_add=True)
#     completed_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.quiz.title} - {self.score}"


# class Leaderboard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaderboard_entries")
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="leaderboard")
#     score = models.IntegerField()
#     achieved_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-score']

#     def __str__(self):
#         return f"{self.user.username} - {self.quiz.title} ({self.score})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile for every new user
        Profile.objects.create(user=instance)
    else:
        # Save existing profile when user is updated
        instance.profile.save()
