import typing
import strawberry
from strawberry.field import StrawberryField

# resolvers
def get_books():
    return [
            Book(
                title="The Great Gatsby",
                author="123",
                )
            ]

# schema
@strawberry.type
class Book:
  title: str
  author: str

@strawberry.type
class Query:
  books: typing.List[Book] = strawberry.field(resolver=get_books)

schema = strawberry.Schema(query=Query)
