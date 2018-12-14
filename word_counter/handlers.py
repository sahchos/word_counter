from tornado import web
from tornado.httpclient import AsyncHTTPClient

from utils.text_processor import TextProcessor
from .forms import WordCounterForm


class WordCounterHandler(web.RequestHandler):
    template_name = "word_counter/word_counter.html"

    def get(self, *args, **kwargs):
        form = WordCounterForm()
        self.render(self.template_name, form=form)

    async def post(self, *args, **kwargs):
        top_words = []
        form = WordCounterForm(self.request.arguments)
        if form.validate():
            source = form.data['url']
            http_client = AsyncHTTPClient()
            try:
                response = await http_client.fetch(source)
            except Exception as e:
                error_msg = f'Error occurred during URL fetching: {e}'
                self.render(self.template_name, form=form, error_msg=error_msg)
            else:
                text_processor = TextProcessor(text=response.body)
                text_processor.set_text_from_tags(['p', 'div'])
                word_counter = text_processor.get_word_counter(['N', 'V'])
                top_words = word_counter.most_common(100)

        self.render(self.template_name, form=form, top_words=top_words)
