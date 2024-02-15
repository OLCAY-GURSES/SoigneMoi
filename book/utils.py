from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateHospitals(request, hospitals, results):
    page = request.GET.get('page')
    paginator = Paginator(hospitals, results)

    try:
        hospitals = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        hospitals = paginator.page(page)
    except EmptyPage:
        # display last page if page is out of range
        page = paginator.num_pages
        hospitals = paginator.page(page)

    # if there are many pages, we will see some at a time in the pagination bar (range window)
    # leftIndex(left button) = current page no. - 4
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        # if leftIndex is less than 1, we will start from 1
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    # return custom_range, projects, paginator
    return custom_range, hospitals