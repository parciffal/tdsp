from django.shortcuts import render
from ...tools.bid_tools import Analyzer

def bid_analyzer_view(request):
    aggressive = request.POST.get('aggressive', 'False') == 'True'
    Analyzer().set_aggr(aggressive=aggressive)
    return render(request, 'admin/bid_analyzer.html', {'aggressive': aggressive})
