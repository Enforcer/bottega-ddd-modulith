# Used Stuff Market

## Prerequisites
- Install Python 3.11
- Install docker & have its deamon up'n'running

## Start up
```bash
# Create virtual environment and install dependencies
python3.12 -m venv ve312
source ve312/bin/activate
pip install -r requirements.txt

docker compose up

# Wait several seconds and run
alembic -c used_stuff_market/db/alembic.ini upgrade head

# Run all tests (all should pass, one can be skipped)
pytest tests/
```

## Makefile commands

`make fmt` - run isort & black

`make test` - run pytest

`make run` - start FastAPI server

`run-reload` - start FastAPI server with hot code reloading on changes

## Migrations

### Upgrading to the latest version
```bash
alembic -c used_stuff_market/db/alembic.ini upgrade head
```

NOTE: Tests also use migrations, so one need to generate one during development.

### Generating new migration with auto-changes detection

```bash
alembic -c used_stuff_market/db/alembic.ini revision --autogenerate -m "MESSAGE"
```

⚠ NOTE: New schemas NEED to be added manually to the migration, e.g.
```diff
--- used_stuff_market/db/migrations/versions/562894b9762e_add_payments.py_original  2022-10-17 20:43:21.000000000 +0200
+++ used_stuff_market/db/migrations/versions/562894b9762e_add_payments.py   2022-10-17 20:01:02.000000000 +0200
@@ -18,6 +18,7 @@

 def upgrade() -> None:
     # ### commands auto generated by Alembic - please adjust! ###
+    op.execute("CREATE SCHEMA payments")
     op.create_table(
         "payments",
         sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
```

