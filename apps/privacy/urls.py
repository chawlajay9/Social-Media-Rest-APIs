from django.urls import path
from .views import PrivacySettingView

urlpatterns = [
    path("privacy/", PrivacySettingView.as_view(), name="privacy-setting"),
]
