# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase, TestCase
import mock
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

from models import Allocation, Domain, Interface, Network, Service


class DomainModelTest(TestCase):
    def test_creating_new_domains(self):
        domain = Domain()
        domain.id = 42
        domain.name = "Test VM"
        domain.state = domain.RUNNING
        domain.max_memory = 2*2024*2024
        domain.memory = domain.max_memory
        domain.vcpu = 1
        domain.save()

        all_domains_in_database = Domain.objects.all()
        self.assertEquals(len(all_domains_in_database), 1)
        only_domain_in_database = all_domains_in_database[0]
        self.assertEquals(only_domain_in_database, domain)

        self.assertEquals(only_domain_in_database.name, "Test VM")


class DomainManagerTest(TestCase):
    def setUp(self):
        # Mock a libvirt virDomain object:
        vir_domain = mock.Mock()
        vir_domain.name.return_value = "test_domain"
        vir_domain.ID.return_value = 1
        vir_domain.info.return_value = [1, 2097152, 2097152, 1, 0]
        self.vir_domain = vir_domain

    def test_creating_new_domains(self):
        self.domain = Domain.objects.create(self.vir_domain)

        self.assertEquals(self.domain.name, "test_domain")
        self.assertEquals(self.domain.state, 1)
        self.assertEquals(self.domain.max_memory, 2097152)

    def test_updating_domains(self):
        # Mock an updated libvirt virDomain object:
        vir_domain = self.vir_domain
        vir_domain.info.return_value = [2, 2097152, 2097152, 1, 10]

        updated_domain = Domain.objects.update_or_create(vir_domain)

        self.assertEquals(updated_domain.state, 2)
        self.assertEquals(updated_domain.memory, 2097152)
        self.assertEquals(updated_domain.cpu_time, 10)

    #def test_updating_all_domains(self):
    #    pass


#   class DomainFunctionalTest(LiveServerTestCase):
#       fixtures = ['admin_user.json']

#       def setUp(self):
#           pass


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
