from django.utils.http import is_safe_url


class NextUrlMixin(object):
    default_next = "home"
    def get_next_url(self):
        request = self.request
        redirect_path = request.GET.get('next') or request.POST.get('next_post') or None
        if is_safe_url(redirect_path,request.get_host()):
            return redirect_path
        return self.default_next

class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin,self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
