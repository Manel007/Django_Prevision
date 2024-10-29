from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import Image

load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)
openai.api_key = api_key

def generate_image_from_txt(request):
    obj = None
    if api_key is not None and request.method == 'POST' :
        user_input = request.POST.get('user_input')
        response = openai.Image.create(
            prompt=user_input,
            size='256x256'
        )
        img_url = response['data'][0]['url']

        response = requests.get(img_url)
        img_file = ContentFile(response.content)

        count = Image.objects.count() + 1
        fname = f"image-{count}.jpg"

        obj = Image(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()

        print(obj)

    return render(request, "image.html", {"object":obj})