from django.forms import DateTimeInput, ModelForm, Select, Textarea, TextInput, URLInput
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

from main.models import Education, Experience, Project

def strip_html_tags(*fields_to_strip):
    def decorator(cls):
        original_clean = cls.clean

        # mabar mas https://docs.djangoproject.com/en/5.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
        def clean(self):
            cleaned_data = original_clean(self)

            if cleaned_data is None:
                cleaned_data = self.cleaned_data

            for field in fields_to_strip:
                value = cleaned_data.get(field)
                
                if isinstance(value, str):
                    stripped = strip_tags(value).strip()
                
                    if not stripped:
                        # https://docs.djangoproject.com/en/5.0/ref/forms/api/#django.forms.Form.add_error
                        self.add_error(field, ValidationError(f"{self.fields[field].label} can't contain only HTML tags."))
                    else:
                        cleaned_data[field] = stripped
            
            return cleaned_data

        cls.clean = clean
        
        return cls
    return decorator


@strip_html_tags("title", "description")
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "started_at", "ended_at"]

        labels = {
            "title": "Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
            "started_at": "Start date",
            "ended_at": "End date",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Software Engineer", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Describe here", "rows": 3}),
            "category": Select(),
            "thumbnail": URLInput(attrs={"placeholder": "https://..."}),
            "started_at": DateTimeInput(attrs={"type": "datetime-local"}),
            "ended_at": DateTimeInput(attrs={"type": "datetime-local"}),
        }


@strip_html_tags("institution", "program", "field")
class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["institution", "program", "field", "started_at"]

        labels = {
            "institution": "Institution",
            "program": "Program",
            "field": "Field of study",
            "started_at": "Start date",
        }

        widgets = {
            "institution": TextInput(attrs={"placeholder": "Universitas Indonesia", "maxlength": 255}),
            "program": TextInput(attrs={"placeholder": "Bachelor of Computer Science", "maxlength": 255}),
            "field": TextInput(attrs={"placeholder": "Computer Science", "maxlength": 255}),
            "started_at": DateTimeInput(attrs={"type": "datetime-local"}),
        }


@strip_html_tags("title", "description")
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "link", "created_at"]

        labels = {
            "title": "Project Name",
            "description": "Description",
            "link": "Project URL",
            "created_at": "Created date",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Describe here", "rows": 3}),
            "link": URLInput(attrs={"placeholder": "https://github.com/redstone576"}),
            "created_at": DateTimeInput(attrs={"type": "datetime-local"}),
        }
