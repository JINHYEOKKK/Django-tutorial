from django import forms


class QuestionCreateForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)


# class QuestionUpdateForm(forms.Form):
#     your_name = forms.CharField(label="Your name", max_length=100)