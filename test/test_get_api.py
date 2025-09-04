import requests

def test_get_api():
    from api.api_discovery.ontimize_api import getMetaData
    tables = getMetaData(include_attributes=True)
    for endpoint in tables.resources:
        print(endpoint)
        response = requests.get(f"http://localhost:5656/api/{endpoint}?page%5Boffset%5D=0&page%5Blimit%5D=1")
        assert response.status_code == 200
        assert "data" in response.json()

        for item in response.json()["data"]:
            assert "id" in item
            assert "attributes" in item

if __name__ == "__main__":
    test_get_api()