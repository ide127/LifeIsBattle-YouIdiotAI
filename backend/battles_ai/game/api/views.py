from pydoc import cli
from rest_framework import viewsets, status
from django.conf import settings
import requests
from rest_framework.response import Response
from game.models import ChatSession, Message, Leaderboard
from game.serializers import ChatSessionSerializer, MessageSerializer, LeaderboardSerializer
from django.http import request
from battles_ai.openAIAPI import SingletonOpenAI, get_ai_response
from game.api.util import calc_score
from drf_yasg.utils import swagger_auto_schema



class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    
    @swagger_auto_schema(request_body=ChatSessionSerializer)
    def create(self, request):
        """
        This is an example API that allows you to create a user.
        """
        client = SingletonOpenAI.get_instance()
        thread = client.beta.threads.create()
        user_ip = request.META.get('REMOTE_ADDR')
        language = request.data.get('language', 'EN')
        session = ChatSession.objects.create(
            OpenAI_thread_id=thread.id,
            user_ip=user_ip,
            user_language=language
        )
        serializer = self.get_serializer(session)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=self.get_success_headers(serializer.data)
        )
    
    # Retrieve a session and associated messages
    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()
        messages = Message.objects.filter(session=session)
        session_serializer = self.get_serializer(session)
        messages_serializer = MessageSerializer(messages, many=True)
        return Response({
            "session": session_serializer.data,
            "messages": messages_serializer.data
        })
    

    
class MessageViewSet(viewsets.ModelViewSet):
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        
        session_id = request.data.get('session')
        # Validate session exists
        try:
            session = ChatSession.objects.get(pk=session_id, end_time__isnull=True)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Invalid session or session has ended."}, status=status.HTTP_400_BAD_REQUEST)
        
        OpenAI_thread_id = session.OpenAI_thread_id
        text = request.data.get('text')
        is_user = request.data.get('is_user', True) 

        user_chat_message = Message.objects.create(session=session, text=text, is_user=is_user)
        ai_response = get_ai_response(user_chat_message.text, OpenAI_thread_id).get('value')
        ai_chat_message = Message.objects.create(session=session, text=ai_response, is_user=False)
        serializer = self.get_serializer(ai_chat_message)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )
    
    
    
class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Check for unique nickname
        if Leaderboard.objects.filter(nickname=serializer.validated_data['nickname']).exists():
            return Response(
                {'detail': 'Nickname already in use.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=self.get_success_headers(serializer.data)
        )
