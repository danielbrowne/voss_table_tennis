import datetime
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Person, Game


RATINGS_CONSTANT = 32


def index(request):
    return HttpResponse("There is nothing here! Yay!")


def get_ratings(request):
    """
    Return player rankings
    """

    rankings = sorted([(person.rating, person.username) for person in Person.objects.all()], reverse=True)

    return HttpResponse(json.dumps(rankings))


def register(request):
    """
    Add a new user to the database
    """

    data = json.loads(request.body)

    username = data.get('username')

    person = Person(username=username, rating=1500)

    person.save()

    return HttpResponse("{} registered".format(username))


def update_ratings(request):
    """
    Update user rankings based on submitted game details

    Example:
    {"player1": "Geoffrey", "player2": "Daniel", "player1_score": 1, "player2_score": 2}
    """

    data = json.loads(request.body)
    player1 = data.get('player1')
    player2 = data.get('player2')
    p1_score = data.get('player1_score')
    p2_score = data.get('player2_score')

    score_difference = p1_score - p2_score
    if score_difference > 0:
        winner, win_score, loser, lose_score = player1, p1_score, player2, p2_score
    elif score_difference < 0:
        loser, lose_score, winner, win_score = player1, p1_score, player2, p2_score
    else:
        return HttpResponse('Draw! Try harder')

    winner_person = get_object_or_404(Person, username=winner)
    loser_person = get_object_or_404(Person, username=loser)

    win_expected_win_ratio = 1.0 / (1 + 10**((winner_person.rating - loser_person.rating) / 400.0))
    lose_expected_win_ratio = 1 - win_expected_win_ratio
    win_rating_change = RATINGS_CONSTANT * win_expected_win_ratio * win_score
    lose_rating_change = RATINGS_CONSTANT * lose_expected_win_ratio * lose_score

    rating_change = win_rating_change - lose_rating_change

    winner_person.rating += rating_change
    loser_person.rating -= rating_change
    winner_person.save()
    loser_person.save()

    game = Game(
        winner=winner_person, win_score=win_score, loser=loser_person, lose_score=lose_score,
        game_date=datetime.datetime.now())
    game.save()

    return HttpResponse("Ratings updated")
