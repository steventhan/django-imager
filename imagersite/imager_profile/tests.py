from django.test import TestCase, Client
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User
from django.urls import reverse


class ImagerProfileTestCase(TestCase):
    """Tests for ImagerProfile"""
    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()

    def teardown(self):
        self.user.delete()

    def test_user_saved_properly(self):
        User(username='test_user2').save()
        test_u = User.objects.filter(username='test_user').first()
        num_user = User.objects.count()
        self.assertTrue(test_u.username, 'test_user')
        self.assertTrue(num_user, 2)

    def test_imagerprofile_auto_created_with_new_user(self):
        self.assertTrue(self.user.imagerprofile, None)

    def test_new_imagerprofile_saved_when_new_user_is_saved(self):
        pre_save_num_profile = ImagerProfile.objects.count()
        User(username='random_user').save()
        post_save_num_profile = ImagerProfile.objects.count()
        self.assertTrue(post_save_num_profile, pre_save_num_profile + 1)

    def test_no_imager_profile_created_when_existing_user_is_saved(self):
        pre_save_num_profile = ImagerProfile.objects.count()
        test_u = User.objects.filter(username='test_user').first()
        test_u.email = 'something@example.com'
        test_u.save()
        post_save_num_profile = ImagerProfile.objects.count()
        self.assertTrue(post_save_num_profile, pre_save_num_profile)

    def test_profile_saved_properly(self):
        self.user.imagerprofile.address_1 = '100 1st st'
        self.user.imagerprofile.address_2 = 'ste 200'
        self.user.imagerprofile.city = 'Seattle'
        self.user.imagerprofile.state = 'WA'
        self.user.imagerprofile.zipcode = '98101'
        self.user.imagerprofile.save()
        fetch_from_db = User.objects.filter(username='test_user').first()
        self.assertTrue(fetch_from_db.imagerprofile.zipcode, '98101')
        self.assertTrue(fetch_from_db.imagerprofile.state, 'WA')
        self.assertTrue(fetch_from_db.imagerprofile.city, 'Seattle')
        self.assertTrue(fetch_from_db.imagerprofile.address_2, 'ste 200')
        self.assertTrue(fetch_from_db.imagerprofile.address_1, '100 1st st')


class ProfileView(TestCase):
    """Test case for profile view."""
    def setUp(self):
        self.response = self.client.get(reverse('my_profile'), follow=True)
        self.c = Client()
        self.user = User(username='test_user')
        self.user.save()
        self.c.force_login(user=self.user)
        self.logged_in_response = self.c.get(reverse('my_profile'))

    def tearDown(self):
        self.user.delete()

    def test_view_redirect_when_not_logged_in(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertContains(self.response, 'Login:')

    def test_view_when_logged_in(self):
        self.assertContains(self.logged_in_response, 'My Imager profile')

    def test_correct_template_for_my_profile(self):
        self.assertTemplateUsed(
            self.logged_in_response, 'imager_profile/my_profile.html'
        )


class RegistrationView(TestCase):
    """Test case for registration view."""
    def setUp(self):
        self.response = self.client.get(reverse('auth_login'))
        self.signup_res = self.client.get(reverse('registration_register'))
        self.c = Client()
        self.user = User(username='test_user')
        self.user.save()
        self.c.force_login(user=self.user)
        self.logged_in_response = self.c.get(reverse('my_profile'))

    def tearDown(self):
        self.user.delete()

    def test_login_view_not_logged_in(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertContains(self.response, 'Login:')

    def test_correct_template_login_view(self):
        self.assertTemplateUsed(
            self.response, 'registration/login.html'
        )

    def test_register_view_not_logged_in(self):
        self.assertEquals(self.signup_res.status_code, 200)
        self.assertContains(self.signup_res, '150 characters or fewer.')

    def test_correct_template_register_view(self):
        self.assertTemplateUsed(
            self.signup_res, 'registration/registration_form.html'
        )

    def test_login_view_redirect_when_logged_in(self):
        login_res = self.c.get(reverse('auth_login'))
        self.assertEquals(login_res.status_code, 302)

    def test_register_view_redirect_when_logged_in(self):
        register_res = self.c.get(reverse('registration_register'))
        self.assertEquals(register_res.status_code, 302)
