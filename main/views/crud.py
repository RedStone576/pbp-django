from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .utils import GLOBAL_CONTEXT, get_model_form


@login_required(login_url="/super/login/")
def form_view(request, item_type):
    _pk = request.GET.get("id")

    if _pk:
        # ni kalo editing
        if not (request.user.is_superuser or request.user.groups.filter(name="Editor").exists()):
            raise PermissionDenied
    else:
        # and this one create object baru anjayyyy
        if not request.user.is_superuser:
            raise PermissionDenied

    Model, FormClass = get_model_form(item_type)

    instance = None

    if _pk:
        instance = get_object_or_404(Model, id=_pk)
    ##

    form = FormClass(request.POST or None, instance=instance)

    title = f"Edit {item_type}" if instance else f"Add {item_type}"
    redir_name = f"show_{item_type}"

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{item_type.capitalize()} added successfully!")
        return redirect(f"main:{redir_name}")

    return render(request, "base_create.html", GLOBAL_CONTEXT(request) | {
        "form": form,
        "title": title
    }) # i will fix the redirect later zzz

# akan ada waktunya manusia akan sadar bahwa semuanya eventually jadi POST request xixixixi
@login_required(login_url="/super/login/")
def delete_item(request, item_type):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method != "POST":
        return redirect(f"main:show_{item_type}")

    Model, _ = get_model_form(item_type)
    _pk = request.GET.get("id")

    if not _pk:
        return redirect(f"main:show_{item_type}")

    obj = get_object_or_404(Model, id=_pk)
    obj.delete()

    messages.success(request, f"{item_type.capitalize()} deleted successfully!")

    return redirect(f"main:show_{item_type}")
