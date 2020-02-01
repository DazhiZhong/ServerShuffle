from django.shortcuts import render, redirect
from .models import *
from .forms import *
import os
import random
import re
from shutil import copy
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


hashtag = re.compile(r'[^\\](\#[^\s]+)')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# send_mail(
#     'Your webapp Shuffle has started',
#     'it has started on {{time}} please check',
#     'xieewenz@gmail.com',
#     ['xieewenz@gmail.com'],
#     fail_silently=False,
# )
BADGES = ['Primary', 'Secondary', 'Success',
          'Danger', 'Warning', 'Info', 'Light', 'Dark']
# hell no

cur = object()
old_pk = 0
no_cards = False

current_deck = []

def filtercards(hashtag):
    """
    filters cards using hashtag, card.tag stores tags like "#sth #tag #tag"
    """
    hashtag = formalize_tag(hashtag)
    allcards = Card.objects.all()
    ok_cards = []
    for card in allcards:
        if hashtag in card.tags:
            ok_cards.append(card)
    # print(ok_cards)
    return ok_cards

def create_tag_if_none(tag, user=None):
    tag = formalize_tag(tag)
    if len(CardTags.objects.filter(name=tag))==0:
        CardTags.objects.create(name=tag)
    # if len(UserHashTag.objects.filter(name=tag))==0 and user != None:
    #     UTag=UserHashTag()
    #     UTag.name=tag
    #     Utag.user=user
    #     Utag.card.

def makedict(**kwargs):
    # makedict(name='damn') -> {'name':'damn'}
    return kwargs

def deltag(request):
    # print(request.GET)
    return redirect('cards_see')

def card_list(request, tag):
    if request.POST: print(request.POST)
    print(request.GET)
    context = makedict(cards=[])

    cards=filtercards(tag)
    placecards = []
    for  c in cards:
        tags=c.tags.split(' ')
        placecards.append(makedict(title=c.title, txt=c.txt, tags=tags, pk=c.pk))
    
    context['cards']=placecards
    print(context)
    return render(request, "cards/cardlist.html", context)

@login_required
def create(request):
    """
    no form, parse the lines of info
    the POST is like {'0':'sth', '1':'sth'}, text linside the line is 
    formatted like 'title - txt #tag #tag'
    parse through the lines, and manually add them to Cards db
    """
    context={}
    from .generate_random_image import generate
    
    #generate(monochrome=True,output_path=os.path.join(BASE_DIR,'media/testing/randimage.png'))
    #from  stylegan_genimg import generate_img
    #generate_img(path='media/testing/randimage.png')
    #context = makedict(img_path='/media/testing/randimage.png')
    if request.POST:
        # print(request.POST)
        for i in range(1, len(request.POST)):
            if i == 1:
                i = 0
            card = Card()
            usercard = UserCard()
            texts = request.POST[str(i)].split('-')
            # print(texts)
            if len(texts) < 1:
                texts = ['none', 'none']
            elif len(texts) == 1:
                texts.append('none')
            else:
                latter = '-'.join(texts[1:])
                texts = [texts[0], latter]
            hashtags = hashtag.findall(texts[1])
            if len(hashtags) == 0:
                hashtags.append('#default')
            for tag in hashtags:
                create_tag_if_none(tag, user=request.user)
            texts[1] = hashtag.sub('', texts[1])
            card.title = texts[0]
            card.tags = ' '.join(hashtags)
            card.txt = texts[1]
            card.save()
            usercard.title = texts[0]
            usercard.tags = ' '.join(hashtags)
            usercard.txt = texts[1]
            usercard.user = request.user
            usercard.save()

    return render(request, "cards/create.html", context=context)


def tagview(request, tag):
    """
    name = cards_tag
    same to cards_see, but adds tags, if current is not the same tag it will be deferred
    """
    # print(tag)
    tag = '#'+tag

    # print('thetag'+tag)

    cards = filtercards(tag)

    if len(cards)==0:
        # print('deleting because  of len==0')
        delete_tag(tag)
        return redirect('cards_see')
    if tag not in cur.tags:
        # return redirect('cards_see')
        defer_when_tag(tag)
    
    

    if request.POST:
        keys = request.POST.keys()
        if 'defer' in keys:
            # if cur.title == "No Cards":
            #     changecurrent(tag=tag)
            defer_when_tag(tag)
            
        if 'done' in keys:
            finish_with_tag(tag)
        return redirect('cards_tag', tag=tag[1:])
    context = makedict(card=cur, tags=[], current_tag=tag[1:])
    tags = cur.tags.split(' ')
    for tag in tags:
        context['tags'].append(tag[1:])
    # print('=====\n',cur,'\n=====')
    return render(request, "cards/card.html", context=context)


def taglist(request):

    context = makedict(tags=[])
    tags = CardTags.objects.all()
    for tag in tags:
        context['tags'].append(tag.name[1:])
    # print(context)
    return render(request, 'cards/taglist.html', context=context)


def see_card(request):
    """
    name = cards_see
    shows card, POST can have 'defer' or 'done' 
    defer shows another card, done deletes it and shows another
    context includes card, and tags, tags are put in a list
    """
    global cur
    if request.POST:
        keys = request.POST.keys()
        if 'defer' in keys:
            defer_card()
        if 'done' in keys:
            finish_card()
        return redirect('cards_see')
    context = makedict(card=cur, tags=[], current_tag=False)
    tags = cur.tags.split(' ')
    for tag in tags:
        context['tags'].append(tag[1:])

    return render(request, "cards/card.html", context=context)


def create_default_card():
    """
    self explanatory
    """
    global cur, no_cards
    a = Card()
    a.txt = "you have no cards yet!"
    a.title = "No Cards"
    a.tags = '#default'
    a.save()
    create_tag_if_none('#default')
    no_cards = True
    cur = a
    return cur


def defer_card():
    global cur
    objects = Card.objects.all()
    cur = find_dissimilar_object(cur, objects, objects, create_default_card)


def finish_card():
    global cur
    delete_current_object(cur)
    objects = Card.objects.all()
    cur = find_dissimilar_object(cur, objects, objects, create_default_card)


def defer_when_tag(tag):
    global cur
    objects = filtercards(tag)
    all_objects = Card.objects.all()
    cur = find_dissimilar_object(
        cur, objects, all_objects, create_default_card)


def finish_with_tag(tag):
    global cur
    delete_current_object(cur)
    objects = filtercards(tag)
    all_objects = Card.objects.all()
    cur = find_dissimilar_object(cur, objects, all_objects, create_default_card)



def load_object():
    pass


def delete_current_object(cur):
    tag_exists  = False
    card_exists  = False
    try:
        Card.objects.get(pk=cur.pk).delete()
        card_exists = True
    except:
        pass
        # print('======\ndelnotgood\n======')
    if card_exists:
        # print('deleting acrd tags')
        delete_card_tags(cur)

def delete_tag(tag):
    # print(tag)
    tag = formalize_tag(tag)
    tag_exists = False
    try:
        tag_exists = True
        CardTags.objects.get(name=tag).delete()
    except:
        pass
        # print(f'======\nerror when deleting {tag}\n======')


def delete_card_tags(cur):
    # print('delcartag')
    card_tags = cur.tags.split(' ')
    card_tag_num = {}
    # print(card_tags)
    for tag in card_tags:
        # print(tag)
        card_tag_num[tag] = len(filtercards(tag))
    
    # print(card_tag_num.items())
    for tag, num  in card_tag_num.items():
        # print(f'deleting  {tag}')
        if num ==  0:
            delete_tag(tag)


def find_dissimilar_object(cur, object_list, backup_list, final_function):
    list_without_cur = [i for i in object_list if i != cur]
    backup_without_cur = [i for i in backup_list if i != cur]
    return_cur = object()
    if len(list_without_cur) >= 1:
        num = random.randint(0, len(list_without_cur)-1)
        return_cur = list_without_cur[num]
    elif len(backup_without_cur) >= 1:
        num = random.randint(0, len(backup_without_cur)-1)
        return_cur = backup_without_cur[num]
    else:
        return_cur = final_function()
    return return_cur

def view_current_deck(request, tag=None):
    global current_deck
    cur = current_deck[0]
    if tag:
        pass
    else:
        pass
    context = makedict(card=cur, tags=[], current_tag=tag[1:])
    tags = cur.tags.split(' ')
    for tag in tags:
        context['tags'].append(tag[1:])
    return render(request, "cards/viewcurrent.html", context)

def shuffle(l):
    ll = []
    for i in range(len(l)):
        ll.append(l.pop(random.randint(0,len(l)-1)))
    return ll

def loopdeck(l):
    return l[1:]+[l[0]]

def initialize_deck():
    global current_deck
    all_cards = Card.objects.all()
    current_deck = [card for card in all_cards]
    if len(current_deck) == 0:
        current_deck.append(create_default_card())
    # print(current_deck)

def formalize_tag(tag):
    if tag[:1] != '#':
        # print('toliitle')
        tag  = '#'+tag
    else:
        span = re.search(r'#+',tag).span()
        end = span[1]
        tag=tag[end-1:]
    return tag
# load_from_static()

def create_current_deck(tag):
    global current_deck
    all_cards = filtercards(tag)
    current_deck = [card for card in all_cards]
    if len(current_deck) == 0:
        current_deck.append(create_default_card())
    # print(current_deck)

initialize_deck()
defer_card()
