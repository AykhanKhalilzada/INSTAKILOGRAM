from django.test import TestCase
from .models import CustomUserModel, FollowUserRelation

class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user1 = CustomUserModel.objects.create(username='alma', email='user1@example.com')
        print(f'User1 created: {self.user1}')
        self.user2 = CustomUserModel.objects.create(username='gilas', email='user2@example.com')
        print(f'User2 created: {self.user2}')
        self.user3 = CustomUserModel.objects.create(username='armud', email='user3@example.com')
        print(f'User3 created: {self.user3}')
        
        self.follow_relation1 = FollowUserRelation.objects.create(follower=self.user1, following=self.user2)
        print(f'Follow Relation 1 created: {self.follow_relation1}')
        self.follow_relation2 = FollowUserRelation.objects.create(follower=self.user1, following=self.user3)
        print(f'Follow Relation 2 created: {self.follow_relation2}')
        self.follow_relation3 = FollowUserRelation.objects.create(follower=self.user2, following=self.user1)
        print(f'Follow Relation 3 created: {self.follow_relation3}')

    def test_get_followers(self):
        followers_user1 = self.user1.get_followers()
        print(f'Followers of User1: {followers_user1}')
        
        self.assertEqual(len(followers_user1), 1)
        self.assertEqual(followers_user1[0], self.user2)

    def test_get_followings(self):
        followings_user1 = self.user1.get_followings()
        print(f'Followings of User1: {followings_user1}')
        
        self.assertEqual(len(followings_user1), 2)
        self.assertIn(self.user2, followings_user1)
        self.assertIn(self.user3, followings_user1)
