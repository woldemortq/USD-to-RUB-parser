from django.http import JsonResponse
from .utils import get_usd_to_rub_cbr, load_history

def get_current_usd(request):
    try:
        current = get_usd_to_rub_cbr()
        history = load_history()
        return JsonResponse({
            "current": current,
            "history": history
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
