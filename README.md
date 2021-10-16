# FastAPI Cassandra Demo

A sample python application based on FasiAPI and Cassandra database.

## Development

Start Cassandra database

```shell
# With cassandra it will take a few minutes to checking that it started up correctly
# Wating for it complete started
make start-db
```

Start application

```shell
make start
```

Run Unit test

```shell
make test
```

## Referance

### Cassandra database

https://docs.datastax.com/en/cql-oss/3.x/cql/cql_reference/cqlshShow.html

**Working with cassandra database.**

Login to cassandra db 

```shell
cqlsh -u cassandra
```

Show the version

```shell
SHOW VERSION
```

Get keyspaces info

```shell
SELECT * FROM system_schema.keyspaces;
```

Get tables info

```shell
SELECT table_name FROM system_schema.tables WHERE keyspace_name = 'keyspace_organization_db' AND table_name = 'organizations';
```

Get table info

```shell
SELECT * FROM system_schema.columns WHERE keyspace_name = 'keyspace_organization_db' AND table_name = 'organizations';
```

Select table data

```shell
SELECT * FROM keyspace_organization_db.organizations;
```

Drop table

```shell
DROP TABLE keyspace_organization_db.organizations;
```
