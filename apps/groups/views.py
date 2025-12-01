from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer
from django.shortcuts import get_object_or_404


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by("-created_at")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class JoinGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        # if already member -> return 200
        member, created = GroupMember.objects.get_or_create(
            group=group, user=request.user
        )
        if created:
            member.role = "member"
            member.save()
            return Response({"detail": "joined"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "already a member"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        try:
            membership = GroupMember.objects.get(group=group, user=request.user)
            membership.delete()
            return Response({"detail": "left group"}, status=status.HTTP_204_NO_CONTENT)
        except GroupMember.DoesNotExist:
            return Response(
                {"detail": "not a member"}, status=status.HTTP_400_BAD_REQUEST
            )


class GroupMembersListView(generics.ListAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs["pk"]
        return GroupMember.objects.filter(group__id=group_id)
