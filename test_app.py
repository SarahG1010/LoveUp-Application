import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import http.client

from app import create_app
from models import setup_db,Movie, Pred_Rating,db_drop_and_create_all,db
from get_token import get_public_headers, get_member_headers, get_admin_headers



#public_headers = { 'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1MdHFvUXhpeGhJZWRSM0Zob3F3ZSJ9.eyJpc3MiOiJodHRwczovL2Rldi10YzdsNHFxMWczZjdiamp1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJGakI2Nk9lazhlQ2VHQWs3R3psTzhLUklSSmNxV2VaTUBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNzE4NjQ1NTEyLCJleHAiOjE3MTg3MzE5MTIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkZqQjY2T2VrOGVDZUdBazdHemxPOEtSSVJKY3FXZVpNIiwicGVybWlzc2lvbnMiOltdfQ.C7dsXIZ0RqQWP0TDmd6ye86iAZYBIpEd-MeU8rywUORHdUXFRRCKXfjOaIAlSN92G4KOMH9np1V300yGhtZxG8XyylF727evQdnz2T-fG2oxze0ja7cbfLpN1Y0gKi91ytBZ1Qrog_jclhqWwbeKvoX-6tjSLxeiw4t6Fesetg_IRxvNLk36kq15WmvIfTu_DbnQ-tHtLaW_sKI9ZgwGFStdir2_83NKwPkvrFVvYevmie-J3a-81Vyzm79MshL-QvB6d9hmUkFbgYrg_NcDRQuEvRyA9BL_3wSB1M7Wm9uZRHhCljluxC9eZSxEz_2Tf3aWU1ZkjpLpJjh4kMMiRQ" }
public_headers = get_public_headers()
member_headers = get_member_headers()
admin_headers = get_admin_headers()


class MovieTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.database_name = 'movie_child_test'
        ## my revision
        cls.database_path = 'postgresql://{}@{}/{}'.format('postgres','localhost:5432', cls.database_name)
        # Define your test configuration
        cls.app = create_app({
            "SQLALCHEMY_DATABASE_URI": cls.database_path
        })
        #print('test0')
        cls.client = cls.app.test_client
        #print('test1')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    def tearDown(self):
        """Executed after reach test"""
        # Example: Close database connections
        # self.db_connection.close()

        # Example: Delete temporary files or directories
        # os.remove('temp_file.txt')

        # Example: Reset instance-level variables
        # self.some_variable = initial_value
        # Drop all tables in the database after all tests complete
        db.session.rollback()
        pass

    #db_drop_and_create_all() 
# ------------------------------------------------------------------------------
#  TEST follow by the route in app.py divide by roles
# ------------------------------------------------------------------------------
## root rout test
    def test_get_root(self):
        reps = self.client().get('/')
        data = json.loads(reps.data)
        self.assertEqual(reps.status_code, 200)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], True)



## public role test for 5 endpoints

    def test_get_all_movies(self):
        reps = self.client().get('/movies')
        data = json.loads(reps.data)
        self.assertEqual(reps.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_detail(self):
        reps = self.client().get('/movies-detail',headers=public_headers)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_add_movies(self):
        reps = self.client().post('/movies',headers=public_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        reps = self.client().patch('/movies/1',headers=public_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        reps = self.client().delete('/movies/1',headers=public_headers)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

## member role

    def test_member_get_movies_detail(self):
        reps = self.client().get('/movies-detail',headers=member_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_member_add_movies(self):
        reps = self.client().post('/movies',headers=member_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_member_update_movie(self):
        reps = self.client().patch('/movies/1',headers=member_headers)
        print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_member_delete_movie(self):
        reps = self.client().delete('/movies/1',headers=member_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 403)
        self.assertEqual(data['success'], False)

## manager role
    def test_admin_get_movies_detail(self):
        reps = self.client().get('/movies-detail',headers=admin_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_admin_member_add_movies(self):
        new_movie = {"detail": [{"director": "BB", "writer": "aa1, ba1", "Cast": "aa2, ba2"}],
                        "duration": 120,
                        "pred_rating_id": 1,
                        "title": "test123",
                        "year": 2024 }
        reps = self.client().post('/movies',headers=admin_headers,json=new_movie)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_admin_member_update_movie(self):
        update_movie = {"detail": [{"director": "update", "writer": "aa1, ba1", "Cast": "aa2, ba2"}],
                        "duration": 120,
                        "pred_rating_id": 1,
                        "title": "test_update",
                        "year": 2024 }
        reps = self.client().patch('/movies/1',headers=admin_headers,json=update_movie)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_admin_member_delete_movie(self):
        reps = self.client().delete('/movies/2',headers=admin_headers)
        #print(reps)
        data = json.loads(reps.data)
        # print(data)

        self.assertEqual(reps.status_code, 200)
        self.assertEqual(data['success'], True)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    