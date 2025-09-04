import requests
from settings import billing_url, headers


params = {"int_name": "test_manual_qa"}


def get_metrics_id(billing_url, headers, params):
    """
    Запрос на получение списка тестовых метрик по определённому названию

    :param billing_url: url стенда или препрода биллинга
    :param headers: заголовок с токеном авторизации
    :param params: qwery параметры запроса, указывается название тестовой фичи
    :return: список всех метрик с определённым названием
    """

    try:
        # отправка GET-запроса, возвращение списка метрик
        return requests.get(f'{billing_url}/v3/statistics/metrics', headers=headers, params=params).json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def delete_test_metric(billing_url, headers, metric_id):
    """
    Запрос на удаление тестовой метрики

    :param billing_url: url стенда или препрода биллинга
    :param headers: заголовок с токеном авторизации
    :param metric_id: id удаляемых метрик
    :return: в случае успеха возвращает True для подсчёта удалённых метрик
    """

    try:
        # отправка DELETE-запроса на удаление метрики
        response = requests.delete(f'{billing_url}/v3/statistics/metrics/{metric_id}', headers=headers)

        # проверка успешности запроса
        response.raise_for_status()

        # в случае успеха - сообщение, что фича удалена
        print(f"Metric with id '{metric_id}' was deleted with status code: {response.status_code}")
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return False

    except Exception as err:
        print(f"Other error occurred: {err}")
        return False


metrics = get_metrics_id(billing_url, headers, params)
metrics_count = 0
for index in range(len(metrics)):
    if delete_test_metric(billing_url, headers, metrics[index]['id']):
        metrics_count += 1

print(f"Total {metrics_count} metrics were deleted")
