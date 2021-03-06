import markdown2
from django import template
from django.utils.safestring import mark_safe

from courses.models import Course

register = template.Library()


@register.simple_tag
def newest_course():
    return Course.objects.filter(published=True).latest("created_at")


@register.inclusion_tag("courses/course_nav.html")
def nav_course_list():
    return {"courses": Course.objects.filter(published=True).order_by("-created_at").values("id", "title")[:5]}


@register.filter("time_estimate")
def time_estimate(wordcount):
    return round(wordcount/20)


@register.filter("markdown_to_html")
def markdown_to_html(markdown_text):
    return mark_safe(markdown2.markdown(markdown_text))
