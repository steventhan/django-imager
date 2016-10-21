from imager_images.models import Photo
from rest_framework import viewsets, response
from imager_api.serializers import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def list(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(user=request.user)
        serializer = PhotoSerializer(queryset, many=True)
        return response.Response(serializer.data)
