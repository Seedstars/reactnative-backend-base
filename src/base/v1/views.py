from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from base.v1.serializers import DiagnosticServiceSerializer
import dateutil.parser

from lib.utils import AtomicMixin


class DiagnosticServiceView(AtomicMixin, GenericAPIView):
    serializer_class = DiagnosticServiceSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        """Example authenticated POST"""

        formatted_data = request.data.copy()
        # FIXME PASS ONLY USER OBJECT
        formatted_data['user'] = request.user.id

        serializer = self.serializer_class(data=formatted_data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        
        preferred_date = dateutil.parser.parse(request.data['preferred_date'])
        
        print (request.data)
        
        print (serializer.validated_data)

        msg = "Email: {0}<br/>" \
              "First Name: {1}<br/>" \
              "Last Name: {2}<br/>" \
              "Vehicle: {3}<br/>" \
              "Preferred Date: {4}<br/>" \
              "Time Preference: {5}<br/>".format(request.user.email,
                                                 request.user.first_name,
                                                 request.user.last_name,
                                                 serializer.validated_data['vehicle'],
                                                 preferred_date.strftime('%Y/%m/%d'),
                                                 serializer.validated_data['time_preference'])
                                                 
        print (msg)

        return Response(status=status.HTTP_200_OK)


