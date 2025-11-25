import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="smartbooking",
        user="postgres",
        password="4njeliad"
    )


# ini nyoba bua comit ke github dari vscode
# PROJECT ANJ