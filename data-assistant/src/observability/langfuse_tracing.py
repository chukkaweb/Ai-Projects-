import os

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


class LangfuseLogger:
    def __init__(self):
        self.enabled = False

        try:
            self.client = Langfuse(
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                host=os.getenv(
                    "LANGFUSE_HOST",
                    "https://cloud.langfuse.com"
                )
            )

            self.enabled = True

            print("✅ Langfuse Connected")

        except Exception as e:

            print(f"Langfuse Disabled : {e}")

            self.client = None

    def log_llm_call(
        self,
        prompt,
        response,
        model="gemini-2.5-flash",
        metadata=None
    ):

        if not self.enabled:
            return

        try:

            trace = self.client.trace(
                name="LLM Call",
                metadata=metadata or {}
            )

            trace.generation(
                name="Gemini",
                model=model,
                input=prompt,
                output=response
            )

            self.client.flush()

        except Exception as e:
         print(e)

    def log_user_query(
        self,
        query,
        feature="Talk To Data"
    ):

        if not self.enabled:
            return

        try:

            self.client.trace(
                name="User Query",
                input=query,
                metadata={
                    "feature": feature
                }
            )

            self.client.flush()

        except Exception as e:

            print(e)

    def log_error(
        self,
        error,
        context=None
    ):

        if not self.enabled:
            return

        try:

            self.client.trace(
                name="Application Error",
                metadata={
                    "error": error,
                    "context": context or {}
                }
            )

            self.client.flush()

        except Exception as e:

            print(e)

    def log_event(
        self,
        name: str,
        metadata: dict = None
    ):
        """
        Log a non-LLM application event.

        Examples:
        - Database Insert
        - DDL Parsed
        - Batch Generated
        - Data Saved
        - Validation Passed
        """

        if not self.enabled:
              return

        try:
            self.client.trace(
                    name=name,
                    metadata=metadata or {}
                )
            self.client.flush()

        except Exception as e:
            print(f"Langfuse Event Error: {e}")


logger = LangfuseLogger()