# import random
#
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from django.db.models import Q
#
# import requests
# # import base64
#
# from .serializers import *
#
#
# def get_valid_ticket(request):
#     if (token := request.data.get('token')) is None:
#         return {
#             'status': status.HTTP_400_BAD_REQUEST,
#             # 'message': "Field 'token' is not provided"
#             'message': "Exposition is private, but field 'token' is not provided"
#         }
#
#     try:
#         ticket = Ticket.objects.get(token=token)
#     except:
#         return {
#             'status': status.HTTP_403_FORBIDDEN,
#             # 'message': "Your token is invalid"
#             'message': "There is no ticket with this token"
#         }
#
#     if ticket.is_alive:
#         return ticket
#     else:
#         return {
#             'status': status.HTTP_403_FORBIDDEN,
#             'message': "Your ticket is expired"
#         }
#
#
# class ExpositionView(APIView):
#     """
#     Returns exposition information
#     """
#
#     def post(self, request):
#
#         if (exposition_type := request.data.get('exposition_type')) is None:
#             return Response({
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': "Field 'exposition_type' is not provided"
#             })
#
#         if exposition_type == 'Свободный вход':
#             if (exposition_pk := request.data.get('exposition_pk')) is None:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': "Field 'exposition_pk' is not provided"
#                 })
#             exposition = Exposition.objects.get(pk=exposition_pk)
#             if exposition.type != exposition_type:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': "Field 'exposition_type' has value 'Свободный вход', but exposition type is 'По билетам'"
#                 })
#             exposition = ExpositionSerializer(exposition, context={'request': request}).data
#             return Response({
#                 'exposition': exposition
#             })
#         elif exposition_type == 'По билетам':
#             ticket = get_valid_ticket(request)
#             if type(ticket) is dict:  # if dict then error
#                 return Response(ticket)
#             exposition = ExpositionSerializer(ticket.exposition, context={'request': request}).data
#             return Response({
#                 'exposition': exposition,
#                 'ticket_remaining_lifetime': ticket.remaining_lifetime
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': "Field 'exposition_type' value must be 'Свободный вход' or 'По билетам'"
#             })
#
#
# class UIDView(APIView):
#     """
#     Returns room or artifact information by 'uid'
#     """
#
#     def post(self, request):
#
#         if (uid := request.data.get('uid')) is None:
#             return Response({
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': "Field 'uid' is not provided"
#             })
#
#         if Room.objects.filter(uid=uid).exists():
#             room = Room.objects.get(uid=uid)
#             if room.exposition.type == 'По билетам':
#                 ticket = get_valid_ticket(request)
#                 if type(ticket) is dict:  # if dict then error
#                     # if ticket['status'] == 400:
#                     #     ticket['message'] = "Exposition is private, field 'token' is not provided"
#                     #     return Response(ticket)
#                     return Response(ticket)
#             room = RoomSerializer(room, context={'request': request}).data
#             return Response(room)
#         elif Artifact.objects.filter(uid=uid).exists():
#             artifact = Artifact.objects.get(uid=uid)
#             if artifact.room.exposition.type == 'По билетам':
#                 ticket = get_valid_ticket(request)
#                 if type(ticket) is dict:  # if dict then error
#                     return Response(ticket)
#             artifact = ArtifactSerializer(artifact, context={'request': request}).data
#             return Response(artifact)
#         else:
#             return Response({
#                 'status': status.HTTP_404_NOT_FOUND,
#                 'message': "There is no room or artifact with this 'uid'"
#             })
#
#
# class ICORecognitionView(APIView):
#     """
#     Returns room or artifact information by 'ICO'
#     """
#
#     def post(self, request):
#         ticket = get_valid_ticket(request)
#         if type(ticket) is dict:  # if dict then error
#             return Response(ticket)
#
#         if (img_base64 := request.data.get('img_base64')) is None:
#             return Response({
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': "Field 'img_base64' is not provided"
#             })
#
#         artifacts = Artifact.objects.filter(room__exposition=ticket.exposition)
#         artifacts = ArtifactForRoomSerializer(artifacts, context={'request': request}, many=True).data
#
#         rand_index = random.randrange(1, len(artifacts) + 1)
#
#         return Response({
#             'obj_type': 'artifacts',
#             'index': artifacts[rand_index - 1]['id']
#         })
#         #
#         # index_to_label = {
#         #     0: "Test",
#         #     1: "Medal",
#         #     2: "PC",
#         #     3: "Search",
#         #     4: "Projector",
#         #     5: "Idea",
#         #     6: "Telescope",
#         #     7: "Briefcase",
#         #     8: "Trofy",
#         #     9: "Cap",
#         # }
#         #
#         # predictions = requests.post("http://localhost:5000/predict/", json={"base64_str": img_base64}).json()
#         #
#         # for prediction in predictions:
#         #     print(prediction)
#         # index = predictions.index(max(predictions))
#         #
#         # return Response(index_to_label[index])
#
#
# class RoomView(APIView):
#     """
#     Returns room information
#     """
#
#     def post(self, request, room_pk):
#
#         if Room.objects.filter(pk=room_pk).exists():
#             room = Room.objects.get(pk=room_pk)
#             exposition = room.exposition
#             if room.exposition.type == 'По билетам':
#                 ticket = get_valid_ticket(request)
#                 if type(ticket) is dict:  # if dict then error
#                     return Response(ticket)
#             room = RoomSerializer(room, context={'request': request}).data
#             return Response({
#                 'exposition_id': exposition.id,
#                 'exposition_name': exposition.name,
#                 'exposition_type': exposition.type,
#                 'room': room,
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_404_NOT_FOUND,
#                 'message': "There is no room with this ID"
#             })
#
#
# class ConnectedRoomsView(APIView):
#     """
#     Returns connected rooms
#     """
#
#     def post(self, request, room_pk):
#
#         if Room.objects.filter(pk=room_pk).exists():
#             room = Room.objects.get(pk=room_pk)
#             room_data = RoomForConnectedRoomsSerializer(room, context={'request': request}).data
#
#             if room.exposition.type == 'По билетам':
#                 ticket = get_valid_ticket(request)
#                 if type(ticket) is dict:  # if dict then error
#                     return Response(ticket)
#             connected_rooms = Room.objects.filter(exposition=room.exposition).get(pk=room_pk).connected_rooms
#             connected_rooms = RoomForConnectedRoomsSerializer(connected_rooms, context={'request': request},
#                                                               many=True).data
#
#             return Response({
#                 'exposition_id': room.exposition.id,
#                 'exposition_name': room.exposition.name,
#                 'exposition_type': room.exposition.type,
#                 'room': room_data,
#                 'connected_rooms': connected_rooms
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_404_NOT_FOUND,
#                 'message': "There is no room with this ID"
#             })
#
#
# class ArtifactView(APIView):
#     """
#     Returns artifact information
#     """
#
#     def post(self, request, artifact_pk):
#
#         if Artifact.objects.filter(pk=artifact_pk).exists():
#             artifact = Artifact.objects.get(pk=artifact_pk)
#             exposition = artifact.room.exposition
#             if artifact.room.exposition.type == 'По билетам':
#                 ticket = get_valid_ticket(request)
#                 if type(ticket) is dict:  # if dict then error
#                     return Response(ticket)
#             artifact = ArtifactSerializer(artifact, context={'request': request}).data
#             return Response({
#                 'exposition_id': exposition.id,
#                 'exposition_name': exposition.name,
#                 'exposition_type': exposition.type,
#                 'artifact': artifact,
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_404_NOT_FOUND,
#                 'message': "There is no artifact with this ID"
#             })
#
#
# class MapView(APIView):
#     """
#     Returns rooms to build a map
#     """
#
#     def post(self, request, exposition_pk):
#
#         if Exposition.objects.filter(pk=exposition_pk).exists():
#             exposition = Exposition.objects.get(pk=exposition_pk)
#             if exposition.type == 'По билетам':
#                 ticket = get_valid_ticket(request)
#                 if type(ticket) is dict:  # if dict then error
#                     return Response(ticket)
#             rooms = Room.objects.filter(exposition=exposition)
#             rooms = RoomForMapSerializer(rooms, context={'request': request}, many=True).data
#             return Response(({
#                 'exposition_id': exposition.id,
#                 'exposition_name': exposition.name,
#                 'exposition_type': exposition.type,
#                 'rooms': rooms
#             }))
#         else:
#             return Response({
#                 'status': status.HTTP_404_NOT_FOUND,
#                 'message': "There is no exposition with this ID"
#             })
#
#
# class PrintTicketsView(APIView):
#     """
#     Returns tickets for printing with search by id
#     """
#
#     def post(self, request):
#         if request.user.is_authenticated:
#             if (find_by_letters := request.data.get('find_by_letters')) is None:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': "Field 'find_by_letters' is not provided"
#                 })
#
#             tickets = Ticket.objects.filter(exposition=request.user.exposition).filter(
#                 Q(id__icontains=find_by_letters) |
#                 Q(id__icontains=find_by_letters.capitalize()) |
#                 Q(id__icontains=find_by_letters.lower()) |
#                 Q(id__icontains=find_by_letters.upper()))
#             alive_tickets = tickets
#             for ticket in tickets:
#                 if not ticket.is_alive:
#                     alive_tickets = alive_tickets.exclude(pk=ticket.id)
#             alive_tickets = TicketSerializer(alive_tickets, context={'request': request}, many=True).data
#             return Response({
#                 'exposition_id': request.user.exposition.id,
#                 'exposition_name': request.user.exposition.name,
#                 'exposition_type': request.user.exposition.type,
#                 'alive_tickets': alive_tickets
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_403_FORBIDDEN,
#                 'message': "You are not authenticated"
#             })
#
#
# class PrintRoomsView(APIView):
#     """
#     Returns rooms for printing with search by name
#     """
#
#     def post(self, request):
#         if request.user.is_authenticated:
#             if (find_by_letters := request.data.get('find_by_letters')) is None:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': "Field 'find_by_letters' is not provided"
#                 })
#
#             rooms = Room.objects.filter(exposition=request.user.exposition).filter(
#                 Q(name__icontains=find_by_letters) |
#                 Q(name__icontains=find_by_letters.capitalize()) |
#                 Q(name__icontains=find_by_letters.lower()) |
#                 Q(name__icontains=find_by_letters.upper()))
#             rooms = RoomForConnectedRoomsSerializer(rooms, context={'request': request}, many=True).data
#             return Response({
#                 'exposition_id': request.user.exposition.id,
#                 'exposition_name': request.user.exposition.name,
#                 'exposition_type': request.user.exposition.type,
#                 'rooms': rooms
#             })
#         else:
#             return Response({
#                 'status': status.HTTP_403_FORBIDDEN,
#                 'message': "You are not authenticated"
#             })
#
#
# class PrintArtifactsView(APIView):
#     """
#     Returns artifacts for printing with search by name
#     """
#
#     def post(self, request):
#         if request.user.is_authenticated:
#             if (find_by_letters := request.data.get('find_by_letters')) is None:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': "Field 'find_by_letters' is not provided"
#                 })
#             if (are_icons_exist := request.data.get('are_icons_exist')) is None:
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': "Field 'are_icons_exist' is not provided"
#                 })
#             else:
#                 if are_icons_exist.lower() == 'true':
#                     are_icons_exist = True
#                 elif are_icons_exist.lower() == 'false':
#                     are_icons_exist = False
#                 else:
#                     return Response({
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': "Field 'are_icons_exist' must be 'true' or 'false'"
#                     })
#
#             next_page = 1
#             previous_page = 1
#             artifacts = Artifact.objects.filter(room__exposition=request.user.exposition).filter(
#                 Q(name__icontains=find_by_letters) |
#                 Q(name__icontains=find_by_letters.capitalize()) |
#                 Q(name__icontains=find_by_letters.lower()) |
#                 Q(name__icontains=find_by_letters.upper()))
#
#             if are_icons_exist:
#                 artifacts = artifacts.exclude(recognition_image=None)
#
#             page = request.GET.get('page', 1)
#             paginator = Paginator(artifacts, 9)
#             try:
#                 data = paginator.page(page)
#             except PageNotAnInteger:
#                 data = paginator.page(1)
#             except EmptyPage:
#                 data = paginator.page(paginator.num_pages)
#
#             serializer = ArtifactForRoomSerializer(data, context={'request': request}, many=True)
#
#             if data.has_next():
#                 next_page = data.next_page_number()
#             if data.has_previous():
#                 previous_page = data.previous_page_number()
#
#             return Response({
#                 'exposition_id': request.user.exposition.id,
#                 'exposition_name': request.user.exposition.name,
#                 'exposition_type': request.user.exposition.type,
#                 'artifacts': serializer.data,
#                 'count': paginator.count,
#                 'numpages': paginator.num_pages,
#                 'nextlink': 'api/print/artifacts?page=' + str(next_page),
#                 'prevlink': 'api/print/artifacts?page=' + str(previous_page)
#             })
#
#         else:
#             return Response({
#                 'status': status.HTTP_403_FORBIDDEN,
#                 'message': "You are not authenticated"
#             })
#
# # class PrintArtifactsView1(generics.)
