import requests
from decouple import config
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

Google_API_URL = 'https://speech.googleapis.com/v1p1beta1/speech:recognize'

DEEPSEEK_API_KEY = config('DEEPSEEK_API_KEY')

Google_API_KEY = config('Google_API_KEY')

context = ''

header = {
    'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
    'Content-Type': 'application/json',
}

with open('chat/context.txt', mode = 'r') as file:
    for line in file:
        context += line


with open('chat/test.ogg', mode = 'rb') as afile:
    audio = afile.read()
@csrf_exempt



def chat(request):
    if request.method == 'POST':
        match request.POST.get('obj'):
            case 'api':
                user_message = request.POST.get('content')
                try:
                    #llamar a la api
                    
                    data = {
                        'model': 'deepseek-chat',
                        'messages': [{'role':'system', 'content': context},
                                    {'role':'user', 'content': user_message}],
                    }
                    
                    response = requests.post(DEEPSEEK_API_URL, headers = header, json=data)
                    response.raise_for_status()
                    
                    bot_response = response.json()["choices"][0]["message"]["content"]
                    return JsonResponse({'response': bot_response})
                
                except requests.exceptions.RequestException as e:
                    # Captura errores de la solicitud a la API
                    return JsonResponse({"error": f"Error al comunicarse con la API: {str(e)}"}, status=response.status_code)
                except KeyError as e:
                    # Captura errores si la estructura de la respuesta no es la esperada
                    return JsonResponse({"error": f"Error en la respuesta de la API: {str(e)}"}, status=response.status_code)
            
            case 'speechToTxt':
                voice = request.POST.get('content')
                
                data = {
                    'audio': {
                        'content': audio.hex(),
                    },
                    'config':{
                        "enableAutomaticPunctuation": True,
                        "encoding": "LINEAR16",
                        "languageCode": "es-MX",
                        "model": "default",
                    }
                }
                
                response = requests.post(Google_API_URL, headers=header, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    for alternative in result.get("results", [])[0].get("alternatives", []):
                        return JsonResponse("Texto transcrito: {}".format(alternative["transcript"]))
                else:
                    return JsonResponse(f"Error: {response.status_code} - {response.text}")
                
                
                
                
    return render(request, 'chat/index.html')    
