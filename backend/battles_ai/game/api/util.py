from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def calc_score(request):
    try:
        num_str = request.data.get('num_str')
        language = request.data.get('language')
        if language == 'KO':
            num_str = num_str * 2
        elif language == 'EN':
            num_str = num_str * 1
        score = 100 - (num_str/5000)
        return Response({"score": format(score, '.2f')}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"detail": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)