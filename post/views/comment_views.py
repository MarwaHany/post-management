from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..helpers import authenticate_user
from ..models import Comment, Post

from http import HTTPStatus

import json


@api_view(["GET"])
@authenticate_user
def list(request):
    comments = []
    post = Post.objects.filter(id=request.GET.get("post_id"))
    if bool(post):
        comments = [{"Body": c.Body} for c in (post[0].Comments.all())]
    else:
        return Response(
            {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    context = {"comments": comments}
    return Response(context)


@api_view(["GET"])
@authenticate_user
def detail(request):
    # show specific post
    post = Post.objects.filter(id=request.GET.get("post_id"))
    if not bool(post):
        return Response(
            {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    comment = Comment.objects.filter(id=request.GET.get("comment_id"))
    if not bool(comment):
        return Response(
            {"error message": "no comments on the requested post."},
            status=HTTPStatus.OK,
        )
    context = {"author": comment[0].Author.username, "body": comment[0].Body}
    return Response(context)


@api_view(["POST"])
@csrf_exempt
@authenticate_user
def post(request):
    body = json.loads(request.body)
    post_id = body.get("post_id")
    comment_body = body.get("body")
    post = Post.objects.filter(id=post_id)
    if not bool(post):
        return Response(
            {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    author = User.objects.filter(id=post[0].Author.id)
    Comment.objects.create(Author=author[0], Body=comment_body)
    return Response(
        {"message": "comment was created successfuly!"}, status=HTTPStatus.CREATED
    )


@api_view(["PUT"])
@authenticate_user
@csrf_exempt
def update(request):
    user = authenticate(
        request,
        username=request.headers.get("username"),
        password=request.headers.get("authorization"),
    )
    body = json.loads(request.body)
    comment_id = body.get("comment_id")
    new_body = body.get("body")
    try:
        comment = Comment.objects.get(pk=comment_id)
        if comment.Author.id != user.id:
            return Response(
                {"error message": "this user can not edit the requested comment."},
                status=HTTPStatus.UNAUTHORIZED,
            )
        comment.Body = new_body
        comment.save(0)
        return Response(
            {"message": "comment body is updated successfully."},
            status=HTTPStatus.OK,
        )
    except:
        return Response(
            {"error message": "comment does not exist."},
            status=HTTPStatus.NOT_FOUND,
        )


@api_view(["DELETE"])
@authenticate_user
@csrf_exempt
def delete(request):
    user = authenticate(
        request,
        username=request.headers.get("username"),
        password=request.headers.get("authorization"),
    )
    body = json.loads(request.body)
    comment_id = int(body.get("comment_id"))
    try:
        comment = Comment.objects.get(pk=comment_id)
        if comment.Author.id != user.id:
            return Response(
                {"error message": "this user can not delete the requested comment."},
                status=HTTPStatus.UNAUTHORIZED,
            )
        comment.delete()
        return Response(
            {"message": "comment was deleted successfully."}, status=HTTPStatus.OK
        )
    except:
        return Response(
            {"error message": "comment does not exist."},
            status=HTTPStatus.NOT_FOUND,
        )
