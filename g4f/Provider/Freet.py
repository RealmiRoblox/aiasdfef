import json

import requests

from ..typing import Any, CreateResult
from .base_provider import BaseProvider


class Freet(BaseProvider):
    url = "https://biwjo6q8.freet.to"
    supports_stream = True

    supports_gpt_35_turbo = True
    supports_gpt_35_turbo_16k = True
    supports_gpt_35_turbo_16k_0613 = True
    supports_gpt_4 = True
    supports_gpt_4_0613 = True
    supports_gpt_4_32k = True
    supports_gpt_4_32k_0613 = True

    working = False


    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool,
        **kwargs: Any,
    ) -> CreateResult:
        active_servers = [
            "https://chat-gpt-next-web-squallstar.vercel.app",
        ]
        server = active_servers[kwargs.get("active_server", 0)]
        headers = {
            "authority": f"{server}".replace("https://", ""),
            "authorization:": "Bearer nk-Tmd-Ni-xiang-Gou=Sb-90807rqHgl8b3jrNkSjEvt90EiMEoCsbKJ2kggV1iHzTKEDWv1tcgazgdsuw0S4pZ1W",
            "accept": "text/event-stream",
            "accept-language": "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3,fa=0.2",
            "content-type": "application/json",
            "origin": f"{server}",
            "referer": f"{server}/",
            "x-requested-with": "XMLHttpRequest",
            'plugins': '0',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'usesearch': 'false',
            'x-requested-with': 'XMLHttpRequest'
        }

        json_data = {
            "messages": messages,
            "stream": stream,
            "model": model,
            "temperature": kwargs.get("temperature", 0.5),
            "presence_penalty": kwargs.get("presence_penalty", 0),
            "frequency_penalty": kwargs.get("frequency_penalty", 0),
            "top_p": kwargs.get("top_p", 1),
        }

        session = requests.Session()
        # init cookies from server
        session.get(f"{server}/")

        response = session.post(
            f"{server}/api/openai/v1/chat/completions",
            headers=headers,
            json=json_data,
            stream=stream,
        )
        if response.status_code == 200:
            if stream == False:
                json_data = response.json()
                if "choices" in json_data:
                    yield json_data["choices"][0]["message"]["content"]
                else:
                    raise Exception("No response from server")
            else:
                
                for chunk in response.iter_lines():
                    if b"content" in chunk:
                        splitData = chunk.decode().split("data:")
                        if len(splitData) > 1:
                            yield json.loads(splitData[1])["choices"][0]["delta"]["content"]
                        else:
                            continue
        else:
            raise Exception(f"Error {response.status_code} from server : {response.reason}")
        
    @classmethod
    @property
    def params(cls):
        params = [
            ("model", "str"),
            ("messages", "list[dict[str, str]]"),
            ("stream", "bool"),
            ("temperature", "float"),
            ("presence_penalty", "int"),
            ("frequency_penalty", "int"),
            ("top_p", "int"),
            ("active_server", "int"),
        ]
        param = ", ".join([": ".join(p) for p in params])
        return f"g4f.provider.{cls.__name__} supports: ({param})"
