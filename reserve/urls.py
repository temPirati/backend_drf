from django.urls import path, re_path
from .views import ListRoom, RoomDetail, ReservationCreate, ListUsers, ReservationDetail, ReservationDetailData, PostRooms
app_name = 'reserve_api'

urlpatterns = [
    path('<int:pk>', RoomDetail.as_view(), name='detail_create'),
    path('', ListRoom.as_view(), name='list-create'),
    path('create/', PostRooms.as_view(), name='post_rooms'),
    path('reserve/', ReservationCreate.as_view(), name='reservation_create'),
    path('users/', ListUsers.as_view(), name='users'),
    path('reservation/<int:pk>', ReservationDetail.as_view(), name='detail_reservation'),
    path('reservationdata/<int:pk>', ReservationDetailData.as_view(), name='detailData')
    # re_path(r'saveImage$', SaveImage),
    # path('categories/', CategoryList.as_view(), name='categorylist'),
    # path('users/', UserList.as_view(), name='listusercreate'),
    # path('users/<int:pk>', UserDetail.as_view(), name='detailusercreate'),
]
