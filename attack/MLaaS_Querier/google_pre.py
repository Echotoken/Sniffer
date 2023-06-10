import googleapiclient.discovery

def google_predictor(data, link1, link2):
    service = googleapiclient.discovery.build('ml', 'v1')

    name = 'projects/{}/models/{}/versions/{}'.format("steel-bliss-343009", link1, link2)
    response = service.projects().predict(
        name=name,
        body={'instances': data}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])
    else:
        return response['predictions']