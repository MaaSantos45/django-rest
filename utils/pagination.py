from django.core.paginator import Paginator
import math
import os

PER_PAGE = int(os.environ.get('PAGINATION_PER_PAGE', 10))
QTD_PAGE = int(os.environ.get('PAGINATION_QTD_PAGE', 10))


def make_pagination_range(page_range, qtd_pages, current_page=1):
    total_pages = len(page_range)
    middle_range = math.ceil(qtd_pages / 2)
    start_range = current_page - middle_range
    end_range = current_page + middle_range

    if start_range < 0:
        start_range_offset = abs(start_range)
        start_range = 0
        end_range += start_range_offset

    if end_range >= total_pages:
        end_range_offset = abs(total_pages - end_range)
        start_range -= end_range_offset

    pagination = page_range[start_range:end_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qtd_pages': qtd_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'end_range': end_range,
    }


def make_pagination(request, queryset, per_page=None, qtd_pages=None):
    if per_page is None:
        per_page = PER_PAGE
    if qtd_pages is None:
        qtd_pages = QTD_PAGE

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)
    pagination_range = make_pagination_range(
        page_range=paginator.page_range,
        qtd_pages=qtd_pages,
        current_page=current_page
    )

    return page_obj, pagination_range
