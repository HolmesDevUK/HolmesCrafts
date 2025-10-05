from django.contrib import messages

def alert_success(request, message):
    messages.success(request, message)

def alert_error(request, message):
    messages.error(request, message)

def alert_info(request, message):
    messages.info(request, message)

def alert_warning(request, message):
    messages.warning(request, message)

def alert_debug(request, message):
    messages.debug(request, message)
