import hashlib
import datetime

class Intcomex():

    def __init__(self):
        config = {}
        with open('config.properties', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

        self.api_key = config['intcomex_api_key']
        self.user_key = config['intcomex_user_key']

    def generate_signature(self, api_key: str, user_key: str) -> tuple[str, str]:
        """
        Generate the signature required for Intcomex API authentication.

        Args:
            api_key (str): The public API key provided by Intcomex.
            user_key (str): The private User Key provided by Intcomex.

        Returns:
            tuple: (signature, utc_timestamp)
        """
        # 1. Generate UTC timestamp (ISO 8601 format, e.g., 2025-08-19T13:45:30Z)
        utc_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # 2. Build signing key (comma-separated string)
        signing_key = f"{api_key},{user_key},{utc_timestamp}"

        # 3. Apply SHA-256 hashing
        signature = hashlib.sha256(signing_key.encode("utf-8")).hexdigest()

        return signature, utc_timestamp


    def get_info_from_intcomex(self):
        signature, timestamp = self.generate_signature(self.api_key, self.user_key)
        print(f"UTC Timestamp: {timestamp}")
        print(f"Signature: {signature}")

        #apiKey=c6bdc293-042b-4dd6-8d7f-aa67a555cff8&utcTimeStamp=2015-02-26T15:06:18Z&signature=2fa7ddc441f45744d3c7253f18a2953377428cc0b25043f39724115f403bbcfc&runAsTask=false
        bearer = f"apiKey={self.user_key}&utcTimeStamp={timestamp}&signature={signature}&runAsTask=false"
        print(bearer)
        import requests

        url = "https://intcomex-prod.apigee.net/v1/GetProducts?skusList=1000,1001,1002&locale=en"

        payload = ""
        headers = {
            "Authorization": "Bearer " + bearer,
            "Content-Type": "application/json"
        }

        response = requests.request("GET", url, json=payload, headers=headers)

        print(response.text)