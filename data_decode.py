import ast


# TODO this needs to handle rate limit error returns-- wait i don't think so
def data_decode(data: bytes) -> dict:
    """
    generic function to decode api call data
    :param data: bytes encoded data returned from an api call
    :return: unnested dict of data
    """
    data = data.decode()
    data = ast.literal_eval(data)
    # print(data)

    data = data['data']

    return data


# this seems like a stupid solution but maybe
# content=b'{"error":{"message":"Ship action failed. Ship is not currently in orbit at X1-JF24-23225F.","code":4236,"data":{"waypointSymbol":"X1-JF24-23225F"}}}'

def error_decode(error:bytes):
    error = error.decode()
    error = ast.literal_eval(error)
    print(error['error']['message'])
    # error = error['error']
    # return error

