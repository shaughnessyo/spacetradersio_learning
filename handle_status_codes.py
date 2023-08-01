from data_decode import data_decode, error_decode



# response = extract_resources.sync_detailed(
#     self.ship.symbol, json_body=ext_res, client=client


def handle_status_codes(response, endpoint):
    """
    this is too minimal and also i want them in postgresql without modifying the generated api calls just to avoid
    future headaches and a small amount of automation

    :param response:
    :param endpoint:
    :return:
    """
    if response.status_code in [200, 201]:
        print(data_decode(response.content))
        pass
    else:
        print(error_decode(response))



if response.status_code in [200, 201]:
    #todo this needs to get connected to whatever the
    # api call is like action_success -> print(action)
    # right now these things are too entwined
    print("mining from survey")
    # create_survey_response = data_decode(response.content)
    extract_return = data_decode(response.content)
    print(
        f"{extract_return['extraction']['shipSymbol']} mined {extract_return['extraction']['yield']['units']} "
        f"units of {extract_return['extraction']['yield']['symbol']}")
    print(f"cooldown: {extract_return['cooldown']['totalSeconds']} seconds")
    self.ship.update_current_cargo()
else:
    error_response = error_decode(response.content)
    print(error_response)
pass

