import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """指定された都市の現在の天気予報を取得します。

    Args:
        city (str): 天気予報を取得する都市の名前。
    Returns:
        dict: ステータスと結果またはエラーメッセージ。
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city: str) -> dict:
    """指定された都市の現在の時刻を返します。

    Args:
        city (str): 現在の時刻を取得する都市の名前。

    Returns:
        dict: ステータスと結果またはエラーメッセージ。
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = Agent(
    name = "weather_timme_agent",
    model="gemini-2.0-flash",
    description=(
        "都市の時間と天気に関する質問に答えるエージェント。"
    ),
    instruction=(
        "あなたは、都市の時間と天気に関する質問に答えるエージェントです。"
        "ユーザーからの質問に対して、適切な情報を提供してください。"
        "質問は、都市名を含む場合があります。"
        "質問が不明な場合は、ユーザーに尋ねてください。"
    ),
    tools=[get_weather, get_current_time],
)
