import requests
from settings import billing_url, headers


params = {"name_en": "test_manual_qa"}


def get_plans_id(billing_url, headers, params):
    """
    Запрос на получение списка тестовых планов по определённому названию

    :param billing_url: url стенда или препрода биллинга
    :param headers: заголовок с токеном авторизации
    :param params: qwery параметры запроса, указывается название тестовой фичи
    :return: список всех метрик с определённым названием
    """

    try:
        # отправка GET-запроса, возвращение списка планов
        return requests.get(f'{billing_url}/v3/plans', headers=headers, params=params).json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def delete_test_plan(billing_url, headers, plan_id):
    """
    Запрос на удаление тестового плана

    :param billing_url: url стенда или препрода биллинга
    :param headers: заголовок с токеном авторизации
    :param plan_id: id удаляемого плана
    :return: в случае успеха возвращает True для подсчёта удалённых метрик
    """

    try:
        # отправка DELETE-запроса на удаление плана
        response = requests.delete(f'{billing_url}/v3/plans/{plan_id}', headers=headers)

        # проверка успешности запроса
        response.raise_for_status()

        # в случае успеха - сообщение, что план удалён
        print(f"Plan with id '{plan_id}' was deleted with status code: {response.status_code}")
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return False

    except Exception as err:
        print(f"Other error occurred: {err}")
        return False


plans = get_plans_id(billing_url, headers, params)
print(plans)
plans_count = 0
for index in range(len(plans)):
    if delete_test_plan(billing_url, headers, plans[index]['id']):
        plans_count += 1

print(f"Total {plans_count} plans were deleted")
