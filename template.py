# noqa: E501
import strawberry
from typing import List, Optional

# Mock database
shops_db = [
    {
        "id": "1",
        "name": "Literary Paradise",
        "location": {"address": "123 Book Lane"},
        "books": [
            {"title": "Mystery of the Old Library", "author": "Jane Doe", "price": 14.99},
            {"title": "Journey Through the Pages", "author": "John Smith", "price": 12.50},
            {"title": "The Bookworm's Guide to the Galaxy", "author": "Emily Stone", "price": 17.00},  
            {"title": "Adventures in Reading", "author": "Alex Johnson", "price": 10.99}
        ]
    },
    {
        "id": "2",
        "name": "The Book Nook",
        "location": {"address": "456 Novel Street"},
        "books": [
            {"title": "Tales of the Unknown Writer", "author": "Sarah Black", "price": 13.75},
            {"title": "Chronicles of the Lost Pages", "author": "Mike White", "price": 15.20}
        ]
    }
]

def get_shop_from_db(id:str):
    return next((shop for shop in shops_db if shop["id"] == id), None)

