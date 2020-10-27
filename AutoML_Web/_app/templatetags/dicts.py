from django import template
register=template.Library()

@register.filter(name="dict_get")
def dict_get(ds,pk):
    return ds.get(pk)