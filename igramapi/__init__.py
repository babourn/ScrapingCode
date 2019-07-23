import requests

class InstacartApi:
    
    base_url = 'https://www.instacart.com'
    api_base_path = '/api/v2'
    
    def __init__(self, oauth_key, *args, **kwargs):
        if oauth_key != None:
            self.oauth_key = oauth_key
        # else:
        #     self.oauth_key = self.fetch_oauth_key()
        return super().__init__(*args, **kwargs)
        

    def fetch_oauth_key(self, client_id, client_secret, email, password):
        pass

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {self.oauth_key}',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }

    def fetch_cart(self, timeout=4):
        cart_url = '/cart'
        cart_request_url = f'{self.base_url}/{self.api_base_path}/{cart_url}'
        cart_request = requests.get(cart_request_url, timeout=timeout, headers=self.headers)
        return cart_request


    def get_item(self, item_id, timeout=4):
        item_base_url = f'/items/{item_id}'
        item_request_url = f'{self.base_url}/{self.api_base_path}/{item_base_url}'
        item_request = requests.get(item_request_url, timeout=timeout, headers=self.headers)
        return item_request
