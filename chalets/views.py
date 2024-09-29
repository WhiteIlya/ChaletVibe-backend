from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models

from chalets.permissions import IsAdminOrReadOnly
from users.permissions import IsAdminUser
from .models import UserReaction, Chalet
from .serializers import ChaletSerializer, UserReactionSerializer

class ChaletViewSet(viewsets.ModelViewSet):
    """
    Chalets ViewSets
    """
    queryset = Chalet.objects.all()
    serializer_class = ChaletSerializer
    permission_classes = [IsAdminOrReadOnly]

    # An option to cache (@cache_response) data for 15 minutes. Particularly, get list of chalets
    # @cache_response(timeout=60*15)
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return chalets user hasn't voted yet
        """
        user = self.request.user

        voted_chalet_ids = UserReaction.objects.filter(user=user).values_list('chalet_id', flat=True)
        return Chalet.objects.exclude(id__in=voted_chalet_ids)

class UserReactionViewSet(viewsets.ModelViewSet):
    """
    User Reaction Viewsets
    """
    serializer_class = UserReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserReaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        chalet_id = self.request.data.get('chalet')
        liked = self.request.data.get('liked')

        if UserReaction.objects.filter(user=self.request.user, chalet_id=chalet_id).exists():
            return Response({"detail": "You have already voted for this chalet."}, status=status.HTTP_400_BAD_REQUEST)
        
        chalet = Chalet.objects.get(id=chalet_id)
        serializer.save(user=self.request.user, chalet=chalet, liked=liked)

    @action(
        detail=False,
        methods=['post'],
        url_path='undo-last-vote',
        permission_classes=[IsAuthenticated]
    )
    def undo_last_vote(self, request):
        """
        Allows the user to undo their last vote.
        """
        last_vote = UserReaction.objects.filter(user=request.user).order_by('-id').first()
        if last_vote:
            last_vote.delete()
            return Response({"detail": "Last vote undone."}, status=status.HTTP_200_OK)
        return Response({"detail": "No votes to undo."}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        url_path='results',
        permission_classes=[IsAuthenticated]
    )
    def get_results(self, request):
        """
        Accumulate reaction results
        {
            "id": 1,
            "name": "Mountain Chalet",
            "likes": 12,
            "dislikes": 3
        },
        """
        results = Chalet.objects.annotate(
            likes=Count('userreaction', filter=models.Q(userreaction__liked=True)),
            dislikes=Count('userreaction', filter=models.Q(userreaction__liked=False))
        ).values('id', 'name', 'likes', 'dislikes')

        return Response(results)
    

    def get_permissions(self):
        if self.action in ['destroy', 'retrieve']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserReactionViewSet, self).get_permissions()
