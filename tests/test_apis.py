# coding utf-8

"""
test user's apis
"""
import unittest
import json
# pylint: disable=import-error
from serv import create_app, db


class UserTestCase(unittest.TestCase):
    """API Test Case Class"""
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        self.pre_work()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        """set json headers"""
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def pre_work(self):
        """add a new user to aos_test_db"""
        user = {
            "user_name": "1000px",
            "password": "123456",
            "email": "foo@abc.com"
        }
        resp_user = self.client.post('/register',
                                     headers=self.get_api_headers(),
                                     data=json.dumps(user))
        self.current_user_id = resp_user.json.get('data').get('id')
        shop = {
            'shop_name': 'food edison',
            'shop_img': 'http://?',
            'user_id': self.current_user_id
        }
        resp_shop = self.client.post('/shop',
                                     headers=self.get_api_headers(),
                                     data=json.dumps(shop))
        self.current_shop_id = resp_shop.json.get('data').get('id')
        dish = {
            'dish_name': 'hsrou',
            'dish_desc': 'hong shao rou',
            'dish_img': 'http://?'
        }
        resp_dish = self.client.post('/dish/'+str(self.current_shop_id),
                                     headers=self.get_api_headers(),
                                     data=json.dumps(dish))
        self.current_dish_id = resp_dish.json.get('data').get('id')
        category = {
            'category_name': 'big love'
        }
        resp_category = self.client.post('/category/'+str(self.current_shop_id),
                                         headers=self.get_api_headers(),
                                         data=json.dumps(category))
        self.current_category_id = resp_category.json.get('data').get('id')

    ### user api list
    def test_user_get(self):
        """get a user by user's id"""
        response = self.client.get('/user/'+str(self.current_user_id),
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def test_user_put(self):
        """test edit user's infor"""
        data = {
            "user_name": "2000px"
        }
        response = self.client.put('/user/'+str(self.current_user_id),
                                   headers=self.get_api_headers(),
                                   data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_users_get(self):
        """test get user list"""
        response = self.client.get('/users',
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def _test_user_del(self):
        """test del user by user's id"""
        response = self.client.delete('/user/'+str(self.current_user_id),
                                      headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    ### shop api list
    def test_shop_get(self):
        """test get a shop infor"""
        response = self.client.get('/shop/'+str(self.current_shop_id),
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def test_shop_put(self):
        """test edit shop infor"""
        shop = {
            'shop_name': 'new food shop'
        }
        response = self.client.put('/shop/'+str(self.current_shop_id),
                                   headers=self.get_api_headers(),
                                   data=json.dumps(shop))
        self.assertEqual(response.status_code, 200)

    def test_shops_get(self):
        """test get shop list"""
        response = self.client.get('/shops/'+str(self.current_user_id),
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def _test_shop_del(self):
        """test del shop by shop's id"""
        response = self.client.delete('/shop/'+str(self.current_shop_id),
                                      headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    ### dish api list
    def test_dish_get(self):
        """test get dish infor"""
        response = self.client.get('/dish/'+str(self.current_dish_id),
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def test_dish_put(self):
        """test edit dish infor"""
        dish = {
            'dish_name': 'wahaha'
        }
        response = self.client.put('/dish/'+str(self.current_dish_id),
                                   headers=self.get_api_headers(),
                                   data=json.dumps(dish))
        self.assertEqual(response.status_code, 200)

    def test_dishes_get(self):
        """test get dishes list"""
        response = self.client.get('/dishes/'+str(self.current_shop_id)+'/all',
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    ### category api list
    def test_category_get(self):
        """test get category infor"""
        response = self.client.get('/category/'+str(self.current_category_id),
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def test_categories_get(self):
        """test get category list"""
        response = self.client.get('/categories/'+str(self.current_shop_id),
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)

    def test_category_put(self):
        """test edit category infor"""
        category = {
            'category_name': 'new category name'
        }
        response = self.client.put('/category/'+str(self.current_category_id),
                                   headers=self.get_api_headers(),
                                   data=json.dumps(category))
        self.assertEqual(response.status_code, 200)
