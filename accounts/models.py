from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

from PIL import Image

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class AbstractUserProfile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    """Don't create a database for this abstract model."""
    class Meta:
        abstract = True

    def save(self):
        super().save()
        img = Image.open(self.avatar.path) # Locate and open the avatar/image.

        # Resize the image.
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resizes the image.
            img.save(self.avatar.path) # Save the image again and override the 'oversized' image.


class StudentProfile(AbstractUserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

class TeacherProfile(AbstractUserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('44444444$$$$$5555555', created)
    if instance.is_student:
        StudentProfile.objects.get_or_create(user=instance)
    elif instance.is_teacher:
        TeacherProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_student:
        instance.studentprofile.save()
    elif instance.is_teacher:
        instance.teacherprofile.save()