from django.test import TestCase
from imager_images.models import Photo, Album
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User
import factory

# Create your tests here.
class ImagerProfileTestCase(TestCase):
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
