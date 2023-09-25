import json
import psycopg2

database = 'note_app'
user = 'postgres'
host = 'localhost'
password = '1z1j-v1ts-fijX'
port = 5432

connection = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

cursor = connection.cursor()



with open('data/quotes.json', 'r') as fh:
    quotes_data = json.load(fh)

with open('data/authors.json', 'r') as fh:
    authors_data = json.load(fh)


def fill_tags_for_quotes():
    sql_tags_for_quotes = "INSERT INTO quotes_quote_tags (quote_id, tag_id) VALUES (%s, %s)"

    sql_tags = "SELECT id, tagname FROM tags_tag"
    cursor.execute(sql_tags)
    all_tags = cursor.fetchall()

    sql_quotes = "SELECT id, quote FROM quotes_quote"
    cursor.execute(sql_quotes)
    all_quotes = cursor.fetchall()

    for element in quotes_data:
        quote = element.get('quote')
        tags = element.get('tags')

        for q in all_quotes:
            if q[1] == quote:
                quote_id = q[0]


                for tag in tags:
                    # print(f"tags for quote_id {quote_id}")
                    for id in all_tags:
                        if tag == id[1]:
                            # print(id[0])
                            cursor.execute(sql_tags_for_quotes, (quote_id, id[0]))
                            connection.commit()





def fill_quotes():
    sql_quotes = "INSERT INTO quotes_quote (quote, author_id) VALUES (%s, %s)"
    select_query = "SELECT id, fullname FROM authors_author"

    cursor.execute(select_query)
    author_ids = cursor.fetchall()

    for element in quotes_data:
        author = element.get('author')
        quote = element.get('quote')

        matching_author_id = None
        for author_id in author_ids:
            if author_id[1] == author:
                matching_author_id = author_id[0]
                break

        if matching_author_id is not None:
            cursor.execute(sql_quotes, (quote, matching_author_id))
            connection.commit()


def fill_tags():
    tags = []
    sql_tags = "INSERT INTO tags_tag (tagname) VALUES (%s) "

    for element in quotes_data:
        for tag in element.get('tags'):
            tags.append(tag)

    for tag in set(tags):
        cursor.execute(sql_tags, (tag, ))

    connection.commit()


def fill_authors():
    sql_authors = "INSERT INTO authors_author (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s)"

    for element in authors_data:
        fullname = element.get('fullname')
        born_date = element.get('born_date')
        born_location = element.get('born_location')
        description = element.get('description')

        cursor.execute(sql_authors, (fullname, born_date, born_location, description))
        connection.commit()


if __name__ == '__main__':
    fill_tags()
    fill_authors()
    fill_quotes()
    fill_tags_for_quotes()


    cursor.close()
    connection.close()