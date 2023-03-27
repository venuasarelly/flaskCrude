from flask import Flask, jsonify, request
import json
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

# Define the item data model
item_model = api.model('Item', {
    'Name': fields.String(required=True, description='The name of the beach'),
    'Address': fields.String(required=True, description='address of the beach'),
    'How to  get there': fields.String(required=True, description='how to get there'),
    'Activities to do': fields.String(required=True, description='activitied to do'),
    'Geolocation': fields.String(required=True, description='geo location'),
    'Ratings': fields.String(required=True, description='ratings'),
    'Overview': fields.String(required=True, description='overview')

})

# Define the route for creating a new item
@api.route('/items')
class Items(Resource):
    @api.expect(item_model)
    def post(self):
        # Get the data from the request
        data = request.json

        # Load the existing data from the JSON file
        with open('datas.json', 'r') as f:
            items = json.load(f)

        # Add the new item to the existing data
        items.append(data)

        # Save the updated data to the JSON file
        with open('datas.json', 'w') as f:
            json.dump(items, f)

        # Return a JSON response indicating success
        return {'success': True}

    # Define the route for retrieving all items
    @api.doc(responses={
        200: 'Success',
        404: 'No items found'
    })
    def get(self):
        # Load the data from the JSON file
        with open('datas.json', 'r') as f:
            items = json.load(f)

        # Return the data as a JSON response
        return items

# Define the route for retrieving a specific item
@api.route('/items/<string:name>')
class Item(Resource):
    @api.doc(responses={
        200: 'Success',
        404: 'Item not found'
    })
    def get(self, name):
        # Load the data from the JSON file
        with open('datas.json', 'r') as f:
            items = json.load(f)
        for item in items:
            if item['Name'] == name:
                return item
        # If no matching item is found, return a 404 error
        api.abort(404, f"Item {name} not found")

    # Define the route for deleting a specific item
    @api.doc(responses={
        200: 'Success',
        404: 'Item not found'
    })
    def delete(self, name):
        # Load the existing data from the JSON file
        with open('datas.json', 'r') as f:
            items = json.load(f)

        # Find the item with the given name
        for item in items:
            if item['Name'] == name:
                # Remove the item from the list
                items.remove(item)

                # Save the updated data to the JSON file
                with open('datas.json', 'w') as f:
                    json.dump(items, f)

                # Return a JSON response indicating success
                return {'success': True}

        # If the item wasn't found, return a 404 error
        api.abort(404, f"Item {name} not found")

# Define the Swagger UI documentation route
@api.route('/swagger')
class SwaggerUI(Resource):
    def get(self):
        return api.__schema__

if __name__ == '__main__':
    app.run(port=5000)
