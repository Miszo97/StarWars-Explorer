from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from starwars_data.serializers import CollectionSerializer
from rest_framework import generics


from starwars_data.models import Collection
from starwars_data.tasks import generate_collection_task
from django.http import HttpResponse




class GenerateCollectionView(APIView):
    def post(self, request):
        generate_collection_task.delay()
        return Response("all good")



class CollectionView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class CollectionDetailView(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)

        response = HttpResponse(content_type='text/csv')

        with open(f"collections/{collection.file_name}", "rb") as file:
            file_content = file.read()

        response = HttpResponse(file_content, content_type='text/csv')

        return response



    

