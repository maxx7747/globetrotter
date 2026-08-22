from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import ForgotPasswordSerializer, LoginSerializer, RegisterSerializer, UserSerializer
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ — body: { email, password }"""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer


class RefreshView(TokenRefreshView):
    """POST /api/auth/refresh/"""

    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    """GET /api/auth/me/"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ForgotPasswordView(APIView):
    """
    POST /api/auth/forgot-password/ — matches ForgotPassword.tsx.
    Always returns 200 regardless of whether the email exists, to avoid
    leaking account existence — the frontend already messages it this way.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        User = get_user_model()
        user = User.objects.filter(email__iexact=email).first()
        if user is not None:
            # TODO: swap this for a real reset-token + reset-confirm flow
            # (e.g. django-rest-passwordreset) before going to production.
            send_mail(
                subject="Reset your GlobalTrotters password",
                message="A password reset was requested for this account.",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )

        return Response({"detail": "If an account exists for that email, a reset link has been sent."})


from rest_framework import generics
from django.db.models import Q

class UserProfileView(APIView):
    # Endpoint for /api/users/me/
    def patch(self, request):
        user = request.user
        if not user.is_authenticated:
            user = get_user_model().objects.first() # Mock auth fallback
            
        # Update logic based on custom user model fields
        if 'fullName' in request.data:
            user.first_name = request.data['fullName'] # Adjust to match your model
        if 'email' in request.data:
            user.email = request.data['email']
        user.save()
        
        return Response({
            "id": user.id,
            "fullName": user.first_name,
            "email": user.email
        })

class UserSearchView(APIView):
    # Endpoint for /api/users/search/
    def get(self, request):
        query = request.query_params.get('q', '')
        User = get_user_model()
        users = User.objects.filter(email__icontains=query)[:10]
        
        data = [{"id": u.id, "fullName": u.first_name, "email": u.email} for u in users]
        return Response(data)