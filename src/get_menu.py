from datetime import timedelta
import json
import requests

from cachetools import cached, TTLCache


cache = TTLCache(maxsize=10, ttl=timedelta(days=7).total_seconds())


class Cafe:
    def __init__(self, company: str, cafe_name: str):
        self.base_url = f"https://{company}.cafebonappetit.com/cafe/{cafe_name}"

    @staticmethod
    def convert_cor_icons(item: dict):
        cor_icons = {
            "1": "[V]",
            "3": "[SW]",
            "4": "[Ve]",
            "6": "[FF]",
            "9": "[GF]"
        }
        return "".join(cor_icons.get(i, "") for i in item["cor_icon"])

    def items_to_text(self, items: dict) -> str:
        return "\n".join(
            "* "
            f"{val['label'].title()}{self.convert_cor_icons(val)}: "
            f"{val['description'].capitalize()}." for val in items.values()
        )

    def get_menu_items(self, date_: str) -> dict:
        """
        :param date_: str YYYY-MM-DD
        """
        r = requests.get(f"{self.base_url}/{date_}")
        lines = r.text.splitlines()
        for line in lines:
            if "Bamco.menu_items" in line:
                return json.loads(line.split("= ")[1][:-1])
        raise Exception("Unable to find ")

    @cached(cache)
    def menu_items(self, date_) -> str:
        """
        Get menu items as string for specified date.
        :param date_: str YYYY-MM-DD
        """
        return self.items_to_text(self.get_menu_items(date_))
