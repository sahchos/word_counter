import tornado.web


class WordCounterHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        sql = "SELECT table_name FROM information_schema.tables;"
        res = await self.application.db.query(sql)
        print(res)
        self.write("Hello world")
        self.finish()
