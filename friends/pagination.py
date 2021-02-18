from rest_framework.pagination import PageNumberPagination


class FriendListPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 50
