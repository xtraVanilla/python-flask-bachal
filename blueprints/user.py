import boto3
from flask import Blueprint, request
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Library')
user = Blueprint(name="user", import_name=__name__)


@user.post('/checkout')
def checkout_book():
    book_id = request.args.get('book_id')
    user_id = request.args.get('user_id')

    updateBookRes = table.update_item(
        Key={
            'id': book_id
        },
        UpdateExpression='SET available = false'
    )

    updateUserRes = table.update_item(
        Key={
            'id': user_id,
        },
        UpdateExpression='SET checkedOutBooks = :checkedOutBooks',
        ExpressionAttributeValues={
            ':checkedOutBooks': book_id
        }
    )

    return updateUserRes


@user.post('/return')
def return_book():
    book_id = request.args.get('book_id')
    user_id = request.args.get('user_id')

    updateBookRes = table.update_item(
        Key={
            'id': book_id
        },
        UpdateExpression='SET available = true'
    )

    updateUserRes = table.update_item(
        Key={
            'id': user_id,
        },
        UpdateExpression='DELETE checkedOutBooks = :checkedOutBooks',
        ExpressionAttributeValues={
            ':checkedOutBooks': book_id
        }
    )

    return updateUserRes


@user.route('/checkedoutbooks')
def get_checkedout_books():
    user_id = request.args.get('user_id')

    user = table.query(
        KeyConditionExpression=Key('id').eq(user_id)
    )

    books = table.batch_get_item(
        RequestItems={
            'Keys': user.checkedoutBooks
        }
    )

    return books
