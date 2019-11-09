import vk_api
from elasticsearch import Elasticsearch
from .response import BotResponse
from vk_api.utils import get_random_id
from project.bots.documents import RequestsDocument
from project.bots.utils import is_chat
from django.conf import settings


class StatsResponse(BotResponse):

    def run(self):
        peer_id = self.request_info.request['object']['peer_id']
        from_id = self.request_info.request['object']['from_id']

        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        if is_chat(self.request_info.request):
            try:
                group_messages = self.get_group_messages_count(peer_id)
                conversation_info = vk.messages.getConversationMembers(
                    peer_id=self.request_info.request['object']['peer_id'])

                message = ""
                count_messages = 0
                for user in conversation_info['profiles']:
                    user_messages_count = group_messages.get(user['id'], 0)
                    count_messages += user_messages_count
                    message += "{} {}: {}\n".format(user['first_name'], user['last_name'], user_messages_count)
                message = "Всего сообщений: {}\n\n{}".format(count_messages, message)
            except:
                message = "Для работы этой функции меня нужно назначить администратором"
        else:
            message = "Отправлено сообщений: " + self.get_user_messages_count(peer_id, from_id)
        vk.messages.send(
            message=message,
            random_id=get_random_id(),
            peer_id=self.request_info.request['object']['peer_id']
        )

    def get_user_messages_count(self, peer_id, from_id):
        client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])

        response = client.search(
            index=RequestsDocument().Index.name,
            body={
                "size": 0,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "peer_id": {
                                        "value": peer_id,
                                        "boost": 1.0
                                    }
                                }
                            },
                            {
                                "term": {
                                    "from_id": {
                                        "value": from_id,
                                        "boost": 1.0
                                    }
                                }
                            }
                        ],
                        "adjust_pure_negative": True,
                        "boost": 1.0
                    }
                }
            }
        )

        return str(response['hits']['total']['value'])

    def get_group_messages_count(self, peer_id):
        client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])

        response = client.search(
            index=RequestsDocument().Index.name,
            body={
                "size": 0,
                "query": {
                    "term": {
                        "peer_id": {
                            "value": peer_id,
                            "boost": 1.0
                        }
                    }
                },
                "_source": False,
                "stored_fields": "_none_",
                "aggregations": {
                    "groupby": {
                        "composite": {
                            "size": 1000,
                            "sources": [
                                {
                                    "363": {
                                        "terms": {
                                            "field": "from_id",
                                            "missing_bucket": True,
                                            "order": "asc"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        )

        key = list(response['aggregations']['groupby']['after_key'].keys())[0]

        user_list = {}
        # TODO add sorting
        for bucket in response['aggregations']['groupby']['buckets']:
            user_list[bucket['key'][key]] = bucket['doc_count']

        return user_list
