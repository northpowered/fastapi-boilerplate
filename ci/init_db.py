from piccolo.engine.postgres import PostgresEngine
import asyncio
dsn: str = "postgresql://test:test@127.0.0.1:5432/test?sslmode=disable"

engine = PostgresEngine(
    config={
        'dsn': dsn,
    }
)
username: str = 'test3'
database_name = 'test'
asyncio.run(engine.run_ddl(
    f"create user {username} with password '{username}'"))
asyncio.run(engine.run_ddl(
    f"grant all on database {database_name} to {username};"))
asyncio.run(engine.run_ddl(f"grant all on schema public to {username};"))
asyncio.run(engine.run_ddl(
    f"grant ALL ON ALL tables in schema public TO {username};"))
asyncio.run(engine.run_ddl(f"alter database test owner to {username};"))
asyncio.run(engine.run_ddl(f"alter schema public owner to {username};"))
