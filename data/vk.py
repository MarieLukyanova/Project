import vk_api


def ID(id):
    vk_session = vk_api.VkApi(
        token='d3c5438ef5dcc87bec92f492246b7f27bdceee7b21d8d59cf6b497a4bf05b657ca764a7605660571ffca1')
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id)
    return response[0]['id']


def Friends(id):
    vk_session = vk_api.VkApi(
        token='d3c5438ef5dcc87bec92f492246b7f27bdceee7b21d8d59cf6b497a4bf05b657ca764a7605660571ffca1')
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id, fields='counters')
    return response[0]['counters']['friends']


def Photos(id):
    vk_session = vk_api.VkApi(
        token='d3c5438ef5dcc87bec92f492246b7f27bdceee7b21d8d59cf6b497a4bf05b657ca764a7605660571ffca1')
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id, fields='counters')
    return response[0]['counters']['photos']


def Avatar(id):
    vk_session = vk_api.VkApi(
        token='d3c5438ef5dcc87bec92f492246b7f27bdceee7b21d8d59cf6b497a4bf05b657ca764a7605660571ffca1')
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id, fields='photo_200')
    return response[0]['photo_200']


def Name(id):
    vk_session = vk_api.VkApi(
        token='d3c5438ef5dcc87bec92f492246b7f27bdceee7b21d8d59cf6b497a4bf05b657ca764a7605660571ffca1')
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id, fields='screen_name')
    return response[0]['screen_name']
