from django.conf import settings

def cfg_assets_root(request):

    return { 'ASSETS_ROOT' : settings.ASSETS_ROOT }

def cfg_front_root(request):
    
    return { 'FRONT_ROOT' : settings.FRONT_ROOT }