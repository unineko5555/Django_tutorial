#settig.py 行108 課題8の写真のように言語を英語から日本語に変更
#問1 admin.py 行25,change_form.html
#問2 admin.py 行28~44,new_page.html,change_list.html
#問3 admin.py 行47~53
#問4 admin.py 行62,63
#問5 admin.py 行68~92
#問6 admin.py 行81,84~87

from django.contrib import admin
from django.urls import reverse
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.template.response import TemplateResponse

from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):

    #問1:QuestionAdmin内でchange_form_templateを設定
    change_form_template = "admin/polls/question/change_form.html"
    
    #問2:QuestionAdminモデルに関する新しいページを追加するためのカスタムなURLを作成。get_urlsメソッドはAdminサイトにカスタムURLパターンを追加する。このメソッドは既存のURLパターンを取得し新しいURLパターンを追加する。
    def get_urls(self):

        # 親クラス（super()）のget_urls()メソッドを呼び出して既存のURLパターンを取得
        urls = super().get_urls()

        # 新しいページへのURLパターンを作成し、リストに追加
        my_urls = [
            path('new_page/', self.admin_site.admin_view(self.new_page), name='polls_question_new_page'),
        ]
        return my_urls + urls
    
    #問2:new_pageメソッドは新しいページのビューを定義する。このビューでは新しいページの表示に必要なコンテキストを作成しTemplateResponseを使用し指定されたテンプレートをレンダリングする。
    def new_page(self, request):
        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, 'admin/polls/question/new_page.html', context)

    #問3:渡されたクエリセット内の各モデルオブジェクトのquestion_textをotherに変更し保存。選択された複数のオブジェクトのquestion_textを一括で変更する
    def change_title_to_other(modelAdmin, request, queryset):
        for title in queryset.all():
            title.question_text = "other"
            title.save()

    change_title_to_other.short_description = "タイトルをotherに変える"
    actions = ['change_title_to_other'] 
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    #問4:一覧画面においてlist_editableで編集可能になりlist_display_linksで詳細ページに移動できるようになる
    list_editable = ['question_text'] 
    list_display_links = ['pub_date'] 
    list_filter = ['pub_date']
    search_fields = ['question_text']

#問5:既存のQuestionモデルを継承し拡張するのでNewQuestionプロキシモデルを作成。プロキシモデルは新しいデータベースを作成せずに元のモデルと同じテーブルを共有しそのモデルに機能を追加するのに適する。
class NewQuestion(Question):
    class Meta:
        proxy = True

class NewQuestionAdmin(admin.ModelAdmin):

    fieldset = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    #問6:個別編集ページに遷移するためのedit_link属性を追加。
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'edit_link')

    #問6:edit_linkメソッドを定義。format_htmlを使用して安全なHTMLコードを生成。obj(モデルのインスタンス)から取得したidを取得して編集ページへのリンクを生成する。
    def edit_link(self, obj):
        return format_html('<a href="{}">Edit</a>', obj.id)
    
    edit_link.short_description = '編集ボタン'
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(NewQuestion, NewQuestionAdmin)
