from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.user import User
from core.encoder_tokens import decode_user_id


class ActivationAccount(APIView):
    """
    activation account current user
    """

    serializer_class = ""
    permissions_classes = (AllowAny,)
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        """activate current account user"""
        try:
            uid = decode_user_id(self.kwargs.get("uid"))
            token = self.kwargs.get("token")
            user = User.objects.get(id=uid)
            if not user.is_activate and token:
                user.is_activate = True
                user.save()
                return Response({"data": "user activated."}, status=status.HTTP_200_OK)
            return Response({"data": "user is active."}, status=status.HTTP_200_OK)
        except User.DoesNotExist as err:
            return Response({"error": f"{err}"})
