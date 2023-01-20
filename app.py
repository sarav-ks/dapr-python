from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
from dapr.clients import DaprClient
import json

with DaprClient() as d:
    req_data = {
        'productId': 1,
        'qty': 15,
        'orderId': 'order_1',
        'status': ''
    }

app = App()

@app.method(name='purchase')
def mymethod(request: InvokeMethodRequest) -> InvokeMethodResponse:
    print(request.text(), flush=True)
    resp = d.invoke_method(
        'order-receiver',
        'postorder',
        data=json.dumps(req_data),
    )

    # Print the response
    print(resp.content_type, flush=True)
    print(resp.text(), flush=True)

    return InvokeMethodResponse(b'INVOKE_RECEIVED'+resp.text(), "text/plain; charset=UTF-8")

app.run(50051)