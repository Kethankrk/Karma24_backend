from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]
    objects = UserManager()


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User, related_name="owned_workspaces")
    members = models.ManyToManyField(User, related_name="joined_workspaces")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    image = models.URLField(
        default="https://img.freepik.com/premium-vector/user-icon_126283-435.jpg?w=740"
    )

    def __str__(self):
        return self.name


class Pages(models.Model):
    PAGE_CHOICES = {"TODO": "todo", "BLANK": "blank"}
    name = models.CharField(max_length=100)
    page_type = models.CharField(max_length=5, choices=PAGE_CHOICES)
    description = models.TextField(blank=True)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="pages"
    )

    def __str__(self):
        return self.name


class Todo(models.Model):
    page = models.ForeignKey(Pages, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    assigned = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_todo"
    )

    def __str__(self):
        return self.title


class Forum(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="forum"
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return self.content


class BlankPage(models.Model):
    page = models.OneToOneField(
        Pages, on_delete=models.CASCADE, related_name="blank_page"
    )
    body = models.TextField()

    def __str__(self):
        return str(self.page)
