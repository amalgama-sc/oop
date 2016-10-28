import csv
import json
from decimal import Decimal
from sys import exit


class Bond(object):
    def __init__(self, bond_id, price_dirty, profit, duration):
        if price_dirty == 'null':
            price_dirty = 0
        if profit == 'null':
            profit = 0
        if duration == 'null':
            duration = 0

        self.bond_id = int(bond_id)
        self.price_dirty = Decimal(price_dirty)
        self.profit = Decimal(profit)
        self.duration = Decimal(duration)


class BondManager(object):
    @classmethod
    def __init__(cls, filename):
        cls.bond_list = []
        cls.parse_scv(filename)

    @classmethod
    def parse_scv(self, filename):
        with open(filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                new_bond = Bond(row['bond_id'],
                                row['price_dirty'],
                                row['yield'],
                                row['duration'],
                                )
                self.bond_list.append(new_bond)

    @classmethod
    def get_bond(self, search_id):
        for bond in self.bond_list:
            if bond.bond_id == search_id:
                return bond
        raise NameError("Bond with id {0} was not found".format(search_id))


class Asset(object):
    def __init__(self, bondit_id, units):
        self.bondit_id = int(bondit_id)
        self.units = int(units)

    @property
    def weight(self):
        bond = BondManager.get_bond(search_id=self.bondit_id)
        return (bond.price_dirty * self.units / Portfolio.holding_value)


class Portfolio(object):
    @classmethod
    def __init__(cls, filename):
        cls.assets = []
        cls.assets = cls.parse_input(filename)
        cls.holding_value = cls.get_holding_value()

    @classmethod
    def parse_input(cls, filename):
        assets = []
        with open(filename) as json_file:
            data = json.load(json_file)
            for asset in data['assets']:
                new_asset = Asset(asset['bondit_id'], asset['units'])
                assets.append(new_asset)
        return assets

    @classmethod
    def get_holding_value(cls):
        holding_value = 0
        for asset in cls.assets:
            bond = bond_manager.get_bond(asset.bondit_id)
            holding_value += asset.units * bond.price_dirty
        return holding_value

    @classmethod
    def get_duration(cls):
        duration = Decimal(0.00)
        for asset in cls.assets:
            bond = bond_manager.get_bond(asset.bondit_id)
            duration += asset.weight * bond.duration
        return duration

    @classmethod
    def get_total_return(cls):
        total_return = Decimal(0.00)
        for asset in cls.assets:
            bond = bond_manager.get_bond(asset.bondit_id)
            total_return += asset.weight * bond.profit
        return total_return


if __name__ == "__main__":
    bond_manager = BondManager('bonds_trading_data.csv')
    portfolio = Portfolio('input.json')

    output = {
        "portfolio_holding_value": str(portfolio.holding_value),
        "portfolio_duration": str(portfolio.get_duration()),
        "portfolio_total_return": str(portfolio.get_total_return()),
        }

    exit(json.dumps(output))
