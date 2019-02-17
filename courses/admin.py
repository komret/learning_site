from datetime import date

from django.contrib import admin

from . import models


def make_published(modeladmin, request, queryset):
    queryset.update(status='p', is_live=True)


make_published.short_description = 'Mark selected courses as Published'


class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('2018', '2018'),
            ('2019', '2019')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                created_at__gte=date(int(self.value()), 1, 1), created_at__lt=date(int(self.value()), 12, 31)
            )


class AnswerInline(admin.TabularInline):
    model = models.Answer


class CourseAdmin(admin.ModelAdmin):
    list_filter = ['created_at', YearListFilter]
    search_fields = ['title', 'description']
    list_display = ['title', 'created_at', 'time_to_complete', 'is_live', 'status']
    list_editable = ['status']
    actions = [make_published]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    search_fields = ['prompt']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']


class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'description', 'order', 'total_questions']


class TextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'order', 'description')
        }),
        ('Add content', {
            'fields': ('content',),
            'classes': ('collapse',)
        })
    )


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion, QuestionAdmin)
