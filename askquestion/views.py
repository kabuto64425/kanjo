from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import TemplateView
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from questioncard.models import QuestionCard
from deck.models import Deck


TOP_QUESTION_NUMBER = -1
BOTTOM_QUESTION_NUMBER = 2 ** 60

class JumpButtonInfo:
    def __init__(self, url = None, text = None, is_secondary = False):
        self.url = url
        self.text = text
        self.is_secondary = is_secondary

def build_jump_button_infos(deck_pk, question_cards, question_number):
    jump_button_infos = []

    jump_button_info = JumpButtonInfo()
    jump_button_info.url = reverse('ask_question_top', kwargs={'deck_pk': deck_pk})
    jump_button_info.text = "top"
    if question_number == TOP_QUESTION_NUMBER : jump_button_info.is_secondary = True
    jump_button_infos.append(jump_button_info)
    
    for i, _ in enumerate(question_cards, start = 1):
        jump_button_info = JumpButtonInfo()
        jump_button_info.url = reverse('ask_question', kwargs={'deck_pk': deck_pk, 'number': i})
        jump_button_info.text = f"{i}"
        if i == question_number : jump_button_info.is_secondary = True
        jump_button_infos.append(jump_button_info)
    
    jump_button_info = JumpButtonInfo()
    jump_button_info.url = reverse('ask_question_bottom', kwargs={'deck_pk': deck_pk})
    jump_button_info.text = "btm"
    if question_number == BOTTOM_QUESTION_NUMBER : jump_button_info.is_secondary = True
    jump_button_infos.append(jump_button_info)
    return jump_button_infos

class TopView(TemplateView):

    template_name = "askquestion/top.html"

    # アクセス権がないユーザーのアクセスを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if deck.public_flag or self.request.user == deck.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        question_cards = QuestionCard.objects.filter(in_deck=deck).order_by('order')

        kwargs["owner"] = deck.owner
        kwargs["dek_name"] = deck.deck_name

        kwargs["question_number"] = None

        kwargs["next_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': 1})
        kwargs["prev_url"] = None

        jump_button_infos = build_jump_button_infos(self.kwargs.get('deck_pk'), question_cards, TOP_QUESTION_NUMBER)
        kwargs["jump_button_infos"] = jump_button_infos

        return super().get_context_data(**kwargs)

class AskQuestionView(TemplateView):

    template_name = "askquestion/ask_question.html"

    # アクセス権がないユーザーのアクセスを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if deck.public_flag or self.request.user == deck.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        question_cards = QuestionCard.objects.filter(in_deck=deck).order_by('order')
        
        kwargs["owner"] = deck.owner
        kwargs["questioncard"] = question_cards[self.kwargs.get('number') - 1]

        kwargs["question_number"] = self.kwargs.get('number')

        kwargs["next_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': self.kwargs.get('number') + 1}) if self.kwargs.get('number') < len(question_cards) else reverse('ask_question_bottom', kwargs={'deck_pk': self.kwargs.get('deck_pk')})
        kwargs["prev_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': self.kwargs.get('number') - 1}) if self.kwargs.get('number') > 1 else reverse('ask_question_top', kwargs={'deck_pk': self.kwargs.get('deck_pk')})

        jump_button_infos = build_jump_button_infos(self.kwargs.get('deck_pk'), question_cards, kwargs["question_number"])
        kwargs["jump_button_infos"] = jump_button_infos

        return super().get_context_data(**kwargs)
    
class BottomView(TemplateView):

    template_name = "askquestion/bottom.html"

    # アクセス権がないユーザーのアクセスを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if deck.public_flag or self.request.user == deck.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        question_cards = QuestionCard.objects.filter(in_deck=deck).order_by('order')

        kwargs["owner"] = deck.owner
        kwargs["dek_name"] = deck.deck_name

        kwargs["question_number"] = None

        kwargs["next_url"] = None
        kwargs["prev_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': len(question_cards)})

        jump_button_infos = build_jump_button_infos(self.kwargs.get('deck_pk'), question_cards, BOTTOM_QUESTION_NUMBER)
        kwargs["jump_button_infos"] = jump_button_infos

        return super().get_context_data(**kwargs)