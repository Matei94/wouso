from django import template
from wouso.core.ui import get_sidebar, get_library
from wouso.core.config.models import Setting
register = template.Library()

@register.simple_tag(takes_context=True)
def render_zone(context, zone, glue):
    """
    :return: HTML for the sidebar
    """
    s = get_library(zone)
    order = [k for k in Setting.get('%s-order' % zone).get_value().split(',') if k]
    if not order:
        order = s.get_blocks()
    return glue.join([s.get_block(block, context) for block in order])


@register.simple_tag(takes_context=True)
def render_sidebar(context):
    return render_zone(zone='sidebar', context=context, glue='')


@register.simple_tag(takes_context=True)
def render_header(context):
    s = get_library('header')
    order = [k for k in Setting.get('header-order').get_value().split(',') if k]
    if not order:
        order = s.get_blocks()
    content = ''
    for block in order:
        data = s.get_block(block, context)
        content += '<span id="head-%s"><a href="%s">%s</a>' % (block, data.get('link', ''), data.get('text', ''))
        if data.get('count', 0):
            content += '<sup class="unread-count">%s</sup>' % data.get('count')
        content += '</span> '
    return content

@register.simple_tag(takes_context=True)
def render_footer(context):
    return render_zone(context=context, zone='footer', glue=' | ')