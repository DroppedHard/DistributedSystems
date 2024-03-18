import requests

API_LINK = "https://foaas.dev"

class FOaaS:
    @staticmethod
    def getOperations() -> dict:
        api_url = API_LINK + "/operations"
        try:
            response = requests.get(api_url)
            if response.status_code == requests.codes.ok:
                return {endpoint["name"]: endpoint for endpoint in response.json()}
            else:
                print("Error:", response.status_code, response.text)
        except Exception as e:
            print(f"An error occured: {e}")
            raise e

    @staticmethod
    def getFOaaSEndpoint(url: str) -> dict[str, str]:
        api_url = API_LINK + url
        try:
            response = requests.get(api_url, headers={"Accept": "application/json"})

            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                print("Error:", response.status_code, response.text)
        except Exception as e:
            print(f"An error occured: {e}")
            raise e
