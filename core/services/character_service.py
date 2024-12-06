from core.repository.character_repository import CharacterRepository


class CharacterService:

    def __init__(self, character_repository: CharacterRepository):
        self.repository = character_repository

    def get_list(self):
        return self.repository.read()

    def add(self, schema):
        return self.repository.create(schema)

    def patch(self, id: int, schema):
        return self.repository.update(id, schema)

    def remove_by_id(self, id):
        return self.repository.delete_by_id(id)

    def get_by_field(self, field, id):
        return self.repository.read_by_field(field, id)