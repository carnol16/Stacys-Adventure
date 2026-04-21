import requests
import random
from csgo_market_api import CSGOMarket

API_KEY = "96K4Hz3W3U3i75JmQQQawg6jSoMOPo2"


class marketItem:
    """Simple object holding name + price in camelCase."""

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<marketItem name='{self.name}' price={self.price}>"



class csPriceChecker:
    def __init__(self, api_key=API_KEY):
        self.market = CSGOMarket(api_key=api_key)

    def _fetchSingle(self, name):
        """Fetch one item (API still needs list)."""
        response = self.market.get_list_items_info(list_hash_name=[name])

        if not response.get("success"):
            raise RuntimeError(f"API error: {response}")

        data = response.get("data", {})
        info = data.get(name)

        price = info.get("min") if info else None
        return marketItem(name, price)

    def getItem(self, name):
        """Return MarketItem object."""
        return self._fetchSingle(name)

    def getItemPrice(self, name):
        """Return only the price."""
        return self._fetchSingle(name).price


#Test

caseChoices = [ "Chroma Case", 
                #"Gamma Case", 
                #"Dreams & Nightmares Case",
                #"Kilowatt Case",
                "Fever Case"
                ]

pickedCase = caseChoices[random.randint(0,1)]

market = csPriceChecker()

item  = market.getItem(pickedCase)

casePrice = int(item.price * 10)
caseName = item.name

#print(caseName, casePrice)

