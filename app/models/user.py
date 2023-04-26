from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, EmailField, IntField, EnumField

class Category(EmbeddedDocument):
    name = StringField(required=True)
    value = StringField(required=True)

class Notification(EmbeddedDocument):
    type = StringField(choices=('push', 'email'), required=True)
    frequency = StringField(choices=('weekly', 'daily', 'every other day', 'all'), required=True)
    time_of_notification = StringField(required=True)


class Preferences(EmbeddedDocument):
    categories = ListField(EmbeddedDocumentField(Category))
    notification = EmbeddedDocumentField(Notification)
    language = StringField(choices=('hi', 'en', 'fr', 'jp'), required=True)
    region = StringField(choices=('us', 'in', 'jp', 'fr'), required=True)

class Users(Document):
    id = StringField(primary_key=True)
    name = StringField(required=True)
    email = EmailField(required=True)
    picture = StringField(required=True)
    preferences = EmbeddedDocumentField(Preferences)
    role = StringField(required=True)