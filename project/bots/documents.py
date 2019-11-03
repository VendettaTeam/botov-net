from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Messages
from elasticsearch_dsl import analyzer, token_filter

ru_morphology_filter = token_filter(
    'ru_RU',
    type="hunspell",
    locale="ru_RU",
    dedup=True
)

synonym_filter = token_filter(
    'synonym_filter',
    type="synonym",
    lenient=True,
    synonyms_path="analysis/synonym.txt"
)

my_analyzer = analyzer(
    'my_analyzer',
    tokenizer="standard",
    filter=[
        "lowercase",
        ru_morphology_filter,
        synonym_filter
    ],
)


@registry.register_document
class MessagesDocument(Document):
    message = fields.TextField(analyzer=my_analyzer)

    class Index:
        name = 'messages'

    class Django:
        model = Messages
        fields = ['id']
