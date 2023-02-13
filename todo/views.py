from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status


from django.shortcuts import get_object_or_404

from .pagination import StandardResultsSetPagination
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ('title', 'body')
    ordering = ('created_at',)
    ordering_fields = ('title', 'id')


class TodoViewSetCustom(GenericViewSet):
    queryset = Todo.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'title', 'body']


    def list(self, request):
        queryset = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


    def get_serializer_class(self):
        return TodoSerializer
    

    def retrieve(self, request, pk=None):
        todo = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        if isinstance(request.data, list):
            serializer = TodoSerializer(data=request.data, many=True)
        else:
            serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        todo = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoSerializer(instance=todo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def partial_update(self, request, pk=None):
        todo = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoSerializer(instance=todo, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        todo = get_object_or_404(self.queryset, pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

