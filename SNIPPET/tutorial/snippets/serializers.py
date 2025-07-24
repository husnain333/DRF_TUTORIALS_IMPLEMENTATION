from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, Project, User
from rest_framework.validators import UniqueTogetherValidator


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     title  = serializers.CharField(required = False, allow_blank = True, max_length = 100)
#     code = serializers.CharField(style = {'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required = False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default = 'python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default = 'friendly')

#     def create(self, validated_data):

#         return Snippet.objects.create(**validated_data)
    

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title',instance.title)
#         instance.code = validated_data.get('code',instance.code)
#         instance.linenos = validated_data.get('linenos',instance.linenos)
#         instance.language = validated_data.get('language',instance.language)
#         instance.style = validated_data.get('style',instance.style)
#         instance.save()
#         return instance
#     # Field Level Validation
#     def validate_title(value):
#         if not value:
#             raise serializers.ValidationError("Title cannot be empty")
#         return value
    
#     # Object Level Validation
#     def validate(self, attrs):
#         if attrs['language'] == 'java' and not attrs['code'].startswith('public class'):
#             raise serializers.ValidationError("Java code must start with 'public class'")
#         return attrs
    
#     # custom validation method for a specific field
#     def validate_code(self, value):
#         if 'print' not in value:
#             raise serializers.ValidationError("Code must contain a print statement")
#         return value

# class SnippetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Snippet
#         exclude = ['created']


# class SnippetSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only = True)
#     title  = serializers.CharField(required = False, allow_blank = True, max_length = 100)
#     code = serializers.CharField(style = {'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required = False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default = 'python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default = 'friendly')
#     class Meta:
#         model = Snippet
#         fields = '__all__'
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Snippet.objects.all(),
#                 fields=('title', 'language')
#             )
#         ]
    
#     def create(self, validated_data):
#         return Snippet.objects.create(created=validated_data.get('created', None),
#                                       title=validated_data.get('title', ''),
#                                       code=validated_data.get('code', ''),
#                                       linenos=validated_data.get('linenos', False),
#                                       language=validated_data.get('language', 'python'),
#                                       style=validated_data.get('style', 'friendly'))
    
    

# class projectSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=500, allow_blank=True, required=False)
#     created_at = serializers.DateTimeField()
#     updated_at = serializers.DateTimeField()
#     Snippets = SnippetSerializer(many=True)
#     class Meta:
#         fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'Snippets']
#     def create(self, validated_data):
#         snippets_data = validated_data.pop('Snippets')
#         project = Project.objects.create(**validated_data)
#         for snippet_data in snippets_data:
#             Snippet.objects.create(project=project, **snippet_data)
#         return project
#     def update(self, instance, validated_data):
#         snippets_data = validated_data.pop('snippets')
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()

#         instance.snippets.all().delete()
#         for snippet_data in snippets_data:
#             Snippet.objects.create(project=instance, **snippet_data)

#         return instance
    
#     def validate_title(self, value):
#         if not value:
#             raise serializers.ValidationError("Title cannot be empty")
#         return value
    
#     def validate_discription(self, value):
#         if len(value) > 500:
#             raise serializers.ValidationError("Description cannot exceed 500 characters")
#         return value
#     def validate_updated_at(self, value):
#         if value < self.instance.created_at:
#             raise serializers.ValidationError("Updated at cannot be before created at")
#         return value

class UserSerializer(serializers.HyperlinkedIdentityField):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    checkRejex = serializers.RegexField(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
    slug = serializers.SlugField(max_length=100)
    url = serializers.URLField(max_length=200, allow_blank=True, required=False)
    UUID = serializers.UUIDField()
    file_path = serializers.FilePathField(path="/path/to/files", match=".*\.txt$", recursive=True)
    ipadress = serializers.IPAddressField(protocol='both')
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_joined = serializers.DateTimeField()
    float1 = serializers.FloatField(default=0.0)
    slarayDate = serializers.DateField()
    timestarted = serializers.TimeField()
    shift_duration = serializers.DurationField(default='00:00:00')
    resume = serializers.FileField()
    pic = serializers.ImageField()

    class Meta:
        model = User
        fields = ['url','id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']

        )
        return user

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']

class customerserializer(UserDetailSerializer):
    class Meta(UserDetailSerializer.Meta):
        fields = UserDetailSerializer.Meta.fields + ['password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

class ProjectSerializer(serializers.ModelSerializer):
    snippets = serializers.SlugRelatedField(
        slug_field='title',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

