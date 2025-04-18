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