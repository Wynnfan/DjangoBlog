from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
# Create your models here.

# 分类表
@python_2_unicode_compatible
class Category(models.Model):
    """
    Django 要求模型必须继承models.Model类，
    Category 只需要一个简单的分类名 name 就可以，
    CharField 的 max_length 指定最大长度，超出最大长度就不能被存入数据库
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 标签表
@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签 Tag 也只需要一个 name
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# 文章表
@python_2_unicode_compatible
class Post(models.Model):

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文 使用 TextField,
    # 较短字符串用 CharField, 较长用 TextField
    body = models.TextField()

    # 创建两个列表示文章的创建时间和最后一次修改时间，存储时间字段用 DateTimeField
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有摘要，默认情况 CharField 要求必须存入数据
    # 指定 CharField 的 blank=True 参数值后可以允许空值
    excerpt = models.CharField(max_length=100, blank=True)

    # 分类和标签的模型定义在上面
    # 将文章对应的数据库表和分类、标签对应的数据库表关联
    # 一篇文章只能对应一个分类，一个分类可以对应多篇文章，一对多的关系，使用 ForeignKey,即一对多的关联关系
    # 一篇文章可以有多个标签，一个标签下也可能有多篇文章，多对多的关联关系，使用 ManyToManyField
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者， User 是从 django.contrib.auth.models 导入
    # django.contrib.auth 是Djano 内置应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 写好的用户模型
    # 通过 ForeignKey 把文章和 User 关联起来
    # 一篇文章只能有一个作者，一个作者可能有多篇文章，一对多关联关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 从 diango.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Mate:
        ordering = ['-created_time']