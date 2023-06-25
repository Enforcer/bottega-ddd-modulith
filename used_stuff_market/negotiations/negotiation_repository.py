from pymongo.collection import Collection


class NegotiationRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection
