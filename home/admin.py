from django.contrib import admin
from .models import Post,Comment,Vote

class PostAdmin(admin.ModelAdmin):
    list_display =['user' , 'slug' , 'updated']
    raw_id_fields = ['user']
    search_fields = ['slug','body','updated']
    prepopulated_fields = {'slug':('body',)}
    list_filter = ['updated']
admin.site.register(Post,PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','post','body','created' , 'is_reply']
    raw_id_fields = ['user','post','reply']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


