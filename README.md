# SetUp

1. Python 3.9+, Django 3.2

# How it works?

1. To use this package, need to add `admin.py` and `templates` to the project.
2. Set the order of the models in the desired order. It should be a *dictionary* - `ADMIN_APPS`, where the key is the title of the block, and the *values* are a tuple of models (either the name of the model in `CamelCase`, or `capfirst` for the `verbose_name_plural` of the model).
3. Change main `urls.py` (`path("admin/", admin.site.urls),` -> `path("admin/", admin_site.urls)` (from `admin.py`))
4. Change `admin.site.register` to `admin_site.register` and `@admin.register` to `admin_site.register` in `admin.py` of apps

**Example**:
```python
ADMIN_APPS = {
    "Some group": ("Users",),  # capfirst
    "Also group": ("Contact", "User", "Folder"),  # CamelCase
}
```
