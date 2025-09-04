import requests
from settings import platform_url, headers

params = {
    "companyName": "qa_smoke"
}

payload = {
    "status": "approved",
    "delete_personal_data": True
}


def get_clients_id(platform_url, params, headers):
    """
    Запрос на получение списка тестовых клиентов по определённому названию

    :param platform_url: url препрода платформы (IAM)
    :param params: qwery параметры запроса, указывается название компании для поиска тестовых клиентов
    :param headers: заголовок с токеном авторизации
    :return: список всех клиентов с определённым названием компании
    """

    try:
        # отправка GET-запроса, возвращение списка клиентов
        return requests.get(f'{platform_url}/clients', params=params, headers=headers).json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def delete_test_client(platform_url, headers, payload, client_id):
    """
    Запрос на удаление клиента

    :param platform_url: url препрода платформы (IAM)
    :param headers: заголовок с токеном авторизации
    :param payload: словрь с данными для подтверждения удаления клиента
    :param client_id: id удаляемого клиента
    :return: в случае успеха возвращает True для подсчёта удалённых клиентов
    """

    try:
        # отправка PATCH-запроса на удаление клиента
        response = requests.patch(f'{platform_url}/clients/{client_id}/delete_request', headers=headers, json=payload)

        # проверка успешности запроса
        response.raise_for_status()

        # в случае успеха - сообщение, что запрос на удаление клиента выполнен
        print(f"Request to delete a client with ID '{client_id}' was completed with status code {response.status_code}")
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return False

    except Exception as err:
        print(f"Other error occurred: {err}")
        return False


clients = get_clients_id(platform_url, params, headers)
clients_count = 0
for index in range(len(clients)):
    if delete_test_client(platform_url, headers, payload, clients[index]['id']):
        clients_count += 1

print(f"Total {clients_count} test clients were deleted")
