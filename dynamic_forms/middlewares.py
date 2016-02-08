# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.decorators.csrf import csrf_protect

from dynamic_forms.conf import settings
from dynamic_forms.models import FormModel
from dynamic_forms.views import DynamicFormView, DynamicTemplateView


class FormModelMiddleware(object):

    def process_response(self, request, response):
        if response.status_code != 404:
            # Don't check for a form if another request succeeds
            return response
        try:
            path = request.path_info
            form_model = None
            try:
                form_model = FormModel.objects.get(submit_url=path)
                viewfunc = csrf_protect(DynamicFormView.as_view())
            except FormModel.DoesNotExist:
                # success_url is not unique
                form_models = FormModel.objects.filter(success_url=path).all()
                if not form_models:
                    raise Http404
                form_model = form_models[0]
                viewfunc = csrf_protect(DynamicTemplateView.as_view())

            new_resp = viewfunc(request, model=form_model)
            if hasattr(new_resp, 'render') and callable(new_resp.render):
                new_resp.render()
            return new_resp
        except Http404:
            # Return the original response if no form can be found
            return response
        except Exception as exc:
            if settings.DEBUG:
                raise exc
            # Return the original response if any error occurs
            return response
