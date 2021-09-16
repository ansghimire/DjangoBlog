from django.shortcuts import render, HttpResponse,redirect
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
   allPosts = Post.objects.all()
   # print(allPosts)
   context = {'allPosts':allPosts}
   return render(request, 'blog/blogHome.html',context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views =  post.views + 1
    post.save()
    
    comments = BlogComment.objects.filter(post = post, parent=None)
    replies = BlogComment.objects.filter(post = post).exclude(parent=None)
    #print(comments,replies)
    replyDict={}
    for reply in replies:
       if reply.parent.sno not in replyDict.keys():
          replyDict[reply.parent.sno] = [reply]
       else:
          replyDict[reply.parent.sno].append(reply)  
   #  print(replyDict)
    context = {'post':post, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    return render(request, 'blog/blogPost.html',context)


def postComment(request):
   if request.method == "POST":
      comment = request.POST.get("comment")
      user = request.user
      postSno = request.POST.get("postSno")
      post = Post.objects.get(sno = postSno)
      parrentSno = request.POST.get("parrentSno")
      if parrentSno == '':
         comment = BlogComment(comment=comment, user=user, post=post)
         comment.save()
         messages.success(request, "Your comment has been posted sucessfully")
      
      else:
         parent = BlogComment.objects.get(sno = parrentSno)
         comment = BlogComment(comment=comment, user=user, post=post,parent=parent)
         comment.save()
         messages.success(request, "Your reply has been posted sucessfully")


   return redirect(f"/blog/{post.slug}")