# coding=utf8

from contextlib import contextmanager

from psycopg2.extras import NamedTupleCursor
from psycopg2.pool import ThreadedConnectionPool

pg_pool = ThreadedConnectionPool(minconn=1, maxconn=10, dbname='auth_manager', user='interview', password='interview')


@contextmanager
def pool_execute(is_commit=False):
    conn = pg_pool.getconn()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    yield cur
    if is_commit:
        conn.commit()
    cur.close()
    pg_pool.putconn(conn)


if __name__ == '__main__':
    pass
