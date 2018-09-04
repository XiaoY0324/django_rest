from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

# class SnippetSerializer(serializers.Serializer): # serializers提供序列化或反序列化json等方法
#     # 每一个表都可以建一个serializer，类似Django的Form  专门用于json
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#          根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         根据提供的验证过的数据更新和返回一个已经存在的`Snippet`实例。
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

# 使用 ModelSerializer 改下之上方法         -----------------------
# class SnippetSerializer(serializers.ModelSerializer):
#     # ModelSerializer和Django中ModelForm功能相似
#     # Serializer和Django中Form功能相似
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = Snippet
#         fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')
#
# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all()) # 反向关联'snippets'实例对象
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'snippets')

# 超链接我们的api -> 改下              ------------------------
# {
#     "url": "http://localhost:8010/snippets/3/",
#     "id": 3,
#     "highlight": "http://localhost:8010/snippets/3/highlight/",
#     "owner": "zj",
#     "title": "hello",
#     "code": "print(\"123\")\n",
#     "linenos": false,
#     "language": "python",
#     "style": "friendly"
# }


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
