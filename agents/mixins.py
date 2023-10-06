from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganisorAndLoginRequiredMixin(AccessMixin):
    #Verifica que el usuario actual está autenticado y es un organizador
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("leads:list")
        return super().dispatch(request, *args, **kwargs)