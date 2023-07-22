from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS
from django.core.files.base import ContentFile
import os
import uuid
from .models import TextToSpeech
from django.conf import settings
from django.utils import timezone



def text_to_mp3(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        if not text:
            return HttpResponse("Please provide some text to convert to MP3.")

        # Get the user's IP address
        user_ip = request.META.get('REMOTE_ADDR')

        # Check the user's text count
        user_text_count = TextToSpeech.objects.filter(user_ip=user_ip).count()

        if user_text_count >= 3:
            return HttpResponse("You have reached the limit of 3 text files.")

        # Generate the MP3 file using gTTS
        tts = gTTS(text)
        mp3_file = os.path.join(settings.MEDIA_ROOT, f"{user_ip}.mp3")
        tts.save(mp3_file)

        # Read the MP3 file content
        with open(mp3_file, 'rb') as file:
            mp3_file_content = file.read()

        # Clean up the temporary MP3 file
        os.remove(mp3_file)

        # Save the MP3 file and data in the database
        text_to_speech_obj = TextToSpeech.objects.create(user_ip=user_ip, text=text)
        mp3_file_name = f"{user_ip}.mp3"
        text_to_speech_obj.mp3_file.save(mp3_file_name, ContentFile(mp3_file_content))

        # Update user's text count
        text_to_speech_obj.mp3_count_today = user_text_count + 1
        text_to_speech_obj.last_generated_at = timezone.now()
        text_to_speech_obj.save()

        return render(request, 'result.html', {'text_to_speech_obj': text_to_speech_obj})

    return render(request, 'text_to_mp3.html')

def home(request):
    return render(request,'home.html',{})
