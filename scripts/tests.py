# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from scripts.models import Scripts, Tag
from django.shortcuts import render,render_to_response, redirect,get_object_or_404
from django.contrib.auth.models import User

# Create your tests here.
def create_script(title, contents, user):
	return Kid.objects.create(title=title, contents=contents, user=user)	


def create_user(username, email, first_name, last_name, pass1):
	return User.objects.create(username=username, email=email, 
		first_name=first_name, last_name=last_name,
		password=pass1)


# user test case
class UserUrlTestCase(TestCase):
	def test_login(self):
		response = self.client.get('/scripts/login')
		self.assertEqual(response.status_code, 301)


	def test_logout(self):
		response = self.client.get('/scripts/logout')
		self.assertEqual(response.status_code, 301)


	def test_register(self):
		response = self.client.get('/scripts/register')
		self.assertEqual(response.status_code, 301)


	def test_adminpage(self):
		response = self.client.get('/admin')
		self.assertEqual(response.status_code, 301)


# class ScriptTestCase(TestCase):
# 	def setUp(self):
# 		create_category("cat1")
# 		create_category_sub("cat2", "cat1")
		

# 	def test_create_kid(self):
# 		create_kid("test","cat2")
# 		kid_object = get_object_or_404(Kid, title="test")
# 		self.assertEqual(kid_object.title, "test")