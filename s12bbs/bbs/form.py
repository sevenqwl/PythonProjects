from django.forms import ModelForm
from bbs import models

class ArticleModelForm(ModelForm):

    class Meta:
        model = models.Article
        exclude = ('author', 'pub_date', 'priority')

    def __init__(self,*args,**kwargs):  # 重新初始化field样式
        super(ArticleModelForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs['class'] = 'form-control'

        for field_name in self.base_fields:
            field = self.base_fields[field_name]

            field.widget.attrs.update({'class': 'form-control'})
