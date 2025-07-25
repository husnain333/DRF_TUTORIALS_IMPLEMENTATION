from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.core.validators import RegexValidator
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
#    project = models.ForeignKey('Project', related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
#    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
#    highlighted = models.TextField()
    class Meta:
        ordering = ['created']
    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = 'table' if self.linenos else False
    #     options = {'title': self.title} if self.title else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                             full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.language})"
    
    
    

class ProjectManager(models.Manager):
    def create(self,title, description=None):
        project = Project(title=title, description=description)
        project.save()
        snippet = Snippet(created=project.created_at, title=title, code='', linenos=False, language='python', style='friendly')
        snippet.save()
        return project

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ProjectManager()  
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.title

# class User(models.Model):
#     username = models.CharField(unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     checkRejex = RegexValidator(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
#     slug = models.SlugField(max_length=100, unique=True)
#     url = models.URLField(max_length=200, blank=True)
#     UUID = models.UUIDField(unique=True, editable=False)
#     file_path = models.FilePathField(path="/path/to/files", match=".*\.txt$", recursive=True, max_length=100)
#     ipadress = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True, blank=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     float1 = models.FloatField(default=0.0)
#     slarayDate = models.DateField(auto_now=True)
#     timestarted = models.TimeField(auto_now_add=True, null=True, blank=True)
#     shift_duration = models.DurationField(default='00:00:00')
#     resume = models.FileField(upload_to='resumes/', max_length=100, null=True, blank=True)
#     pic = models.ImageField(upload_to='profile_pics/', max_length=100, null=True, blank=True)
    
#     class Meta:
#         ordering = ['username']

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

