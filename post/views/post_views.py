from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
from rest_framework.decorators import api_view
from rest_framework.response import Response

from post.helpers import authenticate_user
from ..models import Comment, Post

import json

# Create your views here.
@api_view(["GET"])
@authenticate_user
def get(request):
    posts = []
    author = User.objects.filter(username=request.GET.get("username"))
    if bool(author):
        posts = [{"Title": p.Title} for p in (Post.objects.filter(Author=author[0].id))]
    else:
        return Response(
            {"error message": "no author found with the requested username."},
            status=HTTPStatus.NOT_FOUND,
        )
    context = {"posts": posts}
    return Response(context)


@api_view(["GET"])
@authenticate_user
def detail(request):
    # show specific post
    author = User.objects.filter(username=request.GET.get("username"))
    if not bool(author):
        return Response(
            {"error message": "no author found with the requested username."},
            status=HTTPStatus.NOT_FOUND,
        )
    post = Post.objects.filter(
        id=request.GET.get("post_id"), Author=author[0].id
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
        return Response(context)
    else:
        return Response(
            {"message": "post does not exist."},
            status=HTTPStatus.NOT_FOUND,
        )


@api_view(["POST"])
@csrf_exempt
@authenticate_user
def post(request):
    body = json.loads(request.body)
    author_name = body.get("author")
    post_title = body.get("title")
    post_body = body.get("body")
    author = User.objects.filter(username=author_name)
    if not bool(author):
        return Response(
            {"error message": "no author found with the requested username."},
            status=HTTPStatus.NOT_FOUND,
        )
    Post.objects.create(Author=author[0], Title=post_title, Body=post_body)
    return Response(
        {"message": "post was created successfuly!"}, status=HTTPStatus.CREATED
    )


@api_view(["PUT"])
@csrf_exempt
@authenticate_user
def update(request):
    body = json.loads(request.body)
    post_id = int(body.get("post_id"))
    new_body = body.get("body")
    try:
        post = Post.objects.get(pk=post_id)
        post.Body = new_body
        post.save(0)
        return Response(
            {"message": "post body is updated successfully."}, status=HTTPStatus.OK
        )
    except:
        return Response(
            {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
        )


@api_view(["DELETE"])
@csrf_exempt
@authenticate_user
def delete(request):
    body = json.loads(request.body)
    post_id = int(body.get("post_id"))
    try:
        post = Post.objects.get(pk=post_id)
        post.delete()
        return Response(
            {"message": "post was deleted successfully."}, status=HTTPStatus.OK
        )
    except:
        return Response(
            {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
        )
