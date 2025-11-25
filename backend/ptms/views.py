from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from .models import Project, Task
from .serializers import (
    ProjectSerializer, ProjectSimpleSerializer,
    TaskSerializer, UserSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for projects in PTMS
    """
    queryset = Project.objects.all().prefetch_related('tasks')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectSimpleSerializer
        return ProjectSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active projects"""
        projects = Project.objects.filter(status='active').prefetch_related('tasks')
        serializer = ProjectSimpleSerializer(projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get projects filtered by status"""
        status_filter = request.query_params.get('status')
        if status_filter:
            projects = Project.objects.filter(status=status_filter).prefetch_related('tasks')
        else:
            projects = Project.objects.all().prefetch_related('tasks')
        serializer = ProjectSimpleSerializer(projects, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tasks in PTMS
    """
    queryset = Task.objects.all().select_related('project', 'assigned_to')
    serializer_class = TaskSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'project__name']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_project(self, request):
        """Get all tasks for a specific project"""
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response(
                {'error': 'project_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = Task.objects.filter(project_id=project_id).select_related('project', 'assigned_to')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get tasks filtered by status"""
        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = Task.objects.filter(status=status_filter).select_related('project', 'assigned_to')
        else:
            tasks = Task.objects.all().select_related('project', 'assigned_to')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        """Get tasks filtered by priority"""
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            tasks = Task.objects.filter(priority=priority_filter).select_related('project', 'assigned_to')
        else:
            tasks = Task.objects.all().select_related('project', 'assigned_to')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def assigned_to_me(self, request):
        """Get tasks assigned to the current user"""
        tasks = Task.objects.filter(assigned_to=request.user).select_related('project', 'assigned_to')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
