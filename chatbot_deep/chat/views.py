import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

DEEPSEEK_API_KEY = "-----"

@csrf_exempt

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        try:
            #llamar a la api
            header = {
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json',
            }
            data = {
                'model': 'deepseek-chat',
                'messages': [{'role':'user', 'content': user_message}],
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
        
    return render(request, 'chat/index.html')    
