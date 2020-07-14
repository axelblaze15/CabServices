from django.http.response import JsonResponse

def _send(data, status_code):
    return JsonResponse(data=data, status=status_code)


def send_200(data, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 200)