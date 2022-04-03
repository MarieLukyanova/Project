import vk_api


def ID(id):
    login, password = 'ваш телефон', 'ваш пароль'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id)
    return response[0]['id']


def Friends(id):
    login, password = 'ваш телефон', 'ваш пароль'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.friends.get(user_id=id)
    return response['count']


def Photos(id):
    login, password = 'ваш телефон', 'ваш пароль'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id, fields='counters')
    return response[0]['counters']['photos']


def Avatar(id):
    login, password = 'ваш телефон', 'ваш пароль'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id, fields='photo_200')
    return response[0]['photo_200']