from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.query import QuerySet

class Pagination:

    def __init__(self):
        self._page = 1
        self._size = 10
        self._max_size = 100
        self._total_pages = 1

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        if value is not None and value.isdigit():
            self._page = int(value)

    @property
    def total_pages(self):
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        if value is not None and isinstance(value, int):
            self._total_pages = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value is not None and value.isdigit():
            value = int(value)
            self._size = min(value, self._max_size)  # Restrict size to max_size

    def paginate_data(self, data):
        # Ensure QuerySet is ordered to avoid UnorderedObjectListWarning
        if isinstance(data, QuerySet) and not data.query.order_by:
            data = data.order_by('id')  # Default ordering by 'id'

        paginator = Paginator(data, self.size)
        self.total_pages = paginator.num_pages

        try:
            paginated_data = paginator.page(self.page)
        except PageNotAnInteger:
            self._page = 1  # Default to first page
            paginated_data = paginator.page(self.page)
        except EmptyPage:
            self._page = self.total_pages  # Default to last page
            paginated_data = paginator.page(self.page)

        return paginated_data
