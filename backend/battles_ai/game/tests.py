import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(PROJECT_ROOT, '..')))

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "battles_ai.settings")
django.setup()

import random
import string
from django.utils import timezone
from game.models import Leaderboard, ChatSession
from decimal import Decimal

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_leaderboard_entries(num_entries):
    sessions = ChatSession.objects.all()
    for _ in range(num_entries):
        nickname = generate_random_string(random.randint(5, 15))
        score = Decimal(random.uniform(0, 1000)).quantize(Decimal('0.000'))
        num_str = random.randint(1, 10000)
        language = random.choice(['en', 'ko'])
        session = random.choice(sessions)
        leaderboard_entry = Leaderboard(
            nickname=nickname,
            score=score,
            num_str=num_str,
            language=language,
            session=session,
            timestamp=timezone.now()
        )
        leaderboard_entry.save()

if __name__ == '__main__':
    generate_leaderboard_entries(100)  # Generate 100 dummy entries