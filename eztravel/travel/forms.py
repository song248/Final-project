from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField()

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['subject', 'content']