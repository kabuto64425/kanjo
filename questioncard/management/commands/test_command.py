from datetime import datetime, date
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from app.models import Item
from deck.models import Deck

from rest_framework.exceptions import ValidationError

from questioncard.models import QuestionCard

class Command(BaseCommand):
    help = "テストコマンド"

    @transaction.atomic
    def handle(self, *args, **options):
        questionCard1 = QuestionCard.objects.get(pk=1)
        questionCard2 = QuestionCard.objects.get(pk=3)

        deck1 = Deck.objects.get(pk=questionCard1.in_deck.pk)
        deck2 = Deck.objects.get(pk=questionCard2.in_deck.pk)  
        
        if deck1 != deck2:
            raise ValidationError("順序を入れ替えようとしているそれぞれの所有デッキが異なります")

        print("hello_world")