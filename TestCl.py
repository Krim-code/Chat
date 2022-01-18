import base64
def encoded_messege(sample_string):
    sample_string_bytes = sample_string.encode("utf-8")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("utf-8")
    return base64_string

def decoded_messege(base64_string):
    base64_string = " R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA=="
    base64_bytes = base64_string.encode("utf-8")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("utf-8")
    return sample_string