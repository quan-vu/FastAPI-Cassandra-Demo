import abc
import math
import uuid
from datetime import datetime
from app.responses.base_response import PaginationResponse

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# For model
from cassandra.cqlengine import columns, functions
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import register_connection, set_default_connection, dict_factory


KEYSPACE = "keyspace_organization_db"
HOSTS = ['db_center_cassandra']
CREDENTIAL = {'username': 'cassandra', 'password': 'cassandra'} 
AUTH_PROVIDER = PlainTextAuthProvider(username='cassandra', password='cassandra')


class Organization(Model):

    __keyspace__ = KEYSPACE
    __table_name__ = 'organizations'

    organization_id = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    user_id = columns.BigInt()
    name = columns.Text()
    alias = columns.Text()
    logo = columns.Text()
    created_at = columns.DateTime(default=datetime.utcnow())
    updated_at = columns.DateTime(default=datetime.utcnow())
    

class OrganizationMember(Model):

    __keyspace__ = KEYSPACE
    __table_name__ = 'organization_members'

    organization_member_id = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    user_id = columns.TimeUUID()
    roles = columns.List(value_type=columns.Text, default=['member'])
    created_at = columns.DateTime(default=datetime.utcnow())
    updated_at = columns.DateTime(default=datetime.utcnow())



def cassandra_session_factory():
    cluster = Cluster(HOSTS, auth_provider=AUTH_PROVIDER)
    session = cluster.connect()

    log.info("Creating keyspace...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE
    )

    log.info("Setting keyspace...")
    session.set_keyspace(KEYSPACE)

    session.row_factory = dict_factory
    session.execute("USE {}".format(KEYSPACE))

    return session


_session = cassandra_session_factory()
register_connection(str(_session), session=_session)
set_default_connection(str(_session))

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def to_dict(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def to_list(self, l):
        raise NotImplementedError



class BaseRepository(AbstractRepository):

    _model = None

    def __init__(self):
        self.session = _session

    def to_dict(self, obj):
        if obj is not None:
            return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
        else:
            return {}

    def to_list(self, _list):
        if isinstance(_list, list) and len(_list):
            output = []
            for item in _list:
                output.append(self.to_dict(item))
            return output
        else:
            print("A list is reuired!")
            return []

    def _is_empty(self, value):
        if value is None:
            return True
        elif isinstance(value, str) and value.strip() == '':
            return True
        return False

    def find(self, id: int):
        item = self._model.objects(organization_id=id)
        if item is not None:
            return dict(item[0])
        return None    

    def paginate(self, limit: int, offset: str = None, search: str = ''):
        total = self._model.objects.count()
        last_page = math.ceil(total / limit) if total > 0 else 1
        next_page = None
        data = []
        
        if total > 0:
            query = self._model.objects.all().limit(limit)
            
            if offset is not None:
                query = query.filter(pk__token__gt=functions.Token(offset))

            data = list(query)

            if len(data) > 0:
                last = data[-1]
                next_page = f'?limit={limit}&offset={last.pk}&search={search}'
        
        return PaginationResponse(
            total=total,
            limit=limit,
            offset=offset,
            last_page=last_page,
            next_page_link=next_page,
            data=data
        )

    def create(self, data):
        item = self._model.create(
            organization_id=str(uuid.uuid1()),
            user_id=data.user_id,
            name=data.name,
            alias=data.alias,
            logo=data.logo,
        )
        return item

    def update(self, id, data):
        records = self._model.objects(organization_id=id)
        if records is not None:
            item = records[0]
            item.update(
                name=data.name,
                alias=data.alias,
                logo=data.logo,
            )
            return item
        return None

    # def update(self, id: int, request):
    #     data = request.dict(
    #         exclude_none=True,
    #         exclude_unset=True,
    #         exclude_defaults=True,
    #     )
    #     item = self._model.find(id)
    #     if item is not None:
    #         item.update(data)
    #         return item.serialize()
    #     return None

    # def delete(self, id: int):
    #     item = self._model.find(id)
    #     if item is not None:
    #         item.delete()
    #         return True
    #     return None