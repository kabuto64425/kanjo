from datetime import datetime, date
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from app.models import Item

from questioncard.models import QuestionCard

class Command(BaseCommand):
    help = "テストコマンド"

    @transaction.atomic
    def handle(self, *args, **options):
        cards = QuestionCard.objects.all().filter(in_deck = 3).order_by('order')
        for index, cards in enumerate(cards):
            cards.order = index + 1
            cards.save()