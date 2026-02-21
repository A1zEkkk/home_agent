import ollama
import logging
import time

logger = logging.getLogger("LanguageModelClient")


class LanguageModelClient:
    """
    Наша модель.
    1) инициализируем имя нашей модели, которая запущена на ollama serve на 127.0.0.1:11434
    2) Указываем наш сервисный промпт, который указан в json

    Функция route позволяет определить сервис, к которому будет передан запрос
    """

    def __init__(self, model_name: str, router_prompt: str):
        self.model = model_name
        self.router_prompt = router_prompt
        self.client = ollama.Client()

        logger.info(f"Router client initialized | model={self.model}")
        #В будущем добавить путь до модели, когда будем раскидывать по контейнерам
    def route(self, prompt: str) -> str:
        start_time = time.time()
        # создаём новый клиент на каждый запрос
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.router_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )

            content = response["message"]["content"].strip()

            logger.info(
                f"Routing result | service={content} | time={round(time.time() - start_time, 3)}s"
            )

            return content
        except Exception:
            logger.exception("Routing failed")
            raise