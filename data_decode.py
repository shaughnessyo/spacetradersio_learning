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
