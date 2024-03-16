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
    
    @swagger_auto_schema(
        operation_description= \
            """
            This creates a new chat session and returns the session ID and OpenAI thread ID.
            Mind it : one user chatting - one chat session - one OpenAI thread.
            So when user start new chat session, you need to create a new chat session first.
            After creating chat session, you get the session ID and OpenAI thread ID as response.
            
            
            **Request Example**:
            ```json
            {
                "user_ip": "127.0.0.1",
                "user_language": "en",
            }
            ```
            - **user_ip** : If you can't get user's IP, you can put '0.0.0.0' as default.
            - **user_language** : Language code of the user. Defaults to 'EN'.
            
            **Return Example**:
            ```json
            {
                "id": "ff67c268-33f2-4f95-af85-0e1abfc62289",
                "OpenAI_thread_id": "thread_6yrt2EbTXSmzrnmGldqrjiMQ",
                "start_time": "2021-08-01T12:00:00Z",
                "end_time": null,
                "is_successful": null,
                "user_ip": "0.0.0.0",
                "user_language": "en"
            }
            ```
            - **start_time** : The time when the chat session is created.
            - **end_time** : The time when the chat session is ended. Defaults to null. You need to change this to the end time when the chat session is ended.
            - **is_successful** : Boolean flag to indicate if the chat session is successful. Defaults to null. You need to change this to True or False when the game result is determined.
            """,
        request_body=MessageSerializer, 
        responses={201: 'Created.',
                   400: 'Invalid session or session has ended.',
                   500: 'Internal server error.'},
    )
    def create(self, request):
        """
        This is an example API that allows you to create a user.
        """
        client = SingletonOpenAI.get_instance()
        thread = client.beta.threads.create()
        user_ip = request.META.get('REMOTE_ADDR')
        language = request.data.get('language', 'en')
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
    
    def patch(self, request, *args, **kwargs):
        session = self.get_object()
        session.end_time = request.data.get('end_time')
        session.is_successful = request.data.get('is_successful')
        session.save()
        return Response(status=status.HTTP_200_OK)
    

    
class MessageViewSet(viewsets.ModelViewSet):
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @swagger_auto_schema(
        operation_description= \
            """
            This creates a new message and returns a AI generated message.
            Before making a new message, you need to create a chat session first.
            
            **Request Example**:
            ```json
            {
                "text": "Who are you?",
                "is_user": True,
                "session": "ff67c268-33f2-4f95-af85-0e1abfc62289"
            }
            ```
            - **text** : The message text generated by user.
            - **is_user** : Boolean flag to indicate if the message is from the user. Defaults to True.
            - **session** : ID of the chat session you want to add this message to.
            
            **Return Example**:
            ```json
            {
                "id": "49fcbfbe-11ed-4708-9c2e-776a075d5c7b",
                "text": "I am an AI created by OpenAI. I am here to help you.",
                "is_user": false,
                "session": "ff67c268-33f2-4f95-af85-0e1abfc62289"
            }
            ```
            - **text** : The answer message text generated by AI.
            - **is_user** : Boolean flag to indicate if the message is from the user. Defaults to False.
            - **session** : ID of the chat session this message being added to.
            """,
        request_body=MessageSerializer, 
        responses={201: 'Created and AI response generated.',
                   400: 'Invalid session or session has ended.',
                   500: 'Internal server error.'},
    )
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
    
    @swagger_auto_schema(
        operation_description= \
            """
            This returns the dec leaderboard records with pagination.
            Let's say there are 10 scores, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1].
            If you set the limit to 3, the first page will return [10, 9, 8].
            However if you set the offset to 1 with the limit value, the first page will return [9, 8, 7].
            """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description= \
            """
            This creates a new leaderboard record and returns the leaderboard entry.
            
            **Request Example**:
            ```json
            {
                "nickname": "Gonglee_4",
                "score": "92.71",
                "num_str": 456,
                "language": "en",
                "session": "ff67c268-33f2-4f95-af85-0e1abfc62289"
            }
            ```
            - **nickname** : The nickname of the user. The server will check if the nickname is unique when receiving the request.
            - **score** : The score of the user. It is a decimal number with 5 decimal places. You can get the score by calling the calc_score API.
            - **num_str** : The number of strings the user has sent in the chat session.
            - **language** : The language code of the user. Defaults to 'EN'.
            - **session** : The ID of the chat session the record is associated with.
            
            **Return Example**:
            ```json
            {
                "id": "fc45edbe-11ed-4708-9c2e-776a075d5c7b",
                "nickname": "Gonglee_4",
                "score": "92.71",
                "num_str": 456,
                "language": "en",
                "timestamp": "2021-08-01T12:00:00Z",
                "session": "ff67c268-33f2-4f95-af85-0e1abfc62289"
            }
            ```
            """,
        request_body=MessageSerializer, 
        responses={201: 'Created.',
                   400: 'Invalid session or session has ended.',
                   500: 'Internal server error.'},
    )
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