from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '../')

from ..utils import generic
from main import app

client = TestClient(app)


def test_message_type():
    assert generic.MessageType.has_value('ORGANIZATION')
    assert generic.MessageType.has_value('SHIPMENT')
    assert generic.MessageType.has_value('ship') == False


def test_weight_unit():
    assert generic.WeightUnit.kg == "KILOGRAMS"
    assert generic.WeightUnit.oz == "OUNCES"
    assert generic.WeightUnit.kg != "POUNDS"
    assert generic.WeightUnit.kg != "kg"
    assert generic.WeightUnit.has_value("KILOGRAMS")
    assert generic.WeightUnit.has_value("oz") == False


def test_weight_conversion():
    assert generic.WeightConversion.kg_to_lb == 2.20462
    assert generic.WeightConversion.kg_to_oz == 35.274
    assert generic.WeightConversion.lb_to_kg == 0.453592
    assert generic.WeightConversion.lb_to_oz == 16
    assert generic.WeightConversion.oz_to_kg == 0.0283495
    assert generic.WeightConversion.oz_to_lb == 0.0625

def test_weight_converter():
    assert generic.WeightConverter.convert(1000, "KILOGRAMS")['kg'] == 1000
    assert generic.WeightConverter.convert(1000, "KILOGRAMS")['lb'] == 2204.62
    assert generic.WeightConverter.convert(1000, "KILOGRAMS")['oz'] == 35274

    assert generic.WeightConverter.convert(1000, "POUNDS")['kg'] == 453.592
    assert generic.WeightConverter.convert(1000, "POUNDS")['lb'] == 1000
    assert generic.WeightConverter.convert(1000, "POUNDS")['oz'] == 16000

    assert generic.WeightConverter.convert(1000, "OUNCES")['kg'] == 28.3495
    assert generic.WeightConverter.convert(1000, "OUNCES")['lb'] == 62.5
    assert generic.WeightConverter.convert(1000, "OUNCES")['oz'] == 1000
