from django.core.management.base import BaseCommand
from django.core.files import File
from tweet.models import Tweet
import os

class Command(BaseCommand):
    help = "Upload all existing Tweet photos to Cloudinary"

    def handle(self, *args, **options):
        tweets = Tweet.objects.all()
        uploaded_count = 0

        for tweet in tweets:
            if tweet.photo:
                try:
                    local_path = tweet.photo.path
                except ValueError:
                    self.stdout.write(f"Skipping tweet {tweet.id}: no local file")
                    continue

                if os.path.exists(local_path):
                    self.stdout.write(f"Uploading tweet {tweet.id} photo: {local_path}")
                    # Open the local file in binary mode
                    with open(local_path, 'rb') as f:
                        # Save to the ImageField using Django's storage (Cloudinary)
                        tweet.photo.save(os.path.basename(local_path), File(f), save=True)
                        uploaded_count += 1
                else:
                    self.stdout.write(f"File does not exist: {local_path}")

        self.stdout.write(self.style.SUCCESS(f"Uploaded {uploaded_count} images to Cloudinary"))
