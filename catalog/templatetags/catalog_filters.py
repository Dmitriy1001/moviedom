from django import template


register = template.Library()


@register.filter
def sep_by(queryset, separator=', '):
    return separator.join(map(str, queryset))