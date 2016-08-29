from rest_framework import status
from rest_framework.test import APITestCase
from django.utils.six import StringIO

from lib.testutils import CustomTestCase

from home.v1.serializers import DiagnosticServiceSerializer, PrePurchaseSerializer, ScheduleMaintenanceSerializer, \
    CarPapersSerializer, DiagnosticScanSerializer, OneSignalSerializer


class DiagnosticServiceSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
                'location': 'Lagos',
                'phone_number ': '+41524204242',
                'preferred_date': '2016-05-05T00:00:00+01:00',
                'time_preference': 'night',
            },
            'error': ('time_preference', ['"night" is not a valid choice.']),
            'label': 'Invalid DiagnosticService.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'vehicle': 'Opel',
            'location': 'Lagos',
            'phone_number ': '+41524204242',
            'preferred_date': '2016-05-05T00:00:00+01:00',
            'time_preference': 'Morning',
        },
    ]

    def setUp(self):
        self.required_fields = ['vehicle', 'location','user', 'phone_number']
        self.not_required_fields = [
            'id', 'preferred_date', 'time_preference'
        ]

    def test_fields(self):
        serializer = DiagnosticServiceSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = DiagnosticServiceSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = DiagnosticServiceSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class PrePurchaseSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
                'location': 'Lagos',
                'phone_number ': '+41524204242',
                'preferred_date': '2016-05-05T00:00:00+01:00',
                'time_preference': 'night',
            },
            'error': ('time_preference', ['"night" is not a valid choice.']),
            'label': 'Invalid PrePurchase.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'vehicle': 'Opel',
            'location': 'Lagos',
            'phone_number ': '+41524204242',
            'preferred_date': '2016-05-05T00:00:00+01:00',
            'time_preference': 'Morning',
        },
    ]

    def setUp(self):
        self.required_fields = ['vehicle', 'location','user', 'phone_number']
        self.not_required_fields = [
            'id','preferred_date', 'time_preference'
        ]

    def test_fields(self):
        serializer = PrePurchaseSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = PrePurchaseSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = PrePurchaseSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class ScheduleMaintenanceSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
                'location': 'Lagos',
                'phone_number ': '+41524204242',
                'preferred_date': '2016-05-05T00:00:00+01:00',
                'time_preference': 'night',
            },
            'error': ('time_preference', ['"night" is not a valid choice.']),
            'label': 'Invalid ScheduleMaintenance.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'vehicle': 'Opel',
            'location': 'Lagos',
            'phone_number ': '+41524204242',
            'preferred_date': '2016-05-05T00:00:00+01:00',
            'time_preference': 'Morning',
        },
    ]

    def setUp(self):
        self.required_fields = ['vehicle', 'location', 'user', 'phone_number']
        self.not_required_fields = [
            'id', 'service_type', 'oil_change',
            'preferred_date', 'time_preference'
        ]

    def test_fields(self):
        serializer = ScheduleMaintenanceSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = ScheduleMaintenanceSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = ScheduleMaintenanceSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class CarPapersSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
                'phone_number': '+41524204242344354334234234324234324324234',
                'license_plate': '23-23-23',
            },
            'error': ('phone_number', ['Ensure this field has no more than 16 characters.']),
            'label': 'Invalid CarPapers.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'license_plate': '23-23-23',
            'phone_number ': '+41524204242',
        },
    ]

    def setUp(self):
        self.required_fields = ['license_plate', 'user', 'phone_number']
        self.not_required_fields = ['id']

    def test_fields(self):
        serializer = CarPapersSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = CarPapersSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = CarPapersSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class DiagnosticScanSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
                'phone_number': '+41524204242344354334234234324234324324234',
                'vehicle': 'opel',
            },
            'error': ('phone_number', ['Ensure this field has no more than 16 characters.']),
            'label': 'Invalid DiagnosticScan.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'vehcile': 'Opel',
            'phone_number ': '+41524204242',
        },
    ]

    def setUp(self):
        self.required_fields = ['vehicle', 'user', 'phone_number']
        self.not_required_fields = ['id']

    def test_fields(self):
        serializer = DiagnosticScanSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = DiagnosticScanSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = DiagnosticScanSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)

class OneSignalSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
            },
            'error': ('one_signal_id', ['This field is required.']),
            'label': 'Invalid OneSignal.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'one_signal_id': 'adgeax'
        },
    ]

    def setUp(self):
        self.required_fields = ['one_signal_id']
        self.not_required_fields = []

    def test_fields(self):
        serializer = OneSignalSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = OneSignalSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = OneSignalSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)
