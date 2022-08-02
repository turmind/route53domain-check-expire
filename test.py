from main import lambda_handler
from dotenv import find_dotenv, load_dotenv

def main():
    load_dotenv(find_dotenv('.env'))
    lambda_handler("123", "123")

if __name__ == "__main__":
    main()