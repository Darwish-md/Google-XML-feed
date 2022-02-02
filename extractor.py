import sqlite3
from sqlite3 import Error
from xml_exporter import generate_xml

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_products(conn):
    """
    Query all rows in the product, manufacturer, product_description, product_image tables 
    where the status is not zero and orders the result in ascending order by id
    :param conn: the Connection object
    :return: rows (lists of tuples)
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT product.product_id, product_description.name, description, ean, CAST(quantity AS INTEGER), "
        "CAST(price AS INTEGER), product.image, product_image.image, manufacturer.name FROM product "
        "join manufacturer on product.manufacturer_id = manufacturer.manufacturer_id "
        "join product_description on product.product_id = product_description.product_id "
        "join product_image on product.product_id = product_image.product_id "
        "WHERE status <> '0' "
        "order by CAST(1 AS INTEGER)")

    rows = cur.fetchall()

    return rows


def main():
    database = r"E:\FirstTask\db\data.sqlite"

    # create database connection
    conn = create_connection(database)
    # query the records from the database
    rows = select_all_products(conn)
    # export the records to the generated feed.xml file 
    generate_xml("feed.xml", rows)
    # close connection to the databse
    conn.close()


if __name__ == '__main__':
    main()
