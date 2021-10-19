from django import template


register = template.Library()


@register.filter
def sep_by(queryset, separator=', '):
    return separator.join(map(str, queryset))


@register.filter
def change_number_sign(number:(int, float)):
    return -number if number > 0 else abs(number)
