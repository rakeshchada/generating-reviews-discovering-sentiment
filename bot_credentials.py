
__all__ = ["provide_key"]

def provide_key(key_name):
    all_keys = {
        "consumer_key": "your_secret",
        "consumer_secret": "your_secret",
        "access_token": "your_secret",
        "access_token_secret": "your_secret"
    }
    try:
        return all_keys[key_name]
    except:
        print("Invalid key name")
