import os, json, pprint, uuid
import vertexai
from google import genai
from google.genai.types import (
    HttpOptions, GenerateContentConfig,
    Part, UserContent, ModelContent
)
from dotenv import load_dotenv

load_dotenv()
project = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")

vertexai.init(project=project, location=location, staging_bucket=f'gs://{project}')
# MODEL="gemini-2.5-pro-exp-03-25"
MODEL="gemini-2.0-flash-lite"
# MODEL="gemini-2.0-flash"



def generate_response(system_instruction, contents, response_schema, model):
    client = genai.Client(vertexai=True, project=project, location=location, http_options=HttpOptions(api_version='v1'))
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.4,
            response_mime_type='application/json',
            response_schema=response_schema,
        )
    )
    return '\n'.join(
        [p.text for p in response.candidates[0].content.parts if p.text]
    )

def _generate_plan(goal):
    system_instruction = """
あなたはプロのイベントプランナーです。以下のタスクに取り組んでください。

[タスク]
A. 与えられた[goal]を達成するためのイベントコンテンツを作成してください。

[フォーマットの指示]
日本語で提出してください。マークダウンは不要です。出力は以下の3つの項目で構成されます。
"title": イベントの短いタイトル
"summary": イベントの概要（3文）
"timeline": イベントのタイムライン（期間や内容など）（箇条書き）
    """
    response_schema = {
        "type":"object",
        "properties":{
            "title":{"type":"string"},
            "summary":{"type":"string"},
            "timeline":{"type":"string"}
        },
        "required":["title", "summary", "timeline"]
    }
    parts = []
    parts.append(Part.from_text(text=f'[goal]\n{goal}'))
    contents = [UserContent(parts=parts)]
    return generate_response(system_instruction, contents, response_schema, MODEL)

def generate_plan(goal:str) -> dict:
    response = _generate_plan(goal)
    return json.loads(response)


if __name__ == "__main__":
    response_schema = {
        "type":"object",
        "properties": {
            "greeting":{"type":"string"},
        },
        "required":["greeting"]
    }
    system_instruction="""
ネットショップの仮想店員として、丁寧で、かつ、フレンドリーな雰囲気の挨拶を返してください。
架空の商品名などは含めないこと。
"""
    contents = 'こんにちは、中井です。何か、おすすめはありますか？'
    # print(generate_response(system_instruction, contents, response_schema, model))
    goal = '新しい商品を紹介するイベントを企画したい。'
    plan = generate_plan(goal)
    print('---')
    print(plan)
    # print('title:', plan['title'])
    # print('summary:', plan['summary'])
    # print('timeline:', plan['timeline'])
    print('---')
