from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth as auth
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
import requests
from transformers import AutoTokenizer
from .models import Messages

def return_tokens(text):
    tokenizer = AutoTokenizer.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v0.6')
    return(len(tokenizer.tokenize(text)))

def get_message_history(user, message):
    chats = Messages.objects.filter(user=user)
    in_limit = True
    chat_history = chat = ''
    counter = len(chats)-1
    if len(chats)==0:
        return ''
    
    while(in_limit):
        if counter>=0:
            chat_history+=str(chats[counter-1])+'\n'
            chat_history+=str(chats[counter])+'\n'
            counter-=2
    
        str_test = f'You are a helpful assistant, here is the history of your chat with this user in reverse order{chat_history} {message}'
        if return_tokens(str_test)<=2048:
            chat = chat_history
        else:
            in_limit = False
        if counter < 0:
            in_limit = False
    return chat

    #return f'{user, message}'

def ask_llm(user_logged_in, user, message):
    
    #return 'fast'
    url = 'http://127.0.0.1:11434/api/chat'
    if user_logged_in == False:
        payload = {
            'model': 'tinyllama',
            'messages': [
                {'role': 'user', 'content': message}
            ],
            'stream': False
        }
    else:
        history = get_message_history(user, message)
        if history == '':
            payload = {
                'model': 'tinyllama',
                'messages': [
                    {'role': 'user', 'content': message}
                ],
                'stream': False
            }
        else:
            print('Passing history: ',history)
            payload = {
                'model': 'tinyllama',
                'messages': [
                    {'role': 'system', 'content': f'You are a helpful assistant, here is the history of your chat with this user in reverse order{history}'},
                    {'role': 'user', 'content': message}
                ],
                'stream': False
            }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        #print(type(response))
        return 'Agent', data['message']['content'].strip()
        #return ('sample content for now')
    except:
        return 'System', 'Model refused connection, try again'

def save_message(sender, user, content):
    msg = Messages(sender=sender,user=user,content=content)
    msg.save()

# Create your views here.
get_rate = lambda _, r: '5/m' if r.user.is_authenticated else '3/m'
@ratelimit(key='ip', rate=get_rate)
def chatbot(request):
    chats=[]
    user_logged_in = False
    if request.user.is_authenticated:
        user_logged_in = True
        chats = Messages.objects.filter(user=request.user)
        #get_message_history(request.user, 'llm1')
    if request.method=='POST':
        message = request.POST.get('message')
        sender, response = ask_llm(user_logged_in, request.user, message)

        user = request.user if user_logged_in else None

        save_message('User', user, message)
        save_message(sender, user, response)

        # Messages = Messages(sender = False,
        #                     user = user, 
        #                     content = message, 
        #                     )
        # Messages.save()
        
        # Messages = Messages(sender = True,
        #                     user = user, 
        #                     content = response, 
        #                     )
        # Messages.save()

        return(JsonResponse({'sender': sender, 'message': message, 'response': response}))
    return(render(request, 'chatbot.html', {'chats': chats}))
    

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if username != 'Anonymous':
            if password1 == password2:
                try:
                    user = User.objects.create_user(username, 
                                                    email, 
                                                    password1)
                    user.save()
                    auth.login(request, user)
                    return redirect('chatbot')
                except:
                    error_message = 'Error creating account'
                    return render(request, 'register.html', {'error_message': error_message})
            else:
                error_message = 'Passwords do not match'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Username cannot be "Anonymous"'
            return render(request, 'register.html', {'error_message': error_message})
    return(render(request, 'register.html'))

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(
            request, 
            username=username, 
            password=password
            )
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    return(render(request, 'login.html'))

def logout(request):
    auth.logout(request)
    return(redirect('login'))