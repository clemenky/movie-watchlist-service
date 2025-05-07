import zmq
import json
from watchlist_client import API_ENDPOINTS


def process_request(request):
    if not isinstance(request, dict):
        return {'status': 'error', 'message': 'Request must be a JSON object'}
    
    request_type = request.get('type')
    if request_type == 'query':
        endpoint = request.get('endpoint')
        if endpoint not in API_ENDPOINTS:
            return {'status': 'error', 'message': 'Unknown endpoint: {endpoint}'}
        endpoint_info = API_ENDPOINTS[endpoint]
        required_params = endpoint_info.get('required_params', [])
        params = request.get('params', {})

        if not isinstance(params, dict):
            return {'status': 'error', 'message': '\'params\' must be a dictionary'}
        
        missing_params = [p for p in required_params if not params.get(p)]
        if missing_params:
            return {'status': 'error', 'message': f'Missing required parameters: {', '.join(missing_params)}'}
        
        function = endpoint_info['function']
        try:
            result = function(*(params[p] for p in required_params))
            return {'status': 'ok', 'result': result}
        except Exception as e:
            return {'status': 'error', 'message': f'Function call failed: {str(e)}'}

    else:
        return {'status': 'error', 'message': 'Unknown request type'}
        
def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5556')

    print('Microservice movie-watchlist-service is running...')

    try:
        while True:
            message = socket.recv_string()
            print(f'Message received: {message}')

            try:
                request = json.loads(message)
                response = process_request(request)
            except json.JSONDecodeError:
                response = {'status': 'error', 'message': 'Invalid JSON'}

            socket.send_string(json.dumps(response))


    finally:
        socket.close()
        context.term()
        print('Microservice movie-info-service shut down.')


if __name__ == '__main__':
    main()

# Example request object:
# {
#     'type': 'query',
#     'endpoint': 'search_by_title',
#     'params': {
#         'title': 'Titanic'
#     }
# }