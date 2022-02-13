from django.shortcuts import render

# Create your views here.


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    for_index = 'Ответственная за дизайн Ульяна Краморенко, во всем винить её!'

    # Генерация "количеств" некоторых главных объектов
    # num_books=Book.objects.all().count()
    # num_instances=BookInstance.objects.all().count()
    # # Доступные книги (статус = 'a')
    # num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    # num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'for_index': for_index},
    )
