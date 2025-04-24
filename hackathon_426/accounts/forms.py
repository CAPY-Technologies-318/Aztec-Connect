from django import forms

class LoginForm(forms.Form): 
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("confirm_password"):
            if cleaned_data["password"] != cleaned_data["confirm_password"]:
                self.add_error("confirm_password", "Passwords do not match.")

class PasswordResetForm(forms.Form): 
    email = forms.EmailField(
        max_length=254, 
        error_messages={
            "required": "Email is required.",
            "invalid": "Enter a valid email address."
        }
    )
    verification_code = forms.CharField(
        max_length=6, 
        error_messages={
            "required": "Verification code is required.",
            "invalid": "Enter a valid verification code."
        }
    )

class AccountDetailsForm(forms.Form):
    name = forms.CharField(max_length=100)
    major = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=50)
    race = forms.CharField(max_length=100)
    sports = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
