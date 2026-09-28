
from django.shortcuts import render

from .utils import GLOBAL_CONTEXT, get_model_form


def show_main(request):
    # mkay context.name are more like title or something bruh
    context = {
        "bio": (
            "<ul>"
            "<li>Recreational programmer</li>"
            "<li>linguistic enthusiast</li>"
            "<li>supposedly computer philosopher</li>"
            "<li>and Tetris player at heart.</li>"
            "</ul>"
            "Loves raw JavaScript at its finest. TypeScript too, if you insist."
        ),
    }

    return render(request, "index.html", GLOBAL_CONTEXT(request) | context)

###

def show_list(request, item_type):
    bomat, FormClass = get_model_form(item_type)

    context = {
        "title_query": request.GET.get("title", "").strip(),
        "form": FormClass(),
    }

    return render(request, f"{item_type}.html", GLOBAL_CONTEXT(request) | context)
