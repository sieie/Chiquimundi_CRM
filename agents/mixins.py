from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganisorAndLoginRequiredMixin(AccessMixin):
    #Verifica que el usuario actual está autenticado y es un organizador
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organisor or not request.user.is_authenticated:
            return redirect("leads:lista")
        return super().dispatch(request, *args, **kwargs)