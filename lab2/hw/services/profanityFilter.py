import requests

API_KEY = "Nice try!"
API_LINK = "https://api.api-ninjas.com/v1/profanityfilter"


class ProfanityFilterAPI:
    @staticmethod
    def getFilteredMessage(text: str, APIKey: str) -> str:
        api_url = API_LINK + f"?text={text}"
        try:
            response = requests.get(api_url, headers={"X-Api-Key": APIKey})
            if response.status_code == requests.codes.ok:
                return response.json().get("censored")
            else:
                print("Error:", response.status_code, response.text)
                raise Exception("Error:", response.status_code, response.text)
        except Exception as e:
            print(f"An error occured: {e}")
            raise e
