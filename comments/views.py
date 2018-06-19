from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm
# Create your views here.

def post_comment(request, post_pk):
    # 获取被评论的文章
    # get_object_or_404 函数作用是获取文章存在时返回该文章，否则返回404
    post = get_object_or_404(Post, pk=post_pk)

    # 表单提交使用 post 请求
    if request.method == 'POST':

        form = CommentForm(request.POST)

        # 调用 form.is_calid() 方法时，Django 自动检查表单数据是否符合要求
        if form.is_valid():
            # 数据合法，调用表单的 save() 方法保存数据到数据库
            comment = form.save(commit=False)

            # 将评论和文章关联
            comment.post = post

            comment.save()

            # 重定向到 post 详情页
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)

    return redirect(post)