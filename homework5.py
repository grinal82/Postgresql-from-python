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
        cur.execute(
            "SELECT id FROM clients where first_name = %s and last_name = %s;",
            (first_name, last_name))
        client_id = cur.fetchone()

    # inserting client_id(selected above) and phone_number (based on user's input)
        cur.execute(
            " INSERT INTO phone(client_id, phone_number) VALUES(%s,%s);",
            (client_id, phone)
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


def add_phone(conn, first_name, last_name, phone):
    with conn.cursor() as cur:
        # selecting id to insert into phone table's client_id to ensure the phone number is added to the same person
        cur.execute(
            "SELECT id FROM clients where first_name = %s and last_name = %s;",
            (first_name, last_name))
        client_id = cur.fetchone()
    # print(cur.fetchone())
        cur.execute(
            "INSERT INTO phone(client_id, phone_number) VALUES(%s,%s);",
            (client_id, phone),
        )
        conn.commit()


def change_client(
        conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM clients where first_name = %s and last_name = %s;",
            (first_name, last_name))

        client_id = cur.fetchone()

    # Updating the existing client by changing his/her email
    # (the only option to change as the phone numbers might be multiple and there's no need to change)
        cur.execute(
            """ UPDATE clients
            SET email = %s where id = %s;""",
            (email, client_id)
        )
        conn.commit()


def delete_phone(conn, first_name, last_name, phone):
    # Deleting phone based on user's input of the first and last name of the client
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM clients where first_name = %s and last_name = %s;",
            (first_name, last_name)
        )

        client_id = cur.fetchone()

        cur.execute(
            "DELETE from phone where client_id = %s and phone_number = %s;",
            (client_id, phone)
        )
        conn.commit()


def delete_client(conn, first_name, last_name):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM clients where first_name = %s and last_name = %s;",
            (first_name, last_name))
        client_id = cur.fetchone()
    # Deleting from phone talbe first as it has bindings to clients table
        cur.execute(
            "DELETE FROM phone where client_id = %s;", (client_id)
        )
    # Deleting from clients table based on id we figured out selecting by first name and second name
        cur.execute(
            "DELETE FROM clients where id = %s;", (client_id)
        )
        conn.commit()


def find_client(conn, first_name, last_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT first_name, last_name, email, phone_number FROM clients c FULL JOIN phone p on c.id = p.client_id 
            WHERE first_name =%s and last_name =%s;""", (first_name, last_name))
        print(cur.fetchall())


def main():
    with psycopg2.connect(database="clients_db", user="postgres", password="") as conn:
        while True:
            command = input(
                """Введите команду: 
                c  - create database 
                a  - add_client 
                ap - add_phone
                ch - change_client 
                dp - delete_phone 
                dc - delete_client 
                f  - find_client
                q  - EXIT: """
            )
            if command == "c":
                create_db(conn)
            elif command == "a":
                first_name = input("Введите имя: ")
                last_name = input("Введите фамилию: ")
                email = input("Введите и-мэйл: ")
                phone = input("Введите номер телефона: ")
                add_client(conn, first_name, last_name, email, phone)
            elif command == "ap":
                first_name = input("Введите имя искомого человека: ")
                last_name = input("Введите фамилию искомого человека: ")
                phone = input("Введите номер телефона ДЛЯ ДОБАВЛЕНИЯ: ")
                add_phone(conn, first_name, last_name, phone)
            elif command == "ch":
                first_name = input("Введите имя искомого человека: ")
                last_name = input("Введите фамилию искомого человека: ")
                email = input("Введите НОВЫЙ и-мэйл: ")
                change_client(conn, first_name, last_name, email)
            elif command == "dp":
                first_name = input("Введите имя искомого человека: ")
                last_name = input("Введите фамилию искомого человека: ")
                phone = input(
                    "Введите номер телефона, который хотите УДАЛИТЬ: ")
                delete_phone(conn, first_name, last_name, phone)
            elif command == "dc":
                first_name = input("Введите имя искомого человека: ")
                last_name = input("Введите фамилию искомого человека: ")
                delete_client(conn, first_name, last_name)
            elif command == "f":
                first_name = input("Введите имя искомого человека: ")
                last_name = input("Введите фамилию искомого человека: ")
                find_client(conn, first_name, last_name)
            else:
                break
    conn.close()


if __name__ == "__main__":
    main()
