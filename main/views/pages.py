import json
import requests

from django.shortcuts import render
from .utils import GLOBAL_CONTEXT

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
    api_url = f"{request.scheme}://{request.get_host()}/api/{item_type}/"
    
    try:
        response = requests.get(api_url, cookies=request.COOKIES, timeout=10)
        response.raise_for_status()
        
        raw_json = response.json()
        
        if isinstance(raw_json, str):
            items = json.loads(raw_json)
        else:
            items = raw_json
        
        from django.utils.dateparse import parse_datetime

        parsed_items = []
        for item in items:
            fields = item["fields"]
            
            if "starred_by" in fields:
                fields["starred_by"] = [x[0] for x in fields["starred_by"]]
                
            for date_field in ["created_at", "started_at", "ended_at"]:
                if fields.get(date_field):
                    fields[date_field] = parse_datetime(fields[date_field])
                    
            parsed_items.append({"id": item["pk"], **fields})
        
    except requests.RequestException as e:
        print(f"Error: {e}")
        parsed_items = []
        
    context = {f"{item_type}_list": parsed_items}
    return render(request, f"{item_type}.html", GLOBAL_CONTEXT(request) | context)
