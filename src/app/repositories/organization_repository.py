from app.repositories.base_cassandra_repository import BaseRepository
from app.repositories.base_cassandra_repository import Organization

class OrganizationRepository(BaseRepository):

    _model = Organization
