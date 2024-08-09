from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import APIException
from rest_framework import status, pagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import action

from authors import models, serializers, permissions


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.AuthorSerializer
    pagination_class = pagination.PageNumberPagination

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = User.objects.filter(username=self.request.user.username).select_related('profile')
        return qs

    @action(detail=False, methods=['GET'])
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj,
            context={'request': request},
            *args, **kwargs,
        )
        return Response(serializer.data)
