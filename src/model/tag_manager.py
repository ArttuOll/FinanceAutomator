"""Huolehtii tunnisteiden lukemisesta ja kirjoittamisesta tunnistetiedostoon."""
import json
import os


class TagManager:
    def __init__(self):
        self.resources_dir = "resources"
        self.tag_file_name = "tags.json"
        self.self_dir = os.path.dirname(__file__)
        self.relative_path = os.path.join(self.resources_dir, self.tag_file_name)
        self.tag_file_path = os.path.join(self.self_dir, self.relative_path)

    def read_tags(self):
        """Lukee kategoriat ja niitä vastaavat tunnisteet tunnistetiedostosta
        ja palauttaa ne sanakirjana."""
        with open(self.tag_file_path, "r") as tags_file:
            data = tags_file.read()
            categories_tags_object = json.loads(data)

        return categories_tags_object

    def write_tags(self, dictionary):
        """Kirjoittaa kategoriat ja niitä vastaavat tunnisteet
        tunnistetiedostoon JSON-muodossa."""
        with open(self.tag_file_name, "w", encoding="UTF-8") as categories_tags_file:
            json.dump(dictionary, categories_tags_file, ensure_ascii=False,
                      indent=4)

        os.rename(self.tag_file_name, self.tag_file_path)
