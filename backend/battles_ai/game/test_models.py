from django.test import TestCase
from .models import Leaderboard

class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            nickname='John',
            score=100.0,
            num_str=5,
            language='en',
            session_id=1
        )

    def test_str_representation(self):
        self.assertEqual(str(self.leaderboard), 'John: 100.000')

    def test_ordering(self):
        leaderboard2 = Leaderboard.objects.create(
            nickname='Jane',
            score=200.0,
            num_str=10,
            language='en',
            session_id=1
        )
        leaderboard3 = Leaderboard.objects.create(
            nickname='Bob',
            score=50.0,
            num_str=3,
            language='en',
            session_id=1
        )
        leaderboard4 = Leaderboard.objects.create(
            nickname='Alice',
            score=150.0,
            num_str=7,
            language='en',
            session_id=1
        )

        leaderboard_list = list(Leaderboard.objects.all())
        self.assertEqual(leaderboard_list, [leaderboard2, leaderboard4, leaderboard, leaderboard3])