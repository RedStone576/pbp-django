from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput

from main.models import Experience, Education, Project


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
