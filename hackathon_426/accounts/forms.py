from django import forms
from .models import newSubmission

class LoginForm(forms.ModelForm): 
    class Meta:
        model = newSubmission
        fields = ["username", "password", "email", "confirm_password"]
        widgets = {
            'password': forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        }
    
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        required=False
    )

    email = forms.EmailField(
        label="Email",
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.create_mode = kwargs.pop('create_mode', False)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        email = cleaned_data.get("email")
        confirm_password = cleaned_data.get("confirm_password")
        if self.create_mode:
            if newSubmission.objects.filter(username=username).exists():
                self.add_error("username", "Username already exists.")
            if newSubmission.objects.filter(email=email).exists():
                self.add_error("email", "Email already exists.")
            if password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match.")
        if self.create_mode and not username or not password:
            raise forms.ValidationError("Username and password are required.")

class ResetPasswordForm(forms.ModelForm): 
    class Meta:
        model = newSubmission
        fields = ["email", "verification_code"]
        widgets = {
            'verification_code': forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("verification_code"):
            if len(cleaned_data["verification_code"]) != 6:
                self.add_error("verification_code", "Verification code must be 6 digits.")

class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = newSubmission
        fields = ["name", "major", "gender", "race", "sports"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = newSubmission
        fields = ['profile_picture', 'bio']
        widgets = {
            'profile_picture': forms.FileInput(),
        }

        