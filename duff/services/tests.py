# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase, TestCase
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

from duff.libvirt.models import Domain
from models import Allocation, Service


class ServiceModelTest(TestCase):
    def test_creating_new_services(self):
        service = Service()
        service.name = "test"
        service.description = "Test Service"
        service.port = 8080
        service.protocol = Service.HTTP
        service.save()

        all_services_in_database = Service.objects.all()
        self.assertEquals(len(all_services_in_database), 1)
        only_service_in_database = all_services_in_database[0]
        self.assertEquals(only_service_in_database, service)
        
        self.assertEquals(only_service_in_database.name, "test")
        self.assertEquals(only_service_in_database.description, "Test Service")
        self.assertEquals(only_service_in_database.port, 8080)


class AllocationModelTest(TestCase):
    def setUp(self):
        self.domain = Domain.objects.create(name="my_domain")
        self.service = Service.objects.create(name="my_service")

    def test_allocating_a_service_for_a_domain(self):
        allocation = Allocation()
        allocation.domain = self.domain
        allocation.service = self.service
        allocation.port = 8080
        allocation.save()

        all_allocations_in_database = Allocation.objects.all()
        self.assertEquals(len(all_allocations_in_database), 1)
        only_allocation_in_database = all_allocations_in_database[0]
        self.assertEquals(only_allocation_in_database, allocation)
