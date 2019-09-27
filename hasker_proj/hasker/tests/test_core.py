from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Question
from ..forms import UserForm, QuestionForm


class TestVotable(TestCase):

    def setUp(self):
        self.u1 = get_user_model()(username='u1', password='somepassword',
                                   email='dummy@dummy.com')
        self.u1.save()
        self.u2 = get_user_model()(username='u2', password='somepassword',
                                   email='dummy@dummy.com')
        self.u2.save()
        self.q = Question(title='test q', content='test', author=self.u1)
        self.q.save()

    def test_votes_one(self):
        self.q.up_votes.add(self.u1)
        self.q.save()
        self.assertEqual(self.q.votes, 1)

    def test_votes_many(self):
        self.q.up_votes.add(self.u1)
        self.q.up_votes.add(self.u2)
        self.q.save()
        self.assertEqual(self.q.votes, 2)

    def test_votes_zero(self):
        self.q.up_votes.add(self.u1)
        self.q.down_votes.add(self.u2)
        self.q.save()
        self.assertEqual(self.q.votes, 0)

    def test_votes_negative(self):
        self.q.down_votes.add(self.u2)
        self.q.save()
        self.assertEqual(self.q.votes, -1)

    def test_user_ups(self):
        self.q.up_votes.add(self.u1)
        self.q.save()
        self.assertEqual(self.q.user_ups(self.u1), 1)
        self.assertEqual(self.q.user_downs(self.u1), 0)

    def test_user_downs(self):
        self.q.down_votes.add(self.u1)
        self.q.save()
        self.assertEqual(self.q.user_ups(self.u1), 0)
        self.assertEqual(self.q.user_downs(self.u1), 1)

    def test_votes_mixed(self):
        self.q.up_votes.add(self.u1)
        self.q.down_votes.add(self.u2)
        self.q.save()
        self.assertEqual(self.q.user_ups(self.u1), 1)
        self.assertEqual(self.q.user_ups(self.u2), 0)
        self.assertEqual(self.q.user_downs(self.u1), 0)
        self.assertEqual(self.q.user_downs(self.u2), 1)

    def test_handle_votes(self):
        self.q.handle_new_vote(self.u2, 'up')
        self.assertEqual(self.q.votes, 1)
        self.q.handle_new_vote(self.u1, 'up')
        self.assertEqual(self.q.votes, 1)
        self.q.handle_new_vote(self.u2, 'down')
        self.assertEqual(self.q.votes, 0)
        self.q.handle_new_vote(self.u2, 'up')
        self.assertEqual(self.q.votes, 1)


class TestQuestionSearch(TestCase):

    def setUp(self):
        self.u1 = get_user_model()(username='u1', password='somepassword',
                                   email='dummy@dummy.com')
        self.u1.save()
        self.qs = [
            Question(title='test q zero', content='test', author=self.u1),
            Question(title='blatest q', content='blablatest', author=self.u1),
            Question(title='111', content='1231231231231231', author=self.u1),
        ]
        for q in self.qs:
            q.save()

    def test_title_match(self):
        ms = Question.search('zero')
        self.assertEqual(len(ms), 1)
        self.assertTrue(ms[0].title == 'test q zero')

    def test_title_content_match(self):
        ms = Question.search('test')
        self.assertEqual(len(ms), 2)

    def test_no_match(self):
        ms = Question.search('crazy')
        self.assertEqual(len(ms), 0)

    def test_all_match(self):
        ms = Question.search('')
        self.assertEqual(len(ms), 3)


class TestUserForm(TestCase):

    def test_password_val(self):
        u_form = UserForm(data=dict(
            username='u1',
            email='u1@u1.com',
            password='blablablabla',
            password_re='blablablabla'
        ))
        self.assertTrue(u_form.is_valid())

    def test_password_val(self):
        u_form = UserForm(data=dict(
            username='u1',
            email='u1@u1.com',
            password='blablablabla',
            password_re='blablablabla1'
        ))
        self.assertFalse(u_form.is_valid())


class TestQuestionForm(TestCase):

    def test_correct_tags(self):
        f = QuestionForm(data=dict(
            title='-',
            content='-',
            tags='bla bla',
        ))
        self.assertTrue(f.is_valid())

    def test_incorrect_len(self):
        f = QuestionForm(data=dict(
            title='-',
            content='-',
            tags='asdasdasdasdasdasdsad',
        ))
        self.assertFalse(f.is_valid())

    def test_incorrect_fields_count(self):
        f = QuestionForm(data=dict(
            title='-',
            content='-',
            tags='a b c d',
        ))
        self.assertFalse(f.is_valid())
