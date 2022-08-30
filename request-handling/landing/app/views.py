from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter({'original': 0, 'test': 0})
counter_click = Counter({'original': 0, 'test': 0})
landings = {
    'original': 'landing.html',
    'test': 'landing_alternate.html'
}

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    landing_ab = request.GET.get('from-landing')
    counter_click[landing_ab] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    landing_ab = request.GET.get('from-landing', 'landing.html')

    # Так же реализуйте логику подсчета количества показов
    counter_show[landing_ab] += 1
    return render(request, landings[landing_ab])


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    return render(request, 'stats.html', context={
        'test_conversion': counter_click['test'] / counter_show['test'],
        'original_conversion': counter_click['original'] / counter_show['original'],
    })
