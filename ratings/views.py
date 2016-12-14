import datetime
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, Http404

from .models import Person, Game


RATINGS_CONSTANT = 200


def index(request):
    return HttpResponse("There is nothing here! Yay!")


def register(request):

    data = json.loads(request.body)

    username = data.get('username')

    person = Person(username=username, rating=1000)

    person.save()

    return HttpResponse("{} registered".format(username))


def update_ratings(request):
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

    ratings_difference = abs(winner_person.rating - loser_person.rating) / 50
    expected_win_ratio = 1 - (0.9 / (ratings_difference + 1)**2)

    ratings_change = RATINGS_CONSTANT * expected_win_ratio * abs(score_difference)
    winner_person.rating += ratings_change
    loser_person.rating -= ratings_change
    winner_person.save()
    loser_person.save()

    game = Game(
        winner=winner_person, win_score=win_score, loser=loser_person, lose_score=lose_score,
        game_date=datetime.datetime.now())
    game.save()

    return HttpResponse("Ratings updated")
