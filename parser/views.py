from django.shortcuts import render
from django.http import HttpResponse
import re
from collections import Counter


def index(request):
    return render(request, 'parser/index.html')


def upload(request):
    if request.method == 'POST':
        log_file = request.FILES['log_file']
        log_data = log_file.read().decode('utf-8')
        request.session['log_lines'] = log_data
        return render(request, 'parser/upload.html', {'log_data': log_data})
    return HttpResponse('Error: No log file provided.')


def analyze(request):
    log_data = request.session.get('log_data', '')
    if log_data:
        ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_data)
        errors = re.findall(r'ERROR: (.+)', log_data)
        ip_count = Counter(ip_addresses).most_common(5)
        error_count = Counter(errors).most_common(5)

        context = {
            'ip_count': ip_count,
            'error_count': error_count
        }
        return render(request, 'parser/results.html', context)
    return HttpResponse('Error: No log data found.')



