import graphene
from graphene import ObjectType, String, Schema

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

schema = graphene.Schema(query=Query)


# we can query for our field (with the default argument)
query_string = '{ hello }'
result = schema.execute('''
  query {
    hello
  }
''')
print(result.data['hello'])

# or passing the argument in the query
query_with_argument = '{ hello(name: "GraphQL") }'
result = schema.execute(query_with_argument)
print(result.data['hello'])
# "Hello GraphQL!"

# Even shorter
print(
    schema
        .execute('{ goodbye }')
        .data['goodbye']
    )