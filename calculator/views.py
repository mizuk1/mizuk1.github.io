from django.shortcuts import render
from .item_parser import parse_item_modifiers
from .dps_calculator import calculate_weapon_dps

# Create your views here.
def dps_view(request):
    context = {}
    if request.method == "POST":
        item_text = request.POST.get("item_text", "")
        try:
            parsed = parse_item_modifiers(item_text)
            dps = calculate_weapon_dps(parsed)
            context["dps"] = dps
        except Exception as e:
            context["dps"] = {"min_dps": "Erro", "max_dps": "Erro", "avg_dps": str(e)}
    return render(request, "calculator/dps_form.html", context)