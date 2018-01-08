from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(name='svg_icon')
def svg_icon(icon_name, icon_color, extra_class=''):
    svg_tag = format_html('<svg viewBox="0 0 210.27 210.27" class="icon-{name} {extra} icon-{color}">'
               '<use xlink:href="#{name}" class="sym-{name}"></use>'
               '</svg>', name=icon_name, color=icon_color, extra=extra_class)

    return mark_safe(svg_tag)