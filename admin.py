from functools import partial

from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst


class AdminSiteRegroup(AdminSite):
    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a
                for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for app_name, my_models in settings.ADMIN_APPS.items():
            for my_model in my_models:
                for model, model_admin in models.items():
                    if my_model in (
                        capfirst(model._meta.verbose_name_plural),
                        model._meta.object_name,
                    ):
                        app_label = model._meta.app_label

                        has_module_perms = model_admin.has_module_permission(
                            request
                        )
                        if not has_module_perms:
                            continue

                        perms = model_admin.get_model_perms(request)

                        # Check whether user has any perm for this module.
                        # If so, add the module to the model_list.
                        if True not in perms.values():
                            continue

                        info = (app_label, model._meta.model_name)
                        model_dict = {
                            "name": capfirst(model._meta.verbose_name_plural),
                            "object_name": model._meta.object_name,
                            "perms": perms,
                            "admin_url": None,
                            "add_url": None,
                        }
                        if perms.get("change") or perms.get("view"):
                            model_dict["view_only"] = not perms.get("change")
                            try:
                                model_dict["admin_url"] = reverse(
                                    "admin:%s_%s_changelist" % info,
                                    current_app=self.name,
                                )
                            except NoReverseMatch:
                                pass
                        if perms.get("add"):
                            try:
                                model_dict["add_url"] = reverse(
                                    "admin:%s_%s_add" % info,
                                    current_app=self.name,
                                )
                            except NoReverseMatch:
                                pass

                        if app_name in app_dict:
                            app_dict[app_name]["models"].append(model_dict)
                        else:
                            app_dict[app_name] = {
                                "name": app_name,
                                "app_label": app_name,
                                "app_url": "",
                                "has_module_perms": has_module_perms,
                                "models": [model_dict],
                            }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        # Sort the apps alphabetically.
        app_list = app_dict.values()
        return app_list


admin_site = AdminSiteRegroup()
admin_site_register = partial(admin.register, site=admin_site)
