from django import template


register = template.Library()


@register.filter
def sep_by(queryset, separator=', '):
    return separator.join(map(str, queryset))


@register.filter
def change_number_sign(number: (int, float)):
    number = 0 if number is None else number
    return -number if number > 0 else abs(number)


@register.filter
def make_range(number: int):
    number = 0 if number is None else round(number)
    return range(number)
