from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from networks.models import Network

from base_groups.models import GroupMember, GroupMemberRecord

class TestAddCreatorToNetwork(TestCase):
    """
    Regression test for https://cotonou.ewb.ca/fastrac/myewb2/ticket/390.
    Network creator is not added to newtork as admin.
    """

    def test_add_creator_to_network(self):
        u = User.objects.create_user('creator', 'c@ewb.ca', 'password')
        net = Network.objects.create(slug='new-net', name='new-net', creator=u)
        self.assertTrue(net.user_is_member(u))
        self.assertTrue(net.user_is_admin(u))

class TestNetworkMembershipDeletion(TestCase):
    """
    Testing the ability for users to be removed from groups, by themselves or others.
    """

    def setUp(self):
        self.admin = User.objects.create_user(username='creator', email='c@ewb.ca', password='password')
        self.user = User.objects.create_user(username='user', email='user@ewb.ca', password='password')

        self.bg = Network.objects.create(slug='bg', name='generic network', creator=self.admin)
        self.gm = GroupMember.objects.create(user=self.user, group=self.bg)

    def tearDown(self):
        GroupMemberRecord.objects.all().delete()
        GroupMember.objects.all().delete()
        Network.objects.all().delete()
        User.objects.all().delete()

    def test_admin_member_removal(self):
        """
        Group admin can remove a member.
        """
        c = Client()
        response = c.post('/account/login/', {'login_name': 'creator', 'password': 'password'})
        response = c.get('/networks/bg/members/user/delete/')
        self.assertContains(response, "Are you sure you want to remove user@... from generic network?")

        response = c.post('/networks/bg/members/user/delete/')
        self.assertEqual(0, GroupMember.objects.filter(user=self.user, group=self.bg).count())

        c.logout()

    def test_self_member_removal(self):
        """
        Member can end own membership.
        """
        c = Client()
        response = c.post('/account/login/', {'login_name': 'user', 'password': 'password'})
        response = c.get('/networks/bg/members/user/delete/')
        self.assertContains(response, "Are you sure you want to leave generic network?")

        response = c.post('/networks/bg/members/user/delete/')
        self.assertEqual(0, GroupMember.objects.filter(user=self.user, group=self.bg).count())

        c.logout()

    def test_third_party_member_removal(self):
        """
        A user that is not a group admin cannot end another user's membership.
        """
        c = Client()
        response = c.post('/account/login/', {'login_name': 'user', 'password': 'password'})
        response = c.get('/networks/bg/members/creator/delete/')
        self.assertNotContains(response, "Are you sure you want to remove c@... from generic network?")

        response = c.post('/networks/bg/members/creator/delete/')
        self.assertEqual(1, GroupMember.objects.filter(user=self.admin, group=self.bg).count())
        
        c.logout()
        
    def test_anon_member_removal(self):
        """
        An anonymous user cannot end another user's membership.
        """
        c = Client()
        response = c.get('/networks/bg/members/creator/delete/')
        self.assertNotContains(response, "Are you sure you want to remove c@... from generic network?", status_code=302)

        response = c.post('/networks/bg/members/creator/delete/')
        self.assertEqual(1, GroupMember.objects.filter(user=self.admin, group=self.bg).count())
