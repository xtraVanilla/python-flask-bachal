import boto3
from flask import Blueprint, request
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Library')
librarian = Blueprint(name="librarian", import_name=__name__)


@librarian.route('/overdue')
def get_overdue_books():
    response = table.query(
        IndexName="overdue",
        KeyConditionExpression=Key('overdue').eq(True)
    )

    return response


@librarian.post('/librarian')
def add_book():
    id = request.args.get('id')
    title = request.args.get('title')
    author = request.args.get('author')
    quantity = request.args.get('quantity')
    available = request.args.get('available')

    response = table.put_item(
        Item={
            'id': id,
            'title': title,
            'author': author,
            'quantity': quantity,
            'available': available
        }
    )

    return response


@librarian.delete('/librarian')
def remove_book_by_id():
    id = request.args.get('id')

    response = table.delete_item(
        Key={
            'id': id
        }
    )

    return response
