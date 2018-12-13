from tornado import web

from .forms import WordCounterForm


class WordCounterHandler(web.RequestHandler):
    template_name = "word_counter/word_counter.html"

    def get(self, *args, **kwargs):
        form = WordCounterForm()
        self.render(self.template_name, form=form)

    def post(self, *args, **kwargs):
        form = WordCounterForm(self.request.arguments)
        if form.validate():
            # TODO: fetch url and return words
            #     sql = "SELECT table_name FROM information_schema.tables;"
            #     res = await self.application.db.query(sql)
            print('form valid')

        self.render(self.template_name, form=form)
