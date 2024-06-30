from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, ArticleScope


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_scope_count = 0
        tag_names = set()
        duplicate_tags = set()

        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_scope_count += 1
            if main_scope_count > 1:
                raise ValidationError('Может быть только один основной раздел')

            tag = form.cleaned_data.get('tag')
            if tag is not None:
                tag_name = tag.name
                if tag_name in tag_names:
                    duplicate_tags.add(tag_name)
                tag_names.add(tag_name)

            if form.instance.is_main and form.cleaned_data.get('DELETE'):
                raise ValidationError('Нельзя удалять основной раздел')

            if form.cleaned_data.get('DELETE'):
                form.instance.save()

        if main_scope_count != 1:
            raise ValidationError('Пожалуйста, выберите один основной раздел')

        if duplicate_tags:
            raise ValidationError(f'Теги не должны повторяться: {", ".join(duplicate_tags)}')

        return super().clean()



class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset




@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
