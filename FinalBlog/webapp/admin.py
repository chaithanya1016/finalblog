from django.contrib import admin
from .models import Category,Article,Comment,Profile

# Register your models here.

#Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','profile_pic','bio','location','birth_date']
admin.site.register(Profile,ProfileAdmin)

#Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug']
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Category,CategoryAdmin)


#Article
class ArticleAdmin(admin.ModelAdmin):
    list_display =['id','title','slug','overview','article_image','author','category','body','publish','status','viewcount','previous_post','next_post']
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Article,ArticleAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
