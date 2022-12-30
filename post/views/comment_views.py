import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Comment, Post
from django.contrib.auth.models import User
from http import HTTPStatus


def list(request):
    if request.method == "GET":
        comments = []
        post = Post.objects.filter(id=request.GET.get("post_id"))
        if bool(post):
            comments = [{"Body": c.Body} for c in (post[0].Comments.all())]
        else:
            return JsonResponse(
                {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
            )
        context = {"comments": comments}
        return JsonResponse(context, safe=False)
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


def detail(request):
    # show specific post
    if request.method == "GET":
        post = Post.objects.filter(id=request.GET.get("post_id"))
        if not bool(post):
            return JsonResponse(
                {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
            )
        comment = Comment.objects.filter(id=request.GET.get("comment_id"))
        if not bool(comment):
            return JsonResponse(
                {"error message": "no comments on the requested post."},
                status=HTTPStatus.OK,
            )
        context = {"author": comment[0].Author.username, "body": comment[0].Body}
        return JsonResponse(context, safe=False)
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


@csrf_exempt
def post(request):
    if request.method == "POST":
        body = json.loads(request.body)
        post_id = body.get("post_id")
        comment_body = body.get("body")
        post = Post.objects.filter(id=post_id)
        if not bool(post):
            return JsonResponse(
                {"error message": "post does not exist."}, status=HTTPStatus.NOT_FOUND
            )
        author = User.objects.filter(id=post[0].Author.id)
        Comment.objects.create(Author=author[0], Body=comment_body)
        return JsonResponse(
            {"message": "comment was created successfuly!"}, status=HTTPStatus.CREATED
        )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


@csrf_exempt
def update(request):
    if request.method == "PUT":
        print(request.headers)
        body = json.loads(request.body)
        comment_id = body.get("comment_id")
        new_body = body.get("body")
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.Body = new_body
            comment.save(0)
            return JsonResponse(
                {"message": "comment body is updated successfully."},
                status=HTTPStatus.OK,
            )
        except:
            return JsonResponse(
                {"error message": "comment does not exist."},
                status=HTTPStatus.NOT_FOUND,
            )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )


@csrf_exempt
def delete(request):
    if request.method == "DELETE":
        body = json.loads(request.body)
        comment_id = int(body.get("comment_id"))
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse(
                {"message": "comment was deleted successfully."}, status=HTTPStatus.OK
            )
        except:
            return JsonResponse(
                {"error message": "comment does not exist."},
                status=HTTPStatus.NOT_FOUND,
            )
    return JsonResponse(
        {"error message": "method is not supported."}, status=HTTPStatus.NOT_FOUND
    )
