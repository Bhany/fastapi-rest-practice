import json
import requests

messages = [
  {
    "type": "ORGANIZATION",
    "id": "99f2535b-3f90-4758-8549-5b13c43a8504",
    "code": "BOG"
  },
  {
    "type": "ORGANIZATION",
    "id": "381f5cc5-dfe4-4f58-98ad-116666855ca3",
    "code": "SEA"
  },
  {
    "type": "ORGANIZATION",
    "id": "34f195b5-2aa1-4914-85ab-f8849f9b541a",
    "code": "FMT"
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001175",
    "organizations": ["SEA", "BOG", "FMT"],
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "0",
            "unit": "KILOGRAMS"
          }
        }
      ],
    }
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001009",
    "organizations": [],
    "estimated_time_arrival": "2020-01-17T15:07:00",
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "1000",
            "unit": "OUNCES"
          }
        }
      ]
    }
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001142",
    "organizations": ["FMT"],
    "estimated_time_arrival": "2020-08-29T00:00:00",
    "transport_packs": {
      "nodes": []
    }
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001071",
    "organizations": ["BOG"],
    "estimated_time_arrival": "2020-03-13T00:00:00",
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "5",
            "unit": "KILOGRAMS"
          }
        }
      ]
    }
  },
  {
    "type": "ORGANIZATION",
    "id": "34f195b5-2aa1-4914-85ab-f8849f9b541a",
    "code": "NAM"
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001167",
    "organizations": ["SEA"],
    "estimated_time_arrival": "2020-11-21T00:00:00",
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "22690",
            "unit": "KILOGRAMS"
          }
        }
      ]
    }
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001175",
    "organizations": ["SEA", "NAM"],
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "10",
            "unit": "KILOGRAMS"
          }
        }
      ]
    }
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001197",
    "organizations": ["BOG"],
    "estimated_time_arrival": None,
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "10",
            "unit": "POUNDS"
          }
        }
      ]
    }
  },
  {
    "type": "SHIPMENT",
    "reference_id": "S00001175",
    "organizations": ["SEA"],
    "estimated_time_arrival": "2020-11-20T00:00:00",
    "transport_packs": {
      "nodes": [
        {
          "total_weight": {
            "weight": "3",
            "unit": "KILOGRAMS"
          }
        }
      ]
    }
  },
]


url = 'http://localhost:8000/{}'

for message in messages:
    j = json.dumps(message)
    if message['type'] == "SHIPMENT": endpoint = "shipment"
    else: endpoint = "organization"
    print("MESSAGE:{}".format(j))
    response = requests.post(url.format(endpoint), data=j)
    print(response.text)
    input()


