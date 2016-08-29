import factory
from django.test import TestCase

from home.models import DiagnosticService, PrePurchase, ScheduleMaintenance, CarPapers, DiagnosticScan, Appointments
from tests.v1.python.accounts.test_models import UserFactory


class DiagnosticServiceFactory(factory.DjangoModelFactory):
    vehicle = 'Opel'
    location = 'Lagos'
    phone_number = '+41524204242'
    preferred_date = '2016-05-05T00:00:00+01:00'
    time_preference = 'Morning'


    class Meta:
        model = DiagnosticService


class DiagnosticServiceModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='jacinto@jaicnto.com')
        self.diagnosticService = DiagnosticServiceFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.diagnosticService), '{0}, John Doe'.format(self.diagnosticService.id))


class PrePurchaseFactory(factory.DjangoModelFactory):
    vehicle = 'Opel'
    location = 'Lagos'
    phone_number = '+41524204242'
    preferred_date = '2016-05-05T00:00:00+01:00'
    time_preference = 'Morning'


    class Meta:
        model = PrePurchase


class PrePurchaseModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='jacinto@jaicnto.com')
        self.prePurchase = PrePurchaseFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.prePurchase), '{0}, John Doe'.format(self.prePurchase.id))


class ScheduleMaintenanceFactory(factory.DjangoModelFactory):
    vehicle = 'Opel'
    location = 'Lagos'
    phone_number = '+41524204242'
    preferred_date = '2016-05-05T00:00:00+01:00'
    time_preference = 'Morning'
    service_type = 'Full',
    oil_change = True


    class Meta:
        model = ScheduleMaintenance


class ScheduleMaintenanceModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='jacinto@jaicnto.com')
        self.scheduleMaintenance = ScheduleMaintenanceFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.scheduleMaintenance), '{0}, John Doe'.format(self.scheduleMaintenance.id))


class CarPapersFactory(factory.DjangoModelFactory):
    license_plate = '23-23-23'
    phone_number = '+41524204242'


    class Meta:
        model = CarPapers


class CarPapersModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='jacinto@jaicnto.com')
        self.carPapers = CarPapersFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.carPapers), '{0}, John Doe'.format(self.carPapers.id))


class DiagnosticScanFactory(factory.DjangoModelFactory):
    vehicle = 'opel'
    phone_number = '+41524204242'


    class Meta:
        model = DiagnosticScan


class DiagnosticScanModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='jacinto@jaicnto.com')
        self.diagnosticScan = DiagnosticScanFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.diagnosticScan), '{0}, John Doe'.format(self.diagnosticScan.id))


class AppointmentsFactory(factory.DjangoModelFactory):
    appointments_type = 'DiagnosticService'
    location = 'Lagos'
    preferred_date = '2016-05-05T00:00:00+01:00'


    class Meta:
        model = Appointments


class AppointmentsModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='jacinto@jaicnto.com')
        self.appointments = AppointmentsFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.appointments), '{0}, John Doe'.format(self.appointments.id))