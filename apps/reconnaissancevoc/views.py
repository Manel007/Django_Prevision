from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
from decouple import config
from django.conf import settings
from pathlib import Path
import time

class SpeechToTextView(View):
    
    def get(self, request):
        return render(request, 'transcribe.html')

    def post(self, request):
        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']
            fs = FileSystemStorage()
            filename = fs.save(audio_file.name, audio_file)
            file_path = fs.url(filename)

            transcript = self.transcribe_audio(filename)
            return JsonResponse({'transcript': transcript}, status=200)
        
        return JsonResponse({'error': 'Aucun fichier audio fourni'}, status=400)

    def transcribe_audio(self, filename):
        headers = {
            'authorization': config('ASSEMBLYAI_API_KEY').strip(),
            'content-type': 'application/json'
        }
        
        print("Clé API lue :", headers['authorization'])  # Vérifiez ici la clé

        file_path = Path(settings.MEDIA_ROOT) / filename

        with open(file_path, 'rb') as audio:
            response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=audio)

        if response.status_code != 200:
            return f'Erreur lors de l\'upload du fichier audio. Code d\'état : {response.status_code}, Réponse : {response.text}'

        audio_url = response.json()['upload_url']
        json = {'audio_url': audio_url}
        response = requests.post('https://api.assemblyai.com/v2/transcript', json=json, headers=headers)

        if response.status_code != 201:
            return 'Erreur lors de la demande de transcription.'

        transcript_id = response.json()['id']
        return self.get_transcription_result(transcript_id, headers)

    def get_transcription_result(self, transcript_id, headers):
        while True:
            response = requests.get(f'https://api.assemblyai.com/v2/transcript/{transcript_id}', headers=headers)
            transcript_result = response.json()
            if transcript_result['status'] == 'completed':
                return transcript_result['text']
            elif transcript_result['status'] == 'failed':
                return 'Échec de la transcription.'
            time.sleep(3)  # Attendre avant de vérifier à nouveau
