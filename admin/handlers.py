from tornado import web

from word_counter.models import Word


class AdminWordListHandler(web.RequestHandler):
    template_name = "admin/word_list.html"

    async def get(self, *args, **kwargs):
        limit = self.application.ADMIN_WORDS_PER_PAGE
        try:
            current_page = int(self.get_argument('page', 1))
        except ValueError:
            current_page = 1

        current_page = current_page if current_page > 0 else 1
        sql = f"SELECT * FROM `words` ORDER BY `count` DESC LIMIT {limit} OFFSET {(current_page - 1) * limit}"
        words = await self.application.db.query(sql)

        prepared_words = []
        for word in words:
            w = Word(word['word'], word['count'])
            w.word = w.get_decrypted_word(self.application.encryption)
            prepared_words.append(w)

        self.render(self.template_name, words=prepared_words, current_page=current_page)
