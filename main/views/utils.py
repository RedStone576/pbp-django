from main.forms import EducationForm, ExperienceForm, ProjectForm
from main.models import Education, Experience, Project


def GLOBAL_CONTEXT(request):
    return {
        "name": "Ilham Firmansyah",
        "npm": "2506532643",
        "study_program": "Sistem Informasi",
        "study_program_kd": "06.00.12.01",
        "role": "Insinyur Perangkat Lunak",

        "is_editor": request.user.is_authenticated and request.user.groups.filter(name="Editor").exists(),
        "is_superuser": request.user.is_superuser,
        "last_login": request.COOKIES.get("last_login", "No active login session / Cookie not found")
    }

###

MODELS = {
    "experience": (Experience, ExperienceForm),
    "education": (Education, EducationForm),
    "projects": (Project, ProjectForm),
}

def get_model_form(item_type):
    model, form = MODELS[item_type]
    return model, form
