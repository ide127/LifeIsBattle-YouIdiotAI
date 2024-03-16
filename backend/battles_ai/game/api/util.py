from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='post',
    operation_description= \
        """
        This endpoint calculates the score based on the number of characters in the input string.
        The score is calculated as 100 - (num_str/10000).
        If the language is Korean, the input string is doubled before the score is calculated.
        
        **Request Example**:
        ```json
        {
            "num_str": "2581",
            "language": "KO"
        }
        ```
        - **num_str** : the number of characters.
        - **language** : Language code of the user. Defaults to 'EN'.
        
        
        **Return Example**:
        ```json
        {
            "score": "78.79"
        }
        ```
        
        """,
    responses={200: 'OK.',
               400: 'Invalid input.'},
)
@api_view(['POST'])
def calc_score(request):
    try:
        num_str = request.data.get('num_str')
        language = request.data.get('language')
        if language == 'ko':
            num_str = num_str * 2
        elif language == 'en':
            num_str = num_str * 1
        score = 100 - (num_str/10000)
        return Response({"score": format(score, '.2f')}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"detail": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)