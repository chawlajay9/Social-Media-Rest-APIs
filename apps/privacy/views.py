from rest_framework import generics, permissions
from .models import PrivacySetting
from .serializers import PrivacySettingSerializer


class PrivacySettingView(generics.RetrieveUpdateAPIView):
    serializer_class = PrivacySettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return PrivacySetting.objects.get(user=self.request.user)
