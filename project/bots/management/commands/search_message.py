from django.core.management.base import BaseCommand
from project.bots.documents import MessagesDocument


class Command(BaseCommand):
    help = 'Get message from elasticsearch index'

    def handle(self, *args, **options):
        for message in options['messages']:
            resp = MessagesDocument.search().query("match", message=message)
            print("input: {}".format(message))
            for hit in resp:
                print("\tid : {}, message: {}".format(hit.id, hit.message))

    def add_arguments(self, parser):
        parser.add_argument('messages', nargs='+', type=str)
