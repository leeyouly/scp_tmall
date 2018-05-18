from spiderlib.data import DataStorage
import PyDB

class ImportScp_TombarthiteStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_CL_TOMBARTHITE_NEWS'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("news_title", is_key=True),
            PyDB.StringField("news_content"),
            PyDB.StringField("public_Id", ),
            PyDB.StringField("public_name"),
            PyDB.StringField("news_contenturl"),
            PyDB.StringField("news_html"),
            PyDB.StringField("viewpoint"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("news_contenturl", ),
            PyDB.StringField("source", ),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

