[한국어 문서 (Korean)](#korean-documentation) | [English Documentation](#english-documentation)

<a name="korean-documentation"></a>
## 🇰🇷 Korean Documentation
# sd-batch-iterator
> **⚠️** <br>
> 이 프로젝트는 개인적으로 사용하던 도구를 정리해 공개한 것입니다.  
> 코드의 대부분은 AI를 사용해 제작하였습니다.  
> 테스트는 `webui_forge_cu124_torch24`를 기반으로 한 제한적인 환경에서만 진행되었으며,  
> 모든 환경에서의 정상 동작을 보장하지 않습니다.  
> 유지보수 및 지원은 보장하지 않습니다.  
> 사용에 따른 문제나 손해에 대해 책임지지 않습니다.  
> 필요에 따라 자유롭게 포크·수정하여 사용하셔도 됩니다.

Stable Diffusion WebUI를 위한 프롬프트 일괄 실행 및 자동화 확장 프로그램입니다.  
워크플로우 없이 SillyTavern의 감정 표현 이미지를 자동으로 생성하기 위해 제작되었습니다.  
JSON 파일에 정의된 프롬프트 목록을 순차적으로 실행하여 `txt2img` 및 `img2img` 생성을 자동화합니다.

## 주요 기능
- **모든 모드 지원**: `txt2img`와 `img2img` 탭 모두에서 스크립트로 사용 가능합니다.
- **JSON 기반 자동화**: 베이스 프롬프트와 여러 변동 프롬프트를 결합하여 대량의 이미지를 생성합니다.
- **자동 파일명 지정**: JSON에서 지정한 각 항목의 이름(`name`)을 출력 파일명의 접미사로 자동 추가합니다.
- **독립 편집기 제공**: JSON 파일(프롬프트 목록)을 쉽게 편집할 수 있는 GUI 애플리케이션(`prompt_editor_app.py`)이 포함되어 있습니다.

### 설치 방법
1. WebUI의 `Extensions` 탭으로 이동합니다.
2. `Install from URL`을 클릭합니다.
3. 이 저장소의 URL을 입력하고 `Install`을 누릅니다.
4. `Apply and restart UI`를 클릭하여 적용합니다.

## 사용법

### WebUI 스크립트 사용
1. `txt2img` 또는 `img2img` 탭의 스크립트(Script) 드롭다운에서 **sd-batch-iterator**를 선택합니다.
2. 작성된 JSON 파일을 업로드합니다.
3. 생성(Generate) 버튼을 클릭하면 목록의 모든 프롬프트에 대해 순차적으로 생성이 진행됩니다.

### 프롬프트 편집기 사용
- `prompt_editor_app.py`를 실행하여 GUI 환경에서 프롬프트 목록을 관리하고 JSON으로 저장할 수 있습니다.
- (실행 예: `python prompt_editor_app.py`)

## JSON 형식 예시
```
json
{
    "base_prompt": "masterpiece, best quality",
    "variable_prompts": [
        {"name": "red_theme", "prompt": "red hair, red eyes", "enabled": true},
        {"name": "blue_theme", "prompt": "blue hair, blue eyes", "enabled": true}
    ]
}
```

---

## 설명

- 이 확장은 별도의 워크플로우 없이 SillyTavern의 감정 표현 이미지를 자동으로 생성하기 위해 제작되었습니다.
- WebUI의 설정을 그대로 사용하며, 프롬프트만 JSON에 설정한 프롬프트로 순차 교체되어 생성이 자동으로 진행되는 방식입니다.  
  (기본 프롬프트 + 변동 프롬프트 1 >> 기본 프롬프트 + 변동 프롬프트 2 >> ...)
- WebUI에 입력된 긍정 프롬프트는 무시하고 JSON에 입력된 프롬프트를 사용합니다.
- 부정 프롬프트는 WebUI에 입력된 프롬프트를 그대로 사용합니다.
- 파일명은 변동 프롬프트 이름이 접미사로 붙어서 저장됩니다.

### `prompt_editor_app.py` 편집기 사용법
- `기본 프롬프트(공통)`에는 생성 시 모든 프롬프트에 공통으로 들어갈 프롬프트를 입력합니다.
- `이름`과 `변동 프롬프트`를 입력한 후 `추가/수정` 버튼을 누르면 `변동 프롬프트 목록`에 추가됩니다.
- `변동 프롬프트 목록`에서 프롬프트를 클릭한 후 내용을 변경하고 `추가/수정` 버튼을 누르면 내용이 수정됩니다.
- 생성 시 `변동 프롬프트`는 `기본 프롬프트(공통)` 뒤에 추가되어 합쳐지고, `변동 프롬프트`만 교체해 가며 생성이 진행됩니다.

### `test_prompts.json`

SillyTavern에 등록 가능한 28가지 표정 프롬프트가 목록에 등록되어 있습니다.  
프롬프트 내용은 아래와 같습니다.

```
name: admiration-0
prompt: slightly raised eyebrows, sparkling eyes, soft smile, gentle blush, slight awe

name: amusement-0
prompt: relaxed eyebrows, playful smile, bright eyes, lighthearted mood

name: anger-0
prompt: v-shaped eyebrows, deeply furrowed brows, glaring eyes, clenched jaw, tense face

name: annoyance-0
prompt: slanted eyebrows, narrowed eyes, slight frown, side glance, puffed cheeks

name: approval-0
prompt: natural relaxed brows, gentle smile, calm eyes, slight nod, composed face

name: caring-0
prompt: inner brows slightly raised, tender eyes, warm smile, concerned look

name: confusion-0
prompt: uneven eyebrows, one brow raised, puzzled eyes, tilted head, slightly open mouth

name: curiosity-0
prompt: raised eyebrows, wide focused eyes, intent gaze, slight lean forward

name: desire-0
prompt: half-lidded eyes, relaxed brows, intense gaze, subtle blush, parted lips

name: disappointment-0
prompt: downward brows, drooping eyelids, small frown, downcast eyes

name: disapproval-0
prompt: knit eyebrows, cold stare, flat lips, stern face

name: disgust-0
prompt: lowered brows, wrinkled nose, averted gaze, tense mouth, recoiling expression

name: embarrassment-0
prompt: uneven lowered brows, deep blush, shy face, looking away, lips pressed together

name: excitement-0
prompt: high arched eyebrows, sparkling wide eyes, big open smile, energetic mood

name: fear-0
prompt: raised knit eyebrows, widened eyes, trembling lips, tense face

name: gratitude-0
prompt: gentle relaxed brows, soft smile, kind eyes, slight bow, thankful look

name: grief-0
prompt: upraised inner brows, tearful eyes, trembling mouth, visible tear streams, distressed face

name: joy-0
prompt: upturned brows, bright smile, lively eyes, cheerful mood

name: love-0
prompt: soft relaxed brows, half-lidded tender eyes, gentle smile, warm blush, affectionate gaze

name: nervousness-0
prompt: slanted worried brows, uneasy smile, restless eyes, slight blush, fidgety look

name: neutral-0
prompt: straight relaxed brows, calm face, neutral mouth, relaxed eyes

name: optimism-0
prompt: lifted brows, hopeful smile, bright eyes, forward-looking gaze

name: pride-0
prompt: arched brows, confident eyes, subtle smirk, chin slightly raised

name: realization-0
prompt: suddenly raised eyebrows, widened eyes, thoughtful pause, subtle surprise

name: relief-0
prompt: lowered relaxed brows, gentle exhale, soft smile, eased tension, calm eyes

name: remorse-0
prompt: inner brows raised, guilty look, downcast eyes, slight tears, apologetic face

name: sadness-0
prompt: inner brows raised, drooping eyelids, flat mouth, gloomy face, subtle tears

name: surprise-0
prompt: very high raised eyebrows, wide eyes, open mouth, startled expression
```

`기본 프롬프트(공통)`에 캐릭터 프롬프트만 입력하면 바로 적용이 가능합니다. 자유롭게 사용해 주세요.

## License
MIT License

---
<a name="english-documentation"></a>
## 🇺🇸 English Documentation

# sd-batch-iterator
> **⚠️** <br>
> This project is a cleaned-up version of a tool originally made for personal use.  
> Most of the code was created with the help of AI.  
> Testing was conducted only in a limited environment based on `webui_forge_cu124_torch24`,  
> and proper operation in all environments is not guaranteed.  
> Ongoing maintenance and support are not guaranteed.  
> The author is not responsible for any issues or damages resulting from the use of this tool.  
> You are free to fork and modify this project as needed.

This is a batch prompt execution and automation extension for Stable Diffusion WebUI.  
It was created to automatically generate SillyTavern expression images without using workflows.  
It sequentially executes a list of prompts defined in a JSON file to automate `txt2img` and `img2img` generation.

## Key Features
- **All modes supported**: Can be used as a script in both the `txt2img` and `img2img` tabs.
- **JSON-based automation**: Combines a base prompt with multiple variable prompts to generate images in bulk.
- **Automatic file naming**: Appends each entry’s name (`name`) from the JSON file as a suffix to the output filename.
- **Standalone editor included**: Includes a GUI application (`prompt_editor_app.py`) for easily editing JSON prompt lists.

### Installation
1. Go to the `Extensions` tab in WebUI.
2. Click `Install from URL`.
3. Enter the URL of this repository and click `Install`.
4. Click `Apply and restart UI` to apply the extension.

## Usage

### Using the WebUI Script
1. Select **sd-batch-iterator** from the Script dropdown in the `txt2img` or `img2img` tab.
2. Upload your JSON file.
3. Click the Generate button to sequentially run all prompts in the list.

### Using the Prompt Editor
- Run `prompt_editor_app.py` to manage prompt lists in a GUI and save them as JSON.
- (Example: `python prompt_editor_app.py`)

## JSON Format Example
```
json
{
    "base_prompt": "masterpiece, best quality",
    "variable_prompts": [
        {"name": "red_theme", "prompt": "red hair, red eyes", "enabled": true},
        {"name": "blue_theme", "prompt": "blue hair, blue eyes", "enabled": true}
    ]
}
```

---

## Description

- This extension was created to automatically generate SillyTavern expression images without requiring additional workflows.
- It uses the current WebUI settings and only replaces the prompt sequentially based on the JSON configuration.  
  (Base prompt + variable prompt 1 >> Base prompt + variable prompt 2 >> ...)
- The positive prompt entered in WebUI is ignored and replaced with the prompt defined in the JSON file.
- The negative prompt entered in WebUI is used as-is.
- Output filenames are saved with the variable prompt name appended as a suffix.

### How to Use `prompt_editor_app.py`
- Enter a common prompt for all generations in `Base Prompt (Common)`.
- Enter a `Name` and `Variable Prompt`, then click `Add/Update` to add it to the list.
- Click an item in the variable prompt list, edit it, and click `Add/Update` to update it.
- During generation, the variable prompt is appended after the base prompt, and only the variable prompt is replaced for each iteration.

### `test_prompts.json`

The file includes a list of 28 expression prompts that can be registered in SillyTavern.  
The prompt contents are as follows.

```
name: admiration-0
prompt: slightly raised eyebrows, sparkling eyes, soft smile, gentle blush, slight awe

name: amusement-0
prompt: relaxed eyebrows, playful smile, bright eyes, lighthearted mood

name: anger-0
prompt: v-shaped eyebrows, deeply furrowed brows, glaring eyes, clenched jaw, tense face

name: annoyance-0
prompt: slanted eyebrows, narrowed eyes, slight frown, side glance, puffed cheeks

name: approval-0
prompt: natural relaxed brows, gentle smile, calm eyes, slight nod, composed face

name: caring-0
prompt: inner brows slightly raised, tender eyes, warm smile, concerned look

name: confusion-0
prompt: uneven eyebrows, one brow raised, puzzled eyes, tilted head, slightly open mouth

name: curiosity-0
prompt: raised eyebrows, wide focused eyes, intent gaze, slight lean forward

name: desire-0
prompt: half-lidded eyes, relaxed brows, intense gaze, subtle blush, parted lips

name: disappointment-0
prompt: downward brows, drooping eyelids, small frown, downcast eyes

name: disapproval-0
prompt: knit eyebrows, cold stare, flat lips, stern face

name: disgust-0
prompt: lowered brows, wrinkled nose, averted gaze, tense mouth, recoiling expression

name: embarrassment-0
prompt: uneven lowered brows, deep blush, shy face, looking away, lips pressed together

name: excitement-0
prompt: high arched eyebrows, sparkling wide eyes, big open smile, energetic mood

name: fear-0
prompt: raised knit eyebrows, widened eyes, trembling lips, tense face

name: gratitude-0
prompt: gentle relaxed brows, soft smile, kind eyes, slight bow, thankful look

name: grief-0
prompt: upraised inner brows, tearful eyes, trembling mouth, visible tear streams, distressed face

name: joy-0
prompt: upturned brows, bright smile, lively eyes, cheerful mood

name: love-0
prompt: soft relaxed brows, half-lidded tender eyes, gentle smile, warm blush, affectionate gaze

name: nervousness-0
prompt: slanted worried brows, uneasy smile, restless eyes, slight blush, fidgety look

name: neutral-0
prompt: straight relaxed brows, calm face, neutral mouth, relaxed eyes

name: optimism-0
prompt: lifted brows, hopeful smile, bright eyes, forward-looking gaze

name: pride-0
prompt: arched brows, confident eyes, subtle smirk, chin slightly raised

name: realization-0
prompt: suddenly raised eyebrows, widened eyes, thoughtful pause, subtle surprise

name: relief-0
prompt: lowered relaxed brows, gentle exhale, soft smile, eased tension, calm eyes

name: remorse-0
prompt: inner brows raised, guilty look, downcast eyes, slight tears, apologetic face

name: sadness-0
prompt: inner brows raised, drooping eyelids, flat mouth, gloomy face, subtle tears

name: surprise-0
prompt: very high raised eyebrows, wide eyes, open mouth, startled expression
```

You can simply enter your character prompt in the base prompt (common) field to apply these expressions immediately.  
Feel free to use and modify them as needed.

## License
MIT License
