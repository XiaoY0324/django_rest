# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             # serializer.data 数据创建成功后所有数据
#             return JsonResponse(serializer.data, status=201)
#         # serializer.errors 错误信息
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)


# 使用rest 框架包装的api视图<@api_view装饰器(基于方法的视图) 和 APIView类(基于类的视图)>

# ------------------ @api_view装饰器 ------------------------
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """
#     列出所有的snippets，或者创建一个新的snippet。
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """
#     获取，更新或删除一个snippet实例。
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# 其实，与其使用基于方法（function based）的视图，我们更加倾向使用基于类（class based）的视图。接下来，你将看到这是一个强大的模式，是我们能够重用公共的功能，并且，帮我们保持代码DRY。
# ------------------ APIView类 ------------------------ 把每个请求方式分成一个单独的方法来处理
# 使用基于类视图的最大优势之一是它可以轻松地创建可复用的行为。
#
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# class SnippetList(APIView):
#     # APIView实际继承django总的View
#     # from django.views.generic import View
#     """
#     # 这里是SnippetList接口描述
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         # manay=True 用于querySet对象
#         serializer = SnippetSerializer(snippets, many=True)
#         # 3 Respone比django的response更强大
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             # .save()是调用SnippetSerializer中的create()方法
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SnippetDetail(APIView):
#     """
#     读取, 更新 or 删除一个代码片段(snippet)实例(instance).
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# 使用基于类视图的最大优势之一是它可以轻松地创建可复用的行为。
# 到目前为止，我们使用的创建/获取/更新/删除操作和我们创建的任何基于模型的API视图非常相似。这些常见的行为是在REST框架的mixin类中实现的。
# 那么 接着改..

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics
#
#
# class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     # mixins.CreateModelMixin 可以保存数据
#     # generics.GenericAPIView 继承了APIView
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         # self.list是ListModelMixin的list函数
#         # 功能是过滤、分页、调用serializer,将数据序列化
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         # 检索一个模型实例 RetrieveModelMixin.retrieve
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         # 更新一个模型实例 UpdateModelMixin.update
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         # 删除一个模型实例 DestroyModelMixin.destroy
#         return self.destroy(request, *args, **kwargs)


# 使用通用的基于类的视图
#
# 通过使用mixin类，我们使用更少的代码重写了这些视图，但我们还可以再进一步。REST框架提供了一组已经混合好（mixed-in）的通用视图，我们可以使用它来简化我们的views.py模块。
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions # 权限验证
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) # 判断是有读写权限的用户或者只能读取的用户

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) # 存储代码创建用户的信息


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET']) # 为我们的api创建一个根路径
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView): # 创建代码高亮视图
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)