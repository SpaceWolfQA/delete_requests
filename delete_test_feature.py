import requests
from settings import billing_url, headers


params = {"name_en": "test_manual_qa"}


def get_features_id(billing_url, headers, params):
    """
    Запрос на получение списка тестовых фичей по определённому названию

    :param billing_url: url стенда или препрода биллинга
    :param params: qwery параметры запроса, указывается название тестовой фичи
    :param headers: заголовок с токеном авторизации
    :return: список всех фичей с определённым названием
    """

    try:
        # отправка GET-запроса, возвращение списка фич
        return requests.get(f'{billing_url}/features', headers=headers, params=params).json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def delete_test_feature(billing_url, headers, feature_id):
    """
    Запрос на удаление тестовой фичи

    :param billing_url: url стенда или препрода биллинга
    :param headers: заголовок с токеном авторизации
    :param feature_id: id удаляемых фич
    :return: в случае успеха возвращает True для подсчёта удалённых фич
    """

    try:
        # отправка DELETE-запроса на удаление фичи
        response = requests.delete(f'{billing_url}/features/{feature_id}', headers=headers)

        # проверка успешности запроса
        response.raise_for_status()

        # в случае успеха - сообщение, что фича удалена
        print(f"Feature with id '{feature_id}' was deleted with status code: {response.status_code}")
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return False

    except Exception as err:
        print(f"Other error occurred: {err}")
        return False


features = get_features_id(billing_url, headers, params)
features_count = 0
for index in range(len(features)):
    if delete_test_feature(billing_url, headers, features[index]['id']):
        features_count += 1

print(f"Total {features_count} features were deleted")
