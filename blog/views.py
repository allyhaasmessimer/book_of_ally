from django.http import JsonResponse
from django.views import View
from .models import Post, Subscriber
from .forms import SubscribeForm
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
import os
from dotenv import load_dotenv
import mailchimp_transactional as MailchimpTransactional
from django.urls import reverse
from django.conf import settings

load_dotenv()


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status=1).order_by("-created_on")

        post_data = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_on": post.created_on,
                "slug": post.slug,
                "image": self.generate_presigned_url(post.image) if post.image else None,
            }
            for post in posts
        ]
        return JsonResponse({"posts": post_data})

    def generate_presigned_url(self, image):
        if image:
            url = settings.MEDIA_URL + image.name
            return url
        return None


class PostDetailView(View):
    def get_object(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        post = self.get_object(kwargs["slug"])

        if post is None:
            return JsonResponse({}, status=404)

        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_on": post.created_on,
            "image": post.image.url if post.image else None,
        }
        return JsonResponse(post_data)


@csrf_exempt
def get_csrf_token(request):
    csrf_token = csrf.get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            Subscriber.objects.get_or_create(email=email)

            return JsonResponse({"message": "Thanks for subscribing!"})
        else:
            return JsonResponse({"message": "Invalid form data."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)


@csrf_exempt
def unsubscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
            return JsonResponse({"message": "You have been unsubscribed successfully."})
        except Subscriber.DoesNotExist:
            return JsonResponse({"message": "Email not found."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)


@csrf_exempt
def create_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        author = request.user
        content = request.POST.get("content")
        image = request.FILES.get("image")

        post = Post.objects.create(
            title=title,
            slug=slug,
            author=author,
            content=content,
            image=image,
            status=0,
        )

        try:
            mailchimp = MailchimpTransactional.Client(
                os.getenv("MAILCHIMP_TRANSACTIONAL_KEY")
            )

            subscribers = Subscriber.objects.values_list("email", flat=True)

            for email in subscribers:
                unsubscribe_url = request.build_absolute_uri(reverse("unsubscribe")) + "?email=" + email
                message = f"A new blog post '{title}' has been published"
                mailchimp.messages.send(
                    {
                        "message": {
                            "subject": "New Blog Post",
                            "from_email": "bookofally@allyhaas.com",
                            "to": [{"email": email, "type": "to"}],
                            "text": message,
                        }
                    }
                )

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    else:
        return JsonResponse({"success": False, "errors": "Invalid request method."})
