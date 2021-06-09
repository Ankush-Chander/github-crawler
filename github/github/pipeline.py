# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import os
import traceback

import gspread

current_dir = os.path.dirname(os.path.realpath(__file__))

from elasticsearch import Elasticsearch, helpers


class GithubElasticsearchPipeline:
	actions = []

	def open_spider(self, spider):
		pass

	def close_spider(self, spider):
		pass

	def process_item(self, item, spider):
		# print(spider.settings)
		es = Elasticsearch(
			[{'host': spider.settings["ELASTICSEARCH_HOST"], 'port': spider.settings["ELASTICSEARCH_PORT"]}])
		action = {
			"_index": "github_users",
			'op_type': 'create',
			"_id": item['doc_id'],
			"_source": item
		}
		self.actions.append(action)

		if len(self.actions) == 10:
			helpers.bulk(es, self.actions, index='ted')
			self.actions.clear()


class GithubExcelPipeline:
	actions = []
	GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/1MbiDtsvI9s7Od49_Q_KE4yQtxGHg8fIc6Z2JeXVu4bQ/edit?usp=sharing"

	def open_spider(self, spider):
		pass

	def close_spider(self, spider):
		pass

	def process_item(self, item, spider):
		other_links = ", ".join(item["other_links"])
		row = [item["fullname"], item["github_link"], item["followers"], item["following"], item["location"],
		       item["description"], item["twitter_link"], other_links]
		self.actions.append(row)
		sheet = spider.settings["GOOGLE_SHEET"]

		if len(self.actions) >= 25:
			self.insert_data_into_google_sheet(sheet=sheet, rows_data=self.actions)
			self.actions.clear()
		# TODO: handle leftover items

	def insert_data_into_google_sheet(self, sheet=None, sheetname="github_sheet", rows_data: list = [],):
		try:
			gc = gspread.service_account(filename=f"{current_dir}/../../utility/gsheets_credentials.json")
			gsheet = gc.open_by_url(sheet)
			try:
				gsheet.add_worksheet(sheetname, rows=210, cols=20)
			except gspread.exceptions.APIError as err:
				print(traceback.format_exc())
				pass
			wsheet = gsheet.worksheet(sheetname)
			wsheet.insert_rows(rows_data, row=2)
		except Exception as err:
			print(rows_data)
			print(traceback.format_exc())
			pass
