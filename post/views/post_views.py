from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from http import HTTPStatus

from ..models import Comment, Post

import json

# Create your views here.


def get(request):
    if request.method == "GET":
        posts = []
        author = User.objects.filter(username=request.GET.get("username"))
        if bool(author):
            posts = [
                {"Title": p.Title} for p in (Post.objects.filter(Author=author[0].id))
            ]
        else:
            return JsonResponse(
                {"error message": "no author found with the requested username."},
                status=HTTPStatus.NOT_FOUND,
            )
        context = {"posts": posts}
        return JsonResponse(context, safe=False)
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


def detail(request):
    # show specific post
    if request.method == "GET":
        author = User.objects.filter(username=request.GET.get("username"))
        if not bool(author):
            return JsonResponse(
                {"error message": "no author found with the requested username."},
                status=HTTPStatus.NOT_FOUND,
            )
        post = Post.objects.filter(
            id=int(request.GET.get("id")), Author=author[0].id
        ).first()
        if bool(post):
            comments = [
                {"body": c.Body} for c in Comment.objects.filter(post__id=post.id).all()
            ]
            context = {
                "Post details": {
                    "title": post.Title,
                    "body": post.Body,
                    "comments": comments,
                }
            }
            return JsonResponse(context, safe=False)
        else:
            return JsonResponse(
                {"message": "post does not exist."},
                safe=False,
                status=HTTPStatus.NOT_FOUND,
            )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


@csrf_exempt
def post(request):
    if request.method == "POST":
        body = json.loads(request.body)
        author_name = body.get("author")
        post_title = body.get("title")
        post_body = body.get("body")
        author = User.objects.filter(username=author_name)
        if not bool(author):
            return JsonResponse(
                {"error message": "no author found with the requested username."},
                status=HTTPStatus.NOT_FOUND,
            )
        Post.objects.create(Author=author[0], Title=post_title, Body=post_body)
        return JsonResponse(
            {"message": "post was created successfuly!"}, status=HTTPStatus.CREATED
        )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


@csrf_exempt
def update(request):
    if request.method == "PUT":
        print(request.headers)
        body = json.loads(request.body)
        post_id = int(body.get("post_id"))
        new_body = body.get("body")
        try:
            post = Post.objects.get(pk=post_id)
            post.Body = new_body
            post.save(0)
            return JsonResponse(
                {"message": "post body is updated successfully."}, status=HTTPStatus.OK
            )
        except:
            return JsonResponse(
                {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
            )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


@csrf_exempt
def delete(request):
    if request.method == "DELETE":
        body = json.loads(request.body)
        post_id = int(body.get("post_id"))
        try:
            post = Post.objects.get(pk=post_id)
            post.delete()
            return JsonResponse(
                {"message": "post was deleted successfully."}, status=HTTPStatus.OK
            )
        except:
            return JsonResponse(
                {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
            )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )
