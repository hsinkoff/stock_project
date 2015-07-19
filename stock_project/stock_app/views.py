from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    request.session['stocks'] = {}
    request.session['money'] = 100000
    request.session['message'] = ''
    return render(request, 'stock_app/index.html', {'money': request.session['money'], 'message': request.session['message']})

def symbol(request):
    symbol = request.GET['s']
    request.session['sym'] = symbol
    url = 'http://careers-data.benzinga.com/rest/richquote?symbols=%s' % request.session['sym']
    try:
        r = requests.get(url)
        data = r.json()
        request.session['name'] = data['%s' % symbol]['name']
        request.session['bid'] = float(data['%s' % symbol]['bidPrice'])
        request.session['ask'] = float(data['%s' % symbol]['askPrice'])
        request.session['message'] = ''
    except:
        request.session['message'] = "That stock symbol does not exist in our database.  Please choose another stock."
        request.session['sym'] = ''
        request.session['name'] = ''
        request.session['bid'] = ''
        request.session['ask'] = ''
    return render(request, 'stock_app/index.html', {'message': request.session['message'], 'symbol': request.session['sym'], 'name': request.session['name'], 'bid': request.session['bid'], 'ask': request.session['ask'], 'money': request.session['money'], 'stocks': request.session['stocks']})

def buy(request):
    quantity = int(request.GET['q'])
    if 'buy' in request.GET:
        price = request.session['ask'] * quantity
        if price < request.session['money']:
            request.session['money'] = request.session['money'] - price
            if request.session['name'] in request.session['stocks']:
                 request.session['stocks'][request.session['name']]['quantity'] = request.session['stocks'][request.session['name']]['quantity'] + quantity
            else:
                request.session['stocks'][request.session['name']] = {'name': request.session['name'], 'quantity': quantity, 'price': request.session['ask']}
            request.session['message'] = "Stock purchased succesfully."
        elif price > request.session['money']:
            request.session['message'] = "Oops, you don't have enough money to purchase that much stock."
    elif 'sell' in request.GET:
        name = request.session['name']
        if name in request.session['stocks']:
            if request.session['stocks'][name]['quantity'] >= quantity:
                price = request.session['bid'] * quantity
                request.session['stocks'][name]['quantity'] = request.session['stocks'][name]['quantity'] - quantity
                request.session['money'] = request.session['money'] + price
                request.session['message'] = "Congrats. Your stock has sold."
                if request.session['stocks'][name]['quantity'] == 0:
                    del request.session['stocks'][name]
            else:
                request.session['message'] = "You can't sell stock you don't own."
        else:
            request.session['message'] = "You can't sell stock you don't own."
    return render(request, 'stock_app/index.html', {'message': request.session['message'], 'quantity': quantity, 'money': request.session['money'], 'stocks':  request.session['stocks'], 'name': request.session['name'], 'bid': request.session['bid'], 'ask': request.session['ask'], 'symbol': request.session['sym']})
