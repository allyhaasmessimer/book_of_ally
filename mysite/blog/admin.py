from django.contrib import admin
from .models import Post, Subscriber
import mailchimp_transactional as MailchimpTransactional
import os
from dotenv import load_dotenv

load_dotenv()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    actions = ["delete_selected"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        ##FOR EMAILING SUBSCRIBE UPDATES. I HAVE PAUSED THIS FOR NOW
        # try:
        #     mailchimp = MailchimpTransactional.Client(
        #         os.getenv("MAILCHIMP_TRANSACTIONAL_KEY")
        #     )

        #     subscribers = Subscriber.objects.values_list("email", flat=True)

        #     for email in subscribers:
        #         mailchimp.messages.send(
        #             {
        #                 "message": {
        #                     "subject": "New Blog Post",
        #                     "from_email": "bookofally@allyhaas.com",
        #                     "to": [{"email": email, "type": "to"}],
        #                     "text": f"A new blog post '{obj.title}' has been published. Check it out at: allyhaas.com/blog/{obj.slug}\n\nTo unsubscribe, click here: allyhaas.com/unsubscribe",
        #                 }
        #             }
        #         )
        # except Exception as e:
        #     pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email",)
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        queryset.delete()

    delete_selected.short_description = "Delete selected"
