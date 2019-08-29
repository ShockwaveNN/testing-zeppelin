import json
import logging
import requests


class ZeppelinApi:
    def __init__(self, url):
        self.url = url

    def notes(self):
        import urllib.request
        logging.info('[ZeppelinApi] Get list of all notes')
        data = urllib.request.urlopen(self.url + "/api/notebook").read()
        return json.loads(data)['body']

    def delete_note_by_id(self, note_id):
        logging.info(f"[ZeppelinApi] delete_note_by_id: {note_id}")
        requests.delete(f"{self.url}/api/notebook/{note_id}")

    def delete_note_by_name(self, name):
        logging.info(f"[ZeppelinApi] Delete note by name: {name}")
        notes = self.notes()
        note = next(item for item in notes if item["name"] == name)
        self.delete_note_by_id(note['id'])
