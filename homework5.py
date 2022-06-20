import psycopg2


def create_db(conn):
    # Dropping existing talbes if needed
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP TABLE phone;
            DROP TABLE clients;
        """
        )
        # Creating new talbes with phone table related to clients table (one to many); phone references on clients(id)
        cur.execute(
            "CREATE TABLE IF NOT EXISTS clients(id SERIAL PRIMARY KEY, first_name VARCHAR(40), last_name VARCHAR(40), email VARCHAR(40));"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS phone(id SERIAL PRIMARY KEY, client_id INTEGER REFERENCES clients(id), phone_number VARCHAR(40));"
        )
        conn.commit()


def add_client(conn, first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute(
            # inserting data into "clients" table based on the user's input
            "INSERT INTO clients(first_name, last_name, email) VALUES(%s,%s,%s);",
            (first_name, last_name, email),
        )
        conn.commit()
        # selecting id to insert into phone table's client_id to ensure relations to clients table
        client_id = cur.execute(
            """
                    SELECT id FROM clients where first_name = %s and last_name = %s RETURNING id;
                    """,
            (first_name, last_name),
        )
        print(cur.fetchall())
        # conn.commit()
        # inserting client_id(selected above) and phone_number (based on user's input)
        cur.execute(
            " INSERT INTO phone(client_id, phone_number) VALUES(client_id = %s, phone_number = %s);",
            (client_id, phone),
        )
        conn.commit()

        # checking out the resulting outcome

        cur.execute(
            """
                    SELECT * FROM clients;
                    """
        )
        print(cur.fetchall())
        cur.execute(
            """
                    SELECT * FROM phone;
                    """
        )
        print(cur.fetchall())


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO phone(client_id, phone_number)  VALUES(%s,%s);",
            (client_id, phone),
        )
        conn.commit()


def change_client(
    conn, client_id, first_name=None, last_name=None, email=None, phones=None
):
    pass


def delete_phone(conn, client_id, phone):
    pass


def delete_client(conn, client_id):
    pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


def main():
    with psycopg2.connect(database="clients_db", user="postgres", password="") as conn:
        while True:
            command = input(
                """Введите команду: 
                c-create database, 
                a-add_client, 
                t-add_phone,
                ch-change_client, 
                dp-delete_phone, 
                dc-delete_client, 
                f-find_client: """
            )
            if command == "c":
                create_db(conn)
            elif command == "a":
                first_name = input("Введите имя: ")
                last_name = input("Введите фамилию: ")
                email = input("Введите и-мэйл: ")
                phone = input("Введите номер телефона: ")
                add_client(conn, first_name, last_name, email, phone)
            elif command == "t":
                first_name = input("Введите имя искомого человека: ")
                last_name = input("Введите фамилию искомого человека: ")
                phone = input("Введите номер телефона для добавления: ")
                with conn.cursor() as cur:
                    client_id = cur.execute(
                        """
                    SELECT id FROM clients where first_name = %s and last_name = %s;
                    """,
                        (first_name, last_name),
                    )
                    add_phone(conn, client_id, phone)
            elif command == "ch":
                change_client(conn)
            elif command == "dp":
                delete_client(conn)
            elif command == "dc":
                delete_client(conn)
            elif command == "f":
                find_client(conn)

        # conn.close()


if __name__ == "__main__":
    main()
