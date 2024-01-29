import strawberry
from typing import List, Optional


#
#   Database
#
    
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

#
#   Types
#
    
@strawberry.type
class Book:
    title: str
    author: str
    price: float

@strawberry.type
class Location:
    address: str

@strawberry.type
class Shop:
    id: str
    name: str
    location: Location

    @strawberry.field
    def books(self, info, limit: Optional[int] = None) -> List[Book]:
        # Fetch the shop's books from the database
        shop_books = next((shop["books"] for shop in shops_db if shop["id"] == self.id))
        # Apply the limit if provided
        if limit is not None:
            return [Book(**book) for book in shop_books[:limit]]
        return [Book(**book) for book in shop_books]

#
#   Query
#
    
@strawberry.type
class Query:
    @strawberry.field
    def shop(self, id: str) -> Optional[Shop]:
        # Fetch a shop by ID
        shop_data = get_shop_from_db(id)
        if shop_data:
            return Shop(**shop_data)
        return None

    @strawberry.field
    def shops(self) -> List[Shop]:
        return [Shop(id=shop['id'], name=shop['name'], location=Location(**shop['location'])) for shop in shops_db]

#
#   Mutation
#
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book_to_shop(self, info, shop_id: strawberry.ID, title: str, author: str, price: float) -> Book:
        # Find the shop in the database
        shop = get_shop_from_db(shop_id)
        if not shop:
            raise ValueError("Shop not found")

        # Create new book and add it to the shop's books
        new_book = {"title": title, "author": author, "price": price}
        shop["books"].append(new_book)

        return Book(**new_book)


schema = strawberry.Schema(query=Query, mutation=Mutation)


# Example GQL query
gql_q="""query {
 shops {
  name
  location{
    address
  }
  books{
    title
  }
	}
}"""

gql_q_mutation = """mutation {
  addBookToShop(shopId: "1", title: "New Book Title", author: "New Author", price: 19.99) {
    title
    author
    price
  }
}"""


# Mock database
#
#   In a more realistic SQL database, data would be more like this
#
# book_db= [
#     #ID, NAME     AUTHOR      PRICE
#     (1, "Book 1", "Author A", 10.0),
#     (2, "Book 2", "Author B", 12.0),
#     (3, "Book 3", "Author C", 11.0),
#     (4, "Book 4", "Author D", 15.0),
#     (5, "Book 5", "Author E", 9.0),
# ]

# shop_db = [
#         #ID, NAME     AUTHOR      ADRESS
#         (1, "Shop One", "111 Book Street"),
#         (2, "Shop Two", "222 Book Street"),
#     ]

# shop_book_rel = [
#     # SHOP_ID #BOOK_ID
#     (1,1),
#     (1,2),
#     (1,3),
#     (2,1),
#     (2,4),
# ]
