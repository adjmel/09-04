# Importations nécessaires
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import CustomUserCreationForm  # Importation du formulaire personnalisé
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Vue pour la page d'accueil
def home(request):
    return render(request, 'home.html')

# Vue pour la page d'inscription
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Vue pour la page de connexion
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('enable_2fa')  # Rediriger vers la page de 2Fa avant la page d'accueil après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vue pour la modification de mot de passe
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Garder l'utilisateur connecté
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password/change_password.html', {'form': form})

# Vue pour la confirmation de modification de mot de passe
def password_change_done(request):
    return render(request, 'change-password/password_change_done.html')

# Create a view that allows users to enable 2FA for their accounts. 
# You can use Django’s class-based views for this purpose. 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import Enable2FAForm

@login_required
def enable_2fa(request):
    if request.method == 'POST':
        form = Enable2FAForm(request.user, request.POST)
        if form.is_valid():
            # Enable 2FA for the user
            device = TOTPDevice.objects.create(user=request.user)
            device.save()
            return redirect('verify_2fa')
    else:
        form = Enable2FAForm(request.user)

    return render(request, 'enable_2fa.html', {'form': form})

#Create a view for verifying 2FA during the login process. 
# This view will prompt users to enter the 2FA code generated 
# by their authentication app.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
# from django_otp.plugins.otp_totp.views import TOTPVerificationView

@login_required
def verify_2fa(request):
    if request.method == 'POST':
        # Handle the 2FA verification form submission
        return redirect('success_page') #TOTPVerificationView.as_view()(request)

    devices = TOTPDevice.objects.filter(user=request.user)
    return render(request, 'verify_2fa.html', {'devices': devices})

from django.shortcuts import render

def success_page(request):
    # Logique de la vue pour la page de succès
    return render(request, 'success_page.html')


#To make use of 2FA, you need to update your user authentication 
# views, such as the login view. Here’s an example of how you can 
# modify the login view to incorporate 2FA verification
from django.contrib.auth.views import LoginView
from django_otp.plugins.otp_totp.models import TOTPDevice

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Check if the user has 2FA enabled
        user = self.request.user
        if TOTPDevice.objects.filter(user=user).count() > 0:
            # Redirect to the 2FA verification view
            return redirect('verify_2fa')

        # Continue with regular login
        return super().form_valid(form)

import pyotp
import qrcode
from io import BytesIO
from django.shortcuts import render

def generate_qr_code(request):
    # Générer une clé secrète pour Google Authenticator
    secret_key = pyotp.random_base32()

    # Créer une instance de pyotp.TOTP avec la clé secrète
    totp = pyotp.TOTP(secret_key)

    # Générer l'URL du code QR avec l'identifiant de l'utilisateur et la clé secrète
    qr_code_url = totp.provisioning_uri(request.user.username, issuer_name='myapp')

    # Créer le code QR avec qrcode
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_code_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convertir l'image en bytes pour l'affichage dans le modèle HTML
    buffer = BytesIO()
    qr_img.save(buffer)
    qr_img_bytes = buffer.getvalue()

    return render(request, 'qr_code.html', {'qr_code_img': qr_img_bytes})


##########################


# import qrcode
# from django.shortcuts import render
# from django_otp.plugins.otp_totp.models import TOTPDevice

# def generate_qr_code(request):
#     # Récupérer l'utilisateur connecté
#     user = request.user

#     # Vérifier si l'utilisateur a une clé TOTP configurée
#     try:
#         device = TOTPDevice.objects.get(user=user)
#         qr_code_url = device.config_url
#         qr_code_img = generate_qr_code_image(qr_code_url)
#         return render(request, 'qr_code.html', {'qr_code_img': qr_code_img})
#     except TOTPDevice.DoesNotExist:
#         # Gérer le cas où l'utilisateur n'a pas de clé TOTP configurée
#         return render(request, 'no_totp.html')

# def generate_qr_code_image(data):
#     # Créer un objet QRCode
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )

#     # Ajouter les données (URL de configuration) au QRCode
#     qr.add_data(data)
#     qr.make(fit=True)

#     # Créer une image PIL (Pillow) à partir du QRCode
#     img = qr.make_image(fill_color="black", back_color="white")
#     return img


# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect

# def custom_login(request):
#     # Vérifier si les informations d'identification de l'utilisateur sont valides
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Générer le QR code pour l'utilisateur s'il a activé 2FA
#         if TOTPDevice.objects.filter(user=user).exists():
#             # Générez le QR code ici
#             qr_code_url = generate_qr_code(user)
#             return render(request, 'login_with_qr.html', {'qr_code_url': qr_code_url})
#         else:
#             return redirect('home')  # Rediriger vers la page d'accueil si l'utilisateur n'a pas activé 2FA
#     # else:
#     #     # Rediriger vers une page d'erreur si les informations d'identification sont incorrectes
#     #     return render(request, 'login_error.html')


########################################