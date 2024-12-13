from core.repository.character_repository import CharacterRepository


class CharacterService:

    def __init__(self, character_repository: CharacterRepository):
        self.repository = character_repository

    async def get_list(self):
        return await self.repository.read()

    async def add(self, schema):
        return await self.repository.create(schema)

    async def patch(self, id: int, schema):
        return await self.repository.update(id, schema)

    async def remove_by_id(self, id):
        return await self.repository.delete_by_id(id)

    async def get_by_field(self, field, id):
        return await self.repository.read_by_field(field, id)