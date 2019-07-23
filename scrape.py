import requests
from igramapi import InstacartApi
import time
import json
import os

class Crawler:

    def __init__(self, *args, **kwargs):
        self.items_to_fetch = set()
        self.items_already_fetched = set()
        self.api = InstacartApi('126a65ef4df857e8c47a8d9597d261e7a3f69e3c5e0eaacf39dc20c04574b308')
        return super().__init__(*args, **kwargs)
    
    def load_existing_files(self):
        for file in os.listdir('/data/results'):
            if os.path.isfile(os.path.join('/data/results', file)):
                item_id = file.split('.')[0]
                self.items_already_fetched.add(int(item_id))
        to_fetch_file = open('/data/results_meta/to_fetch.json', 'r')
        fetch_raw = to_fetch_file.read()
        fetch_list = json.loads(fetch_raw)
        self.items_to_fetch = set(fetch_list)
        to_fetch_file.close()
        self.rectify_lists()
    
    def seed_items_from_cart(self):
        response = self.api.fetch_cart()
        if response.status_code == 200:
            response_json = response.json()
            response_server_code = response_json.get('meta', {}).get('code', None)
            if response_server_code:
                for item in response_json.get('data', {}).get('items', []):
                    self.process_items_to_add_from_cart(item)
            else:
                raise requests.RequestException
        else:
            raise requests.RequestException

    def process_items_to_add_from_cart(self, item):
        self.items_to_fetch.add(item['item_id'])
        self.items_to_fetch.update(set(item['item'].get('suggested_replacement_ids', [])))
        for recommended_item_group in item['item'].get('recommended_replacements', []):
            group_items = [item[0] for item in recommended_item_group.get('replacement_item_ids', [])]
            self.items_to_fetch.update(set(group_items))
        print(len(crawler.items_to_fetch))

    def process_items_to_add(self, item):
        self.items_to_fetch.update(set(item.get('suggested_replacement_ids', [])))
        for recommended_item_group in item.get('recommended_replacements', []):
            group_items = [item[0] for item in recommended_item_group.get('replacement_item_ids', [])]
            self.items_to_fetch.update(set(group_items))
        print(len(crawler.items_to_fetch))

    def rectify_lists(self):
        self.items_to_fetch.difference_update(self.items_already_fetched)
        # print(self.items_to_fetch)
        self.save_items_to_fetch()

    def crawl_products(self):
        while len(self.items_to_fetch) != 0:
            item_id_to_fetch = self.items_to_fetch.pop()
            # print(item_id_to_fetch)    
            item_response = self.api.get_item(item_id_to_fetch)
            if item_response.status_code == 200:
                # print(item_response.json())
                self.items_already_fetched.add(item_id_to_fetch)
                item_data = item_response.json()['data']
                self.process_items_to_add(item_data)
                self.save_item(item_data)
                self.rectify_lists()
                time.sleep(4)
            else:
                raise requests.RequestException

    def save_item(self, item_data):
        item_id = item_data['id']
        new_file = open(f'/data/results/{item_id}.json', 'w')
        new_file.write(json.dumps(item_data))
        new_file.close()

    def save_items_to_fetch(self):
        to_fetch_file = open('/data/results_meta/to_fetch.json', 'w')
        to_fetch_file.write(json.dumps(list(self.items_to_fetch)))
        to_fetch_file.close()

if __name__ == '__main__':
    crawler = Crawler()
    crawler.load_existing_files()
    crawler.seed_items_from_cart()
    crawler.crawl_products()
    