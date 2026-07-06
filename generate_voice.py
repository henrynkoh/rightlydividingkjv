"""
Day 1 – ElevenLabs Voice Generator
Run: pip install elevenlabs
     python generate_voice.py
"""

from elevenlabs.client import ElevenLabs
import os

API_KEY = "sk_2e49be7e4277bd72ca377bd406620d4c186a42ad87c7332a"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel (multilingual) — change if needed
MODEL   = "eleven_multilingual_v2"   # supports Korean + English

client = ElevenLabs(api_key=API_KEY)

scripts = {
    "01_rightly_dividing_intro": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. 2 Timothy 2:15 KJV.

Dear friends, 전능하신 하나님께서 우리에게 주신 성경은 완전합니다. 그러나 왜 그렇게 많은 혼란과 교파가 생겼을까요? 오늘부터 Rightly Dividing의 의미를 함께 나누어 보겠습니다.

Rightly dividing은 단순한 해석이 아닙니다. 하나님께서 다른 시대, 다른 사람들에게 주신 말씀을 정확하게 구분하는 것입니다. 마치 의사가 환자별로 약을 정확히 나누어 주는 것처럼요.

Who? 하나님께 인정받기를 원하는 모든 믿는 자.
Purpose? 부끄러움 없이 하나님의 일꾼이 되기 위함.
When? 특히 오늘날 은혜의 시대에 필수적입니다.

이 원칙을 적용하면 성경의 모호함이 사라지고, 구원의 확신과 하나님을 아는 지식이 날마다 자라게 됩니다.

오늘부터 한 구절씩 dispensationally 읽어보세요. Comment에 여러분이 가장 좋아하는 KJV verse를 남겨주시고, 이 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",

    "02_who_is_the_word_for": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. 2 Timothy 2:15 KJV.

오늘 질문: 성경의 모든 말씀이 모든 사람에게 똑같이 적용될까요?

성경은 하나님의 완전한 말씀이지만, 수신자와 시대에 따라 구분해야 합니다. 예를 들어, 모세에게 주신 율법은 이스라엘 백성을 위한 것이었고, 바울을 통해 주신 은혜의 복음은 오늘날 이방인을 포함한 교회에게 주어졌습니다.

Who? Context에 따라 Israel, Church, Tribulation saints 등 다릅니다.
Purpose? 각 시대에 하나님의 뜻을 분명히 알게 하심.
Application Range? 일부는 모든 시대에 일관되지만, 많은 부분은 특정 경륜, 즉 dispensation에 적용됩니다.

이 distinction을 알면 성경이 더 명확해지고, 하나님의 지혜를 더욱 깊이 알게 됩니다. 구원의 길도 정확히 이해할 수 있습니다.

여러분은 오늘 어떤 verse를 rightly divide 하고 싶으신가요? 댓글로 알려주세요. 함께 성장하는 이 여정에 참여해 주세요. Subscribe 부탁드립니다. Lord Jesus, thank You for Your clear Word. Amen.""",

    "03_kingdom_vs_grace_gospel": """Moreover, brethren, I declare unto you the gospel, by which also ye are saved. 1 Corinthians 15:1-4 KJV.

예수님의 지상 사역 때는 Kingdom Gospel이 전파되었습니다: Repent, for the kingdom of heaven is at hand. Matthew 4:17.

그러나 십자가 후, 바울을 통해 Grace Gospel이 계시되었습니다: 그리스도께서 우리 죄를 위하여 죽으시고 장사 지낸 바 되셨다가 다시 살아나신 것.

Key Distinction: Kingdom Gospel은 Israel에게 지상 왕국을 제안하는 것이었고, Grace Gospel은 오늘날 누구나 믿음으로 구원받는 복음입니다.

Who? Kingdom — Israel primarily. Grace — All, Jew and Gentile.
Purpose? 각 복음은 하나님의 경륜에서 다른 역할을 합니다.

이 구분을 알면 구원의 확신이 생기고, 하나님의 다단한 지혜를 찬양하게 됩니다.

오늘 이 복음을 믿으시고 구원받으셨습니까? 댓글로 간증 나누어 주세요. 매일 이 채널에서 더 깊이 공부합시다. Thank You, Father, for the clear Gospel of Grace. In Jesus' name, Amen.""",

    "04_why_so_many_denominations": """Study to shew thyself approved, rightly dividing the word of truth. 2 Timothy 2:15 KJV.

오늘날 수많은 교파와 교단이 존재하는 주된 이유는 Rightly Dividing의 실패입니다. Law와 Grace를 섞고, Kingdom과 Church를 구분하지 않고, 사람의 전통을 하나님의 말씀 위에 두기 때문입니다.

하나님은 혼란의 하나님이 아니십니다. 1 Corinthians 14:33. Right division을 통해 우리는 Law vs Grace, Kingdom Gospel vs Grace Gospel, Israel vs Church를 명확히 알게 됩니다.

Result: 부끄러움 없는 일꾼이 되어 진리 안에서 하나가 됩니다.

이 채널은 오직 KJV와 Right Division으로 돌아가 하나님의 뜻을 분명히 알리는 선교 채널입니다.

여러분의 교회 경험에서 느꼈던 혼란을 댓글로 나누어 주세요. 함께 성경으로 돌아갑시다. Lord, help us all to rightly divide Your Word. Amen.""",
}

output_dir = "audio_output"
os.makedirs(output_dir, exist_ok=True)

for filename, text in scripts.items():
    print(f"Generating: {filename} ...")
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id=MODEL,
        output_format="mp3_44100_128",
    )
    filepath = os.path.join(output_dir, f"{filename}.mp3")
    with open(filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    print(f"  Saved → {filepath}")

print("\nDone! All 4 audio files saved in ./audio_output/")
