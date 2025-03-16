import requests
from django.http import JsonResponse
from django.shortcuts import render

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

DEEPSEEK_API_KEY = "sk-b0f392d19e834bbeb271b3f04e50c1aa"

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        #llamar a la api
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'deepseek-v3',
            'messages': [{'role':'user', 'content': user_message}],
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers = headers, json=data)
        
        if response.status_code == 200:
            bot_response = response.json()["choices"][0]["message"]["content"]
            return JsonResponse({'response': bot_response})
        else: 
            return JsonResponse({'error': "Error al comunicarse con la API"}, status=500)

    return render(request, 'chat/index.html')    
