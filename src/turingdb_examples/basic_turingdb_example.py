from turingdb import TuringDB

def hello_turingdb():
    return "Hello from TuringDB Examples!"

def create_turingdb_client():
    client = TuringDB()
    return client

if __name__ == "__main__":
    print(hello_turingdb())
    create_turingdb_client()