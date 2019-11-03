class ResponseAnswer():
    @classmethod
    def get_response_class(self, answer_obj):
        import random
        from pydoc import locate
        random_response = random.choice(answer_obj)
        payload = random_response['payload']

        response_class = locate(
            'project.bots.response.' + random_response['type'] + '.' + self._snake_to_camel(random_response['type'])
        )

        return response_class, payload

    @classmethod
    def _snake_to_camel(self, word):
        return ''.join(x.capitalize() or '_' for x in word.split('_'))

    @classmethod
    def default_answer_structure(self):
        return [
            {
                'type': 'text_response',
                'payload': {
                    'text_response': 'value',
                }
            }
        ]
