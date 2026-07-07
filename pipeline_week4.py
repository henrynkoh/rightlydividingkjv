"""
Rightly Dividing KJV – Week 4 Pipeline (Scripts 89-116)
Topic: The Believer's Position & Practice in the Age of Grace
Run: cd ~/Documents/Claude/Projects/rightlydividing && python3 pipeline_week4.py
"""

import os, subprocess, datetime, pickle, json, textwrap
import pytz
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, ImageClip
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ─── CONFIG ───────────────────────────────────────────────────────────────────
MACOS_VOICE    = "Yuna"
KST            = pytz.timezone("Asia/Seoul")
TODAY          = datetime.datetime.now(KST).date()
SCHEDULE_TIMES = ["07:00", "12:00", "16:00", "20:00"]
OUT_DIR        = Path("output")
AUDIO_DIR      = OUT_DIR / "audio"
IMG_DIR        = OUT_DIR / "images"
VIDEO_DIR      = OUT_DIR / "videos"
UPLOAD_LOG     = OUT_DIR / "uploaded_week4.json"
SCOPES         = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET  = "client_secret.json"
TOKEN_PICKLE   = "token.pickle"

for d in [AUDIO_DIR, IMG_DIR, VIDEO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─── VIDEO LIST ───────────────────────────────────────────────────────────────
VIDEOS = [
  {
    "id": "89",
    "title": "Romans 5:1 – Justified by Faith, We Have Peace with God | KJV Right Division",
    "tags": ["Romans 5:1","peace with God","KJV","justification","grace","dispensational","한국어"],
    "thumbnail_text": "Peace\nwith God",
    "thumbnail_sub": "Romans 5:1 | KJV Right Division",
    "thumbnail_bg": (10, 20, 45),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, peace with God is not an emotion. It is a legal declaration. The moment you believed the Gospel — that Christ died for your sins, was buried, and rose again — God's court issued its verdict: justified. Not guilty. Righteous. And with that verdict came peace.

Therefore being justified by faith, we have peace with God through our Lord Jesus Christ. Romans five one, King James Bible.

Under the Law, Israel could never have settled peace with God — because the blood of bulls and goats could never permanently take away sins. The High Priest entered the Holy of Holies once per year. But Christ's one sacrifice accomplished what no system of law could achieve. Romans five one declares the result for everyone who believes in this age of grace: peace — permanent, legal, unshakeable.

이 평화는 당신의 감정에 따라 변하지 않습니다. 이것은 십자가에서 확립되고 부활로 봉인되었습니다. 하나님은 당신을 볼 때 그분의 아들의 의를 보십니다. 적대감은 사라졌습니다. 전쟁은 끝났습니다. 당신은 우주의 하나님과 평화를 누리고 있습니다.

When anxiety or guilt tries to rob you of your peace, return to Romans five one. Declare it aloud: I am justified by faith. I have peace with God through Jesus Christ. This is not positive thinking — it is legal reality grounded in the finished work of Christ. Let this peace, which passes all understanding, guard your heart today.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "90",
    "title": "Romans 8:28 – All Things Work Together for Good | KJV Right Division",
    "tags": ["Romans 8:28","all things","KJV","grace","sovereignty","dispensational","한국어"],
    "thumbnail_text": "All Things\nWork Together",
    "thumbnail_sub": "Romans 8:28 | KJV Right Division",
    "thumbnail_bg": (15, 35, 20),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Romans eight twenty-eight is not a promise that all things feel good, look good, or seem good. It is a promise that the God who works all things is working them together — like a master chef combining ingredients, some bitter, some sweet — into something ultimately good.

And we know that all things work together for good to them that love God, to them who are the called according to his purpose. Romans eight twenty-eight, King James Bible.

The word called points back to God's eternal purpose. He called you. He knew you. He predestined you to be conformed to the image of His Son. Your current difficulty is not outside His plan — it is within it. And within His plan, all things work together for good.

모든 것이 협력하여 선을 이룬다는 것은 — 모든 상황이 좋아 보인다는 의미가 아닙니다. 하나님께서 주권적으로 모든 실마리를 — 고통스러운 것도, 혼란스러운 것도, 어두운 것도 — 그분의 완벽한 목적으로 엮어가신다는 의미입니다.

Write down your current difficulty. Then write Romans eight twenty-eight next to it. God is not absent from that difficulty. He is working. The God who raised Christ from the dead is working your situation together for good. Trust the Chef, not just the ingredients.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "91",
    "title": "Romans 8:37 – More Than Conquerors Through Christ | KJV Right Division",
    "tags": ["Romans 8:37","conquerors","KJV","victory","grace","dispensational","한국어"],
    "thumbnail_text": "More Than\nConquerors",
    "thumbnail_sub": "Romans 8:37 | KJV Right Division",
    "thumbnail_bg": (40, 10, 10),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul lists the battles: tribulation, distress, persecution, famine, nakedness, peril, sword. And then says — in all THESE things, not after them, not around them, but right in the middle of them — we are more than conquerors.

Nay, in all these things we are more than conquerors through him that loved us. Romans eight thirty-seven, King James Bible.

More than conquerors — the Greek hypernikōmen means super-victorious. Not barely surviving. Not enduring with gritted teeth. Super-victorious. This is the grace-age believer's standing in Christ. Not because of personal strength, but through Him that loved us.

승리는 오는 것이 아닙니다 — 이미 이겨진 것입니다. 그리스도는 죄와 사망을 정복하셨고, 그분 안에서 당신도 정복자입니다. 오늘의 시련 속에서도 당신은 정복자로 걷고 있습니다.

Whatever you are facing today — name it, then say: In this, I am more than a conqueror through Christ who loved me. Nothing — nothing — shall be able to separate you from the love of God which is in Christ Jesus our Lord.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "92",
    "title": "Romans 12:1-2 – Present Your Body, Be Transformed | KJV Right Division",
    "tags": ["Romans 12:1","living sacrifice","KJV","transformation","grace","dispensational","한국어"],
    "thumbnail_text": "Living\nSacrifice",
    "thumbnail_sub": "Romans 12:1-2 | KJV Right Division",
    "thumbnail_bg": (10, 25, 50),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, after eleven chapters of doctrine Paul draws the line of application with one word: therefore. Because of all that God has done, here is the reasonable response: present yourself to God.

I beseech you therefore, brethren, by the mercies of God, that ye present your bodies a living sacrifice, holy, acceptable unto God, which is your reasonable service. Romans twelve one, King James Bible.

Under the Law, sacrifices were dead — an animal was slain. But in the grace age, God asks for a living sacrifice — ongoing, daily, voluntary. Verse two adds the transformation: be not conformed to this world, but be ye transformed by the renewing of your mind. The Greek word is metamorphoō — metamorphosis.

매일 아침 일어나기 전에, 하나님께 말로 자신을 드리십시오: 주님, 이 몸, 이 마음, 이 하루 — 당신께 드립니다. 당신의 말씀으로 저를 변화시키소서. 이것이 당신의 합리적인 예배입니다.

Every morning before you rise, present yourself to God verbally. This daily act of surrender is your reasonable, logical, Spirit-led worship. Not ceremony — a life. Begin today.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "93",
    "title": "1 Corinthians 2:9-10 – The Spirit Reveals the Deep Things of God | KJV",
    "tags": ["1 Corinthians 2","Holy Spirit","KJV","revelation","grace","dispensational","한국어"],
    "thumbnail_text": "Deep Things\nof God",
    "thumbnail_sub": "1 Corinthians 2:10 | KJV Right Division",
    "thumbnail_bg": (20, 10, 45),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, eye has not seen, ear has not heard, neither has it entered the heart of man — the things God has prepared. The natural mind cannot access them. But God has revealed them to us by His Spirit.

But God hath revealed them unto us by his Spirit: for the Spirit searcheth all things, yea, the deep things of God. First Corinthians two ten, King James Bible.

In the grace age, every believer has the indwelling Holy Spirit. This Spirit is not merely a comforter — He is the revealer of divine wisdom. The deep things of God — the mystery of the Body of Christ, the riches of His grace — are accessible to the Spirit-taught believer with an open Bible.

당신은 성경을 이해하기 위해 신학교 학위나 종교 기관이 필요하지 않습니다. 당신 안에 거하시는 성령님이 필요합니다. 그분은 하나님의 깊은 것들을 탐구하시고 당신에게 가르쳐 주십니다.

Before you read your Bible today, pray: Holy Spirit, reveal the deep things of God. Open my understanding. Then read Paul's epistles with expectation. The Spirit who searched the depths of God has come to live in you. Trust Him.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "94",
    "title": "1 Corinthians 6:19-20 – Your Body Is the Temple of the Holy Spirit | KJV",
    "tags": ["1 Corinthians 6:19","temple","Holy Spirit","KJV","grace","dispensational","한국어"],
    "thumbnail_text": "Temple of\nthe Spirit",
    "thumbnail_sub": "1 Corinthians 6:19-20 | KJV",
    "thumbnail_bg": (10, 30, 30),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, in the Old Testament, the Holy Spirit came upon selected individuals for specific tasks, then departed. Under the mystery revealed through Paul, the Holy Spirit permanently indwells every believer the moment they believe. Your body has become His temple.

What? know ye not that your body is the temple of the Holy Ghost which is in you, which ye have of God, and ye are not your own? For ye are bought with a price: therefore glorify God in your body. First Corinthians six nineteen to twenty, King James Bible.

Ye are not your own — this is the most liberating truth in Scripture. You do not belong to sin. You belong to the One who purchased you with His own blood. That ownership is not bondage — it is the most secure identity you could ever possess.

당신의 몸은 성전입니다. 오늘의 모든 결정 전에 — 무엇을 먹을지, 무엇을 볼지, 어디를 갈지 — 잠시 멈추고 기억하십시오: 나의 몸은 그분의 성전입니다. 그분이 값을 치르셨습니다. 그분이 그 안에 사십니다.

Glorify God in your body today. Not out of obligation, but out of gratitude. He paid for it. He lives in it. Honor the One who chose to make your body His home.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "95",
    "title": "2 Corinthians 5:7 – Walk by Faith, Not by Sight | KJV Right Division",
    "tags": ["2 Corinthians 5:7","faith","KJV","grace","walk","dispensational","한국어"],
    "thumbnail_text": "Walk by\nFaith",
    "thumbnail_sub": "2 Corinthians 5:7 | KJV Right Division",
    "thumbnail_bg": (35, 20, 5),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, five words, two contrasts, one complete philosophy of the Christian life. Faith versus sight. The unseen versus the visible. The eternal versus the temporary.

For we walk by faith, not by sight. Second Corinthians five seven, King James Bible.

In the Kingdom program, Israel walked by sight — pillar of fire by night, cloud by day, manna on the ground, signs following. But the Church age is the faith age — between the first and second comings of Christ, where we walk by the Word, the Spirit, and the promises, not by visible confirmations.

이것은 맹목적인 믿음이 아닙니다. 대상이 있는 믿음입니다 — 부활하신 그리스도와 그분의 확증된 말씀. 아브라함은 믿음이 흔들리지 않았습니다. 그가 우리의 모델입니다.

What circumstance today demands that you trust what you cannot see? Name it. Then choose faith over sight — not because the difficulty is not real, but because the God who promised is more real. Take one step today that only makes sense if God is who He says He is.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "96",
    "title": "2 Corinthians 5:17 – New Creation in Christ | KJV Right Division",
    "tags": ["2 Corinthians 5:17","new creation","KJV","grace","identity","dispensational","한국어"],
    "thumbnail_text": "New\nCreation",
    "thumbnail_sub": "2 Corinthians 5:17 | KJV Right Division",
    "thumbnail_bg": (10, 40, 15),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, the new creation is not a reformation of the old. It is not a better version of what you were before. It is entirely new — the same creative power that spoke the universe into existence applied to your soul.

Therefore if any man be in Christ, he is a new creature: old things are passed away; behold, all things are become new. Second Corinthians five seventeen, King James Bible.

In Christ, you are not a Gentile sinner cleaned up — you are a new creature belonging to the one new man of Ephesians two fifteen. The old identity — sinner, condemned, dead in trespasses — has passed away. A new identity has been given: righteous, accepted, alive in Christ.

당신의 옛 본성과 동일시하는 것을 멈추십시오. 옛 사람은 죽었습니다 — 로마서 육 육절. 당신은 새로운 피조물입니다. 옛 유혹들이 찾아올 때, 그들에게 상기시키십시오: 그들이 찾는 그 사람은 더 이상 여기 살지 않습니다.

Stop identifying with your old nature. You are a new creation. When old temptations come calling, remind them: that person they're looking for no longer lives here. A new creature has taken up residence. Live from that truth today.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "97",
    "title": "Galatians 2:20 – Crucified with Christ, Christ Lives in Me | KJV",
    "tags": ["Galatians 2:20","crucified with Christ","KJV","grace","identity","dispensational","한국어"],
    "thumbnail_text": "Christ\nLives in Me",
    "thumbnail_sub": "Galatians 2:20 | KJV Right Division",
    "thumbnail_bg": (45, 5, 5),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, this is one of the most transformational verses in all of Paul's writings. Four declarations that redefine Christian existence: I am crucified. Nevertheless I live. Not I, but Christ. By the faith of the Son of God who loved me and gave Himself for me.

I am crucified with Christ: nevertheless I live; yet not I, but Christ liveth in me: and the life which I now live in the flesh I live by the faith of the Son of God, who loved me, and gave himself for me. Galatians two twenty, King James Bible.

Co-crucifixion with Christ — our old man crucified at the cross — is the positional foundation of grace-age living. You do not have to crucify yourself. You have already been crucified with Him. You died. And yet you live — but now Christ lives His life through your surrendered personality.

그분은 나를 사랑하셨습니다. 개인적으로, 구체적으로. 그리고 나를 위해 자신을 주셨습니다. 이 사랑이 그리스도인 삶의 동기입니다 — 두려움이 아니라, 저를 위해 자신을 주신 분에 대한 사랑.

Today's practice: before any decision, any challenge, any temptation — return to Galatians two twenty. I am crucified. Christ lives in me. He loves me. Let that four-phrase anchor hold you steady. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "98",
    "title": "Galatians 5:1 – Stand Fast in the Liberty of Christ | KJV Right Division",
    "tags": ["Galatians 5:1","liberty","KJV","grace","freedom","dispensational","한국어"],
    "thumbnail_text": "Stand Fast\nin Liberty",
    "thumbnail_sub": "Galatians 5:1 | KJV Right Division",
    "thumbnail_bg": (10, 25, 55),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, liberty — real, God-given, Christ-purchased freedom — is freedom from the bondage of the Law as a means of justification. Christ made us free. And Paul commands: stand fast in it.

Stand fast therefore in the liberty wherewith Christ hath made us free, and be not entangled again with the yoke of bondage. Galatians five one, King James Bible.

The yoke of bondage is always seeking re-entry. Religious performance, guilt-driven service, rule-based spirituality, the constant need to earn what has already been freely given. Paul says: don't go back. You were made free. Stand in it. Resist the pull back to bondage.

그리스도께서 당신을 자유롭게 하셨습니다. 그 자유 안에 굳게 서십시오. 누군가 당신의 구원에 종교적 요건을 추가하려 한다면 — 갈라디아서 오 일절이 당신의 대답입니다: 그리스도께서 이미 나를 자유롭게 하셨습니다.

Identify one area where you are trying to earn God's favor through performance. Apply Galatians five one: that favor is already yours in Christ. Stand fast. Serve God freely from love, not from debt and fear. That is grace-age living.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "99",
    "title": "Galatians 6:14 – Glory Only in the Cross of Christ | KJV Right Division",
    "tags": ["Galatians 6:14","cross","KJV","glory","grace","dispensational","한국어"],
    "thumbnail_text": "Glory in\nthe Cross",
    "thumbnail_sub": "Galatians 6:14 | KJV Right Division",
    "thumbnail_bg": (30, 10, 10),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul could have boasted. He was a Pharisee of Pharisees, blameless under the Law, educated under Gamaliel, an apostle who received direct revelation from the risen Christ. But he chose one glory: the cross.

But God forbid that I should glory, save in the cross of our Lord Jesus Christ, by whom the world is crucified unto me, and I unto the world. Galatians six fourteen, King James Bible.

By the cross, Paul says, the world is crucified to me and I to the world. The old attraction to worldly approval, worldly achievement, worldly security — crucified. Dead. Gone. The cross is the center of everything in the grace age.

당신은 무엇을 자랑하는 경향이 있습니까? 당신의 영적 지식? 교회 출석? 도덕적 기록? 바울은 당신을 다시 방향을 잡아줄 것입니다: 하나님이 금하시옵니다. 오직 십자가만을 자랑하십시오.

What do you tend to glory in? Paul would redirect you: God forbid. Glory in the cross alone. The cross says you had nothing to offer and Christ gave everything. Let that humility and wonder be your daily posture. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "100",
    "title": "Ephesians 1:7 – Redemption Through His Blood, Riches of Grace | KJV",
    "tags": ["Ephesians 1:7","redemption","KJV","grace","forgiveness","dispensational","한국어"],
    "thumbnail_text": "Redemption\nThrough Blood",
    "thumbnail_sub": "Ephesians 1:7 | KJV Right Division",
    "thumbnail_bg": (10, 20, 45),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, redemption means to buy back — to purchase freedom for one who was enslaved. We were enslaved to sin, to the Law's condemnation, to death. Christ paid the ransom with His own blood. And the forgiveness was not a minimum wage of grace — it was according to the riches of His grace.

In whom we have redemption through his blood, the forgiveness of sins, according to the riches of his grace. Ephesians one seven, King James Bible.

This is present tense — we HAVE redemption. Not we shall have it. We have it now, in Him. The riches of grace are not measured by your need but by God's abundance. Ephesians three eight calls them unsearchable riches of Christ — beyond calculation, beyond comprehension.

적이 당신의 과거 죄들을 상기시킬 때, 에베소서 일 칠절로 응답하십시오: 나는 그분의 보혈을 통해 구속을 가지고 있습니다. 나의 죄는 그분의 은혜의 풍요로움에 따라 용서받았습니다. 빈곤한 은혜가 아니라 — 풍요로운 은혜입니다.

When the enemy reminds you of your past sins, respond with Ephesians one seven: I have redemption through His blood. My sins are forgiven according to the RICHES of His grace. Walk in that lavish, abundant, eternal forgiveness today. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "101",
    "title": "Ephesians 3:20 – Exceeding Abundantly Above All You Ask | KJV",
    "tags": ["Ephesians 3:20","exceeding abundantly","KJV","grace","prayer","dispensational","한국어"],
    "thumbnail_text": "Exceeding\nAbundantly",
    "thumbnail_sub": "Ephesians 3:20 | KJV Right Division",
    "thumbnail_bg": (40, 25, 5),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, God's ability is not limited to your prayer list or your imagination. He is able to do exceeding abundantly — the Greek is hyperekperissou, beyond all measure — above all that you ask. And above what you think.

Now unto him that is able to do exceeding abundantly above all that we ask or think, according to the power that worketh in us. Ephesians three twenty, King James Bible.

The key phrase is according to the power that worketh in US. This is the specific power of the indwelling Spirit in the grace-age believer — the same power that raised Christ from the dead (Ephesians one nineteen to twenty). That power works in you right now.

당신이 하나님께 구한 가장 큰 것을 생각해보십시오. 이제 그분이 그것보다 훨씬 더 많이 하실 수 있다는 것을 고려하십시오. 크게 기도하십시오. 더 크게 믿으십시오. 하나님의 능력은 당신의 최선의 상상을 능가합니다.

What is the biggest thing you have asked God for? Now consider that He is able to do exceeding abundantly above even that. Pray big. Believe bigger. Trust the God whose ability surpasses your best imagination. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "102",
    "title": "Ephesians 4:4-6 – One Body, One Spirit, One Lord | KJV Right Division",
    "tags": ["Ephesians 4:4","one body","KJV","unity","grace","dispensational","한국어"],
    "thumbnail_text": "One Body\nOne Lord",
    "thumbnail_sub": "Ephesians 4:4-6 | KJV Right Division",
    "thumbnail_bg": (10, 20, 50),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul's seven ones are the unifying foundations of the Body of Christ. In a world that fragments into denominations and competing traditions, Paul anchors the Church to seven indivisible realities that transcend all human division.

There is one body, and one Spirit, even as ye are called in one hope of your calling; One Lord, one faith, one baptism, One God and Father of all, who is above all, and through all, and in you all. Ephesians four four to six, King James Bible.

One baptism — in this context, the Spirit baptism into the Body of Christ from First Corinthians twelve thirteen — the single act that places every believer into Christ at salvation. The seven ones describe the grace-age church in its essential, irreducible unity.

하나님 안에서의 하나됨은 나눔을 제거하지는 않지만, 모든 분열보다 더 깊습니다. 당신은 그리스도의 몸의 일원입니다 — 배경이나 교단에 관계없이. 오늘 그 하나됨을 살아내십시오.

Find a believer from a different background today and recognize them as a member of the one body. The seven ones make you family. Walk worthy of your calling in the bond of peace. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "103",
    "title": "Ephesians 5:25-27 – Christ Loved the Church and Gave Himself | KJV",
    "tags": ["Ephesians 5:25","Christ loves Church","KJV","grace","marriage","dispensational","한국어"],
    "thumbnail_text": "Christ Loved\nthe Church",
    "thumbnail_sub": "Ephesians 5:25-27 | KJV Right Division",
    "thumbnail_bg": (50, 10, 20),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul uses the greatest love in history as the template for marriage — and in doing so, reveals the depth of Christ's love for His Church. Christ loved the Church before it was lovable, before it was faithful, before it was anything at all.

Husbands, love your wives, even as Christ also loved the church, and gave himself for it; That he might sanctify and cleanse it with the washing of water by the word. Ephesians five twenty-five to twenty-six, King James Bible.

He is not waiting for the Church to become worthy. He is making it worthy through His own work — the washing of water by the Word. He will present it to Himself glorious, without spot or wrinkle.

그리스도께서는 당신을 위해 자신을 주셨습니다. 그분은 말씀을 통해 당신을 성결하게 하고 계십니다. 그분은 당신을 흠도 없고 주름도 없이 아버지 앞에 영광스럽게 제시하실 것입니다. 이것이 당신의 영원한 이야기입니다.

Meditate on Christ's love for you as His Church. He gave Himself for you. He is sanctifying you through His Word. He will present you without spot, without wrinkle, in glorious beauty. Let that love transform how you love others. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "104",
    "title": "Ephesians 6:10-11 – Put on the Full Armor of God | KJV Right Division",
    "tags": ["Ephesians 6:10","armor of God","KJV","spiritual warfare","grace","dispensational","한국어"],
    "thumbnail_text": "Full Armor\nof God",
    "thumbnail_sub": "Ephesians 6:10-11 | KJV Right Division",
    "thumbnail_bg": (10, 15, 40),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Ephesians ends where any honest look at reality must end — with spiritual warfare. The believer has a position in heavenly places, but the conflict in heavenly places is real. The armor of God is not optional equipment.

Finally, my brethren, be strong in the Lord, and in the power of his might. Put on the whole armour of God, that ye may be able to stand against the wiles of the devil. Ephesians six ten to eleven, King James Bible.

The armor's components — truth, righteousness, the Gospel of peace, faith, salvation, the Word of God, prayer — are not moral qualities you achieve. They are weapons Christ provides. The strength is not yours — it is His, available to you by faith.

전쟁은 혈육에 대한 것이 아닙니다 — 사람들, 정부, 또는 보이는 적들에 대한 것이 아닙니다. 정사와 권세와 어두움의 주관자들과 하늘에 있는 악한 영들에 대한 것입니다. 기도와 말씀이 필수적인 이유입니다.

Put on the armor deliberately today. Claim truth against lies. Claim righteousness against condemnation. Take the sword of the Spirit — speak the Word into your situation. The battle is real. The armor is provided. Stand. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "105",
    "title": "Philippians 1:6 – He Who Began a Good Work Will Complete It | KJV",
    "tags": ["Philippians 1:6","good work","KJV","sanctification","grace","dispensational","한국어"],
    "thumbnail_text": "He Will\nComplete It",
    "thumbnail_sub": "Philippians 1:6 | KJV Right Division",
    "thumbnail_bg": (10, 35, 20),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, the God who started your salvation will finish it. He did not begin a work He lacks the power or intention to complete. From the first moment of faith to the day of Christ's return — He is actively completing the good work He began in you.

Being confident of this very thing, that he which hath begun a good work in you will perform it until the day of Jesus Christ. Philippians one six, King James Bible.

The confidence is not in your consistency. The confidence is in God who began the work. The initiator is the completer. The author is the finisher. Your spiritual progress does not rest on your faithfulness — it rests on His.

영적 성장에 대해 낙담한 곳이 있습니까? 빌립보서 일 육절을 적용하십시오: 이 선한 일을 시작하신 분이 그것을 완성하실 것입니다. 당신은 진행 중인 작품입니다 — 그러나 예술가는 미완성 캔버스를 결코 포기하지 않습니다.

Where are you discouraged about your spiritual growth? Apply Philippians one six directly: He who began this good work in me will complete it. You are a work in progress — but the Artist never abandons an unfinished canvas. Trust the Completer. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "106",
    "title": "Philippians 1:21 – To Live Is Christ, to Die Is Gain | KJV Right Division",
    "tags": ["Philippians 1:21","to live is Christ","KJV","grace","eternity","dispensational","한국어"],
    "thumbnail_text": "To Live\nIs Christ",
    "thumbnail_sub": "Philippians 1:21 | KJV Right Division",
    "thumbnail_bg": (20, 10, 45),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul wrote this from a prison cell facing possible execution. And he did not write it as despair — he wrote it as triumph. If I live, Christ is expressed through this life. If I die, I gain — I am with Christ, which is far better.

For to me to live is Christ, and to die is gain. Philippians one twenty-one, King James Bible.

In the grace age, absence from the body is presence with the Lord — Second Corinthians five eight. There is no purgatory, no soul sleep, no intermediate state of suffering. The moment a grace-age believer departs from this body, they are immediately in the presence of Christ.

사망은 믿는 자에게 적이 아닙니다 — 그것은 문입니다. 살면 그리스도입니다 — 살 가치가 있는 목적. 죽으면 유익입니다 — 죽을 가치가 있는 운명. 바울은 어느 쪽으로도 잃을 수 없었습니다. 당신도 마찬가지입니다.

Remove the fear of death by replacing it with Philippians one twenty-one. And until that day, let your life be Christ — expressed through your words, your work, your witness. To live is Christ. Live it with everything you have. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "107",
    "title": "Philippians 2:5-8 – Let This Mind Be in You | KJV Right Division",
    "tags": ["Philippians 2:5","mind of Christ","KJV","humility","grace","dispensational","한국어"],
    "thumbnail_text": "Mind of\nChrist",
    "thumbnail_sub": "Philippians 2:5-8 | KJV Right Division",
    "thumbnail_bg": (10, 25, 50),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, the mind of Christ is not primarily intellectual — it is attitudinal. It is the posture of voluntary humility. Christ possessed everything and He chose the form of a servant.

Let this mind be in you, which was also in Christ Jesus: Who, being in the form of God, thought it not robbery to be equal with God: But made himself of no reputation, and took upon him the form of a servant. Philippians two five to seven, King James Bible.

Paul uses the incarnation — the greatest act of condescension in all of history — to motivate humble service among believers. Verse eight: He humbled himself, and became obedient unto death, even the death of the cross. And God highly exalted Him. Humility precedes exaltation in God's economy, always.

오늘 교만이 장벽을 세운 관계를 한 가지 찾아보십시오. 그리스도의 마음을 적용하십시오: 종의 자세를 선택하십시오. 가장 강력한 존재가 그것을 선택했습니다. 그것은 통제 하의 강함입니다. 겸손하게 하십시오. 하나님이 그분의 때에 높이심을 처리하실 것입니다.

Identify one relationship where pride has built a wall. Apply the mind of Christ. Choose the servant's posture. Humble yourself. God will handle the exaltation. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "108",
    "title": "Philippians 4:11-13 – Content in All States Through Christ | KJV",
    "tags": ["Philippians 4:13","contentment","KJV","grace","all things","dispensational","한국어"],
    "thumbnail_text": "Content\nin All States",
    "thumbnail_sub": "Philippians 4:11-13 | KJV Right Division",
    "thumbnail_bg": (35, 20, 5),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, contentment is not a gift — it is a learned skill. Paul says I have learned. Learning requires time, experience, practice, and often failure. Paul learned contentment through shipwrecks, beatings, hunger, cold, and imprisonment.

I have learned, in whatsoever state I am, therewith to be content. I know both how to be abased, and I know how to abound. I can do all things through Christ which strengtheneth me. Philippians four eleven to thirteen, King James Bible.

The famous verse thirteen — I can do all things through Christ — is often taken out of context. In context, it means: I can be content in any state — abased or abounding — through Christ who strengthens me. The all things is specifically contentment in all circumstances.

당신은 오늘 어떤 상태에 있습니까? 낮아졌습니까, 아니면 풍요롭습니까? 어느 쪽이든, 그리스도가 당신의 충분함입니다. 연습하십시오: 나는 그리스도를 통해 이 상태에서 만족할 수 있습니다. 초자연적인 안정감. 그분의 임재에 뿌리를 두고 있습니다.

What state are you in today? Either way, Christ is your sufficiency. Practice saying: I can be content in this through Christ who strengthens me. Not resignation — supernatural steadiness rooted in His presence. Learn contentment. It is worth the curriculum. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "109",
    "title": "Philippians 4:19 – My God Shall Supply All Your Need | KJV Right Division",
    "tags": ["Philippians 4:19","supply","KJV","grace","provision","dispensational","한국어"],
    "thumbnail_text": "God Shall\nSupply",
    "thumbnail_sub": "Philippians 4:19 | KJV Right Division",
    "thumbnail_bg": (10, 40, 15),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, this promise flows from a context of giving. The Philippians gave generously to Paul's ministry in difficult circumstances, and Paul's response is this incomparable promise: my God shall supply all YOUR need.

But my God shall supply all your need according to his riches in glory by Christ Jesus. Philippians four nineteen, King James Bible.

Notice the measure: according to His riches in glory. Not according to your faith level or your deserve-ability — according to HIS riches. Ephesians three eight calls them unsearchable riches of Christ. The supply is measured by God's abundance, not your need.

오늘 특정한 필요를 이름 붙이십시오. 그런 다음 빌립보서 사 십구절을 주장하십시오: 나의 하나님이 그리스도 예수를 통한 그분의 영광의 풍요로움에 따라 이 필요를 공급하실 것입니다. 바라는 것이 아니라, 희망하는 것이 아니라 — 공급하실 것입니다.

Name a specific need today. Then stand on Philippians four nineteen: My God shall supply THIS need according to His riches in glory by Christ Jesus. Give generously when you have opportunity, and trust the God who supplies all need in return. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "110",
    "title": "Colossians 1:27 – Christ in You, the Hope of Glory | KJV Right Division",
    "tags": ["Colossians 1:27","Christ in you","KJV","mystery","grace","dispensational","한국어"],
    "thumbnail_text": "Christ in\nYou",
    "thumbnail_sub": "Colossians 1:27 | KJV Right Division",
    "thumbnail_bg": (10, 20, 45),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul identifies the supreme mystery in four words: Christ in you. Not Christ over you. Not Christ near you. Not Christ for you — though all are gloriously true. Christ IN you. The hope of glory.

To whom God would make known what is the riches of the glory of this mystery among the Gentiles; which is Christ in you, the hope of glory. Colossians one twenty-seven, King James Bible.

Israel's hope was the Messiah coming TO them externally. The grace-age mystery is Christ coming INTO us — indwelling every believer through His Spirit, producing His life from the inside out, making our glorification with Him certain.

당신은 결코 혼자가 아닙니다. 부활하신 그리스도의 임재를 어디에나 가지고 다닙니다. 이사회실, 병원, 깨진 관계, 잠 못 이루는 밤 — 당신 안에 계신 그리스도. 그 무한한 자원을 오늘 사용하십시오.

Begin every day with this declaration: Christ is in me. The hope of glory. His life is my resource. Whatever you face today, you do not face it alone. Draw on the inexhaustible resource already dwelling in you. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "111",
    "title": "Colossians 3:1-3 – Set Your Affections on Things Above | KJV Right Division",
    "tags": ["Colossians 3:1","things above","KJV","heavenly","grace","dispensational","한국어"],
    "thumbnail_text": "Things\nAbove",
    "thumbnail_sub": "Colossians 3:1-3 | KJV Right Division",
    "thumbnail_bg": (5, 20, 50),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, since you are risen with Christ — a settled reality — seek those things which are above. The imperative follows from the indicative. What you are determines what you pursue.

If ye then be risen with Christ, seek those things which are above, where Christ sitteth on the right hand of God. Set your affection on things above, not on things on the earth. For ye are dead, and your life is hid with Christ in God. Colossians three one to three, King James Bible.

Your life is hid with Christ in God — two layers of security. In Christ, and in God. Nothing can reach you there. The world cannot access it. Satan cannot penetrate it. You are hidden in the safest place in the universe.

오늘 당신의 정신적 에너지를 지배하는 세상적인 것을 하나 찾아보십시오. 이제 의도적으로 하나님의 오른편에 계신 그리스도를 향해 시선을 들어올리십시오. 위로부터의 관점은 항상 가장 중요한 것을 명확히 합니다.

Identify one earthly thing dominating your mental energy. Deliberately lift your gaze to Christ at the right hand of God. The view from above always clarifies what matters most. Set your mind there first. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "112",
    "title": "Colossians 3:16 – Let the Word of Christ Dwell in You Richly | KJV",
    "tags": ["Colossians 3:16","word of Christ","KJV","grace","Scripture","dispensational","한국어"],
    "thumbnail_text": "Word Dwell\nRichly",
    "thumbnail_sub": "Colossians 3:16 | KJV Right Division",
    "thumbnail_bg": (30, 15, 5),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, let implies choice and cooperation. The Word of Christ does not force its way into your life — it is welcomed, received, intentionally cultivated. And when it dwells, it dwells richly — abundantly, in all wisdom.

Let the word of Christ dwell in you richly in all wisdom; teaching and admonishing one another in psalms and hymns and spiritual songs, singing with grace in your hearts to the Lord. Colossians three sixteen, King James Bible.

This is the grace-age alternative to Mosaic regulation. Israel had the Law written on stone. The grace-age believer has the complete, revealed Word of Christ — available always, indwelt by the Spirit who teaches it — invited to dwell richly within. The internal transforms what external regulation never could.

그리스도의 말씀이 풍성하게 거하는 자연스러운 흘러넘침은 공동체와 예배입니다 — 가르치고, 권면하고, 마음으로 주께 노래하는 것입니다. 말씀은 내적으로 변화시키고, 그 다음 외적으로 표현됩니다.

Commit to letting the Word dwell more richly this week. Choose one of Paul's epistles. Read one chapter daily, meditatively. Carry a verse through the day. Richness of the Word produces richness of life. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "113",
    "title": "1 Timothy 2:5 – One God, One Mediator, the Man Christ Jesus | KJV",
    "tags": ["1 Timothy 2:5","one mediator","KJV","grace","access","dispensational","한국어"],
    "thumbnail_text": "One\nMediator",
    "thumbnail_sub": "1 Timothy 2:5 | KJV Right Division",
    "thumbnail_bg": (10, 25, 55),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, one God. One mediator. No committee of saints, no chain of priests, no hierarchy of intercessors between you and God. One. The man Christ Jesus — fully God, fully man — who gave Himself as a ransom for all.

For there is one God, and one mediator between God and men, the man Christ Jesus; Who gave himself a ransom for all, to be testified in due time. First Timothy two five to six, King James Bible.

In Israel's system, the Levitical priesthood mediated between God and the people. But at the moment of Christ's death, the veil was torn from top to bottom — from God's side down. The mediation of Christ made the mediation of priests permanently unnecessary.

당신이 다음에 기도할 때, 기억하십시오: 나는 하나의 중보자이신 그리스도 예수를 통해 아버지께 나아가고 있습니다. 중간 중보자 필요 없습니다. 대기 시간 없습니다. 예약 필요 없습니다. 담대히 나아오십시오. 그분은 당신의 아버지입니다.

Come directly to the Father through the one Mediator, Christ Jesus. No intermediary required. Hebrews four sixteen: Come boldly unto the throne of grace. Boldly. Because the one Mediator has cleared your path with His own blood. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "114",
    "title": "2 Timothy 1:12 – I Know Whom I Have Believed | KJV Right Division",
    "tags": ["2 Timothy 1:12","I know whom","KJV","grace","assurance","dispensational","한국어"],
    "thumbnail_text": "I Know\nWhom I Believe",
    "thumbnail_sub": "2 Timothy 1:12 | KJV Right Division",
    "thumbnail_bg": (20, 10, 45),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, Paul is in his second Roman imprisonment — in chains, cold, alone, awaiting execution. From that extreme circumstance, he writes not despair but certainty: I am not ashamed. I know. I am persuaded.

For the which cause I also suffer these things: nevertheless I am not ashamed: for I know whom I have believed, and am persuaded that he is able to keep that which I have committed unto him against that day. Second Timothy one twelve, King James Bible.

Three layers of confidence: I know — personal knowledge of a Person. I have believed — committed trust in the risen Christ. I am persuaded — settled conviction beyond the reach of circumstance. This is the bedrock certainty of a man whose entire life has tested and confirmed the faithfulness of God.

그분은 내가 그분께 맡긴 것을 지킬 수 있습니다 — 나의 생명, 영혼, 영원, 그분의 손에 맡겨지고 그분의 능력으로 지켜집니다. 나의 신실함이 아니라 — 그분의 신실함으로. 예금은 안전합니다. 지키시는 분이 신실하시기 때문입니다.

What have you committed to Christ today? Add this: I know Whom I have believed. I am persuaded He is able to keep what I have committed. The Keeper is faithful. Your deposit is secure. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "115",
    "title": "2 Timothy 3:16-17 – All Scripture Given by Inspiration of God | KJV",
    "tags": ["2 Timothy 3:16","inspiration","KJV","Scripture","sufficient","dispensational","한국어"],
    "thumbnail_text": "All Scripture\nGod-Breathed",
    "thumbnail_sub": "2 Timothy 3:16-17 | KJV Right Division",
    "thumbnail_bg": (10, 30, 20),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, given by inspiration of God — the Greek is theopneustos, God-breathed. As God breathed life into Adam, He breathed His own life and truth into every word of Scripture. The Bible is not merely a human book reporting on God — it is God's own self-expression.

All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness: That the man of God may be perfect, throughly furnished unto all good works. Second Timothy three sixteen to seventeen, King James Bible.

Four functions that cover the complete spectrum of the Christian life: doctrine — what to believe. Reproof — what is wrong. Correction — how to get right. Instruction in righteousness — how to stay right. The Word is sufficient for all four. Nothing needs to be added.

오늘 성경의 충분성에 헌신하십시오. 인간 전통, 성경 외의 계시, 또는 현재의 문화적 트렌드를 당신의 영적 권위로 추가하려는 유혹에 저항하십시오. 말씀을 여십시오. 그것은 하나님의 호흡입니다. 충분합니다.

Commit to the sufficiency of Scripture today. The inspired Word, rightly divided, produces a complete, equipped, unashamed servant of God. Open it. Trust it. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
  {
    "id": "116",
    "title": "Titus 2:11-13 – The Grace of God That Bringeth Salvation | KJV Right Division",
    "tags": ["Titus 2:11","grace bringeth salvation","KJV","blessed hope","grace","dispensational","한국어"],
    "thumbnail_text": "Grace\nBringeth Salvation",
    "thumbnail_sub": "Titus 2:11-13 | KJV Right Division",
    "thumbnail_bg": (10, 20, 50),
    "script": """Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. Second Timothy two fifteen, King James Bible.

Dear friends, this is the perfect summary of the grace age: grace has appeared — past, the cross. Grace teaches us — present, holy living. We look for the blessed hope — future, the glorious appearing. Past grace, present grace, future grace. All in three verses.

For the grace of God that bringeth salvation hath appeared to all men, Teaching us that, denying ungodliness and worldly lusts, we should live soberly, righteously, and godly, in this present world; Looking for that blessed hope, and the glorious appearing of the great God and our Saviour Jesus Christ. Titus two eleven to thirteen, King James Bible.

Hath appeared to ALL men — not just Israel. The grace of God is universal in its offer. The cross was for all, the Gospel is for all, the invitation is for all. And the motivation for holy living: looking for that blessed hope — the Rapture, the glorious appearing of Christ.

복된 소망은 교회만의 고유한 기대입니다. 우리는 바라보고, 지켜보고, 기다리고 있습니다. 그분이 오늘 오실 수도 있습니다. 그 소망이 우리를 정화합니다 — 더 인내하고, 더 사랑하고, 더 거룩하게 만듭니다.

Live today with the blessed hope. He could come today. Let that reality make you more patient, more loving, more holy, more generous. The grace that saved you sustains you and will one day glorify you. To God be the glory — great things He hath done. Amen.

오늘 이 진리를 누군가와 나누어 주시고 채널을 구독하여 매일 함께 rightly divide 합시다. 주님의 이름으로 기도합니다. Amen.""",
  },
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def load_uploaded():
    if UPLOAD_LOG.exists():
        return json.loads(UPLOAD_LOG.read_text())
    return {}

def save_uploaded(u):
    UPLOAD_LOG.write_text(json.dumps(u, indent=2))

def make_audio(v):
    path = AUDIO_DIR / f"{v['id']}.aiff"
    if path.exists():
        print(f"  [skip audio] {v['id']}")
        return path
    subprocess.run(["say", "-v", MACOS_VOICE, "-o", str(path), v["script"]], check=True)
    print(f"  [audio] {v['id']} done")
    return path

def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, line = [], []
    for w in words:
        test = " ".join(line + [w])
        if draw.textlength(test, font=font) <= max_w:
            line.append(w)
        else:
            if line:
                lines.append(" ".join(line))
            line = [w]
    if line:
        lines.append(" ".join(line))
    return lines

def make_thumbnail(v):
    path = IMG_DIR / f"{v['id']}.png"
    if path.exists():
        return path
    W, H = 1280, 720
    bg = v["thumbnail_bg"]
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    # gradient overlay
    for y in range(H):
        alpha = int(120 * (1 - y / H))
        draw.line([(0, y), (W, y)], fill=(255, 215, 0, alpha))
    # gold border
    draw.rectangle([8, 8, W-8, H-8], outline=(212, 175, 55), width=4)
    try:
        font_big  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 90)
        font_med  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 36)
        font_sm   = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        font_big = font_med = font_sm = ImageFont.load_default()
    # main text
    lines = v["thumbnail_text"].split("\n")
    y = H // 2 - len(lines) * 55
    for line in lines:
        w = draw.textlength(line, font=font_big)
        draw.text(((W - w) / 2, y), line, font=font_big, fill=(255, 255, 255))
        y += 105
    # subtitle
    sub = v["thumbnail_sub"]
    sw = draw.textlength(sub, font=font_med)
    draw.text(((W - sw) / 2, y + 10), sub, font=font_med, fill=(212, 175, 55))
    # badge
    badge = "RIGHTLY DIVIDING KJV"
    bw = draw.textlength(badge, font=font_sm)
    draw.text(((W - bw) / 2, 40), badge, font=font_sm, fill=(212, 175, 55))
    img.save(path)
    return path

def make_video(v, audio_path, img_path):
    path = VIDEO_DIR / f"{v['id']}.mp4"
    if path.exists():
        print(f"  [skip video] {v['id']}")
        return path
    audio = AudioFileClip(str(audio_path))
    clip  = ImageClip(str(img_path)).set_duration(audio.duration).set_audio(audio)
    clip.write_videofile(str(path), fps=1, codec="libx264", audio_codec="aac",
                         logger=None, preset="ultrafast")
    print(f"  [video] {v['id']} done")
    return path

def get_youtube_service():
    creds = None
    if Path(TOKEN_PICKLE).exists():
        with open(TOKEN_PICKLE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, "wb") as f:
            pickle.dump(creds, f)
    return build("youtube", "v3", credentials=creds)

def schedule_time(i):
    day_offset = i // 4 + 1
    slot = i % 4
    h, m = SCHEDULE_TIMES[slot].split(":")
    dt = datetime.datetime(TODAY.year, TODAY.month, TODAY.day,
                           int(h), int(m), 0, tzinfo=KST)
    return dt + datetime.timedelta(days=day_offset)

def upload_video(service, v, video_path, img_path, publish_dt):
    body = {
        "snippet": {
            "title": v["title"],
            "description": (
                f"{v['title']}\n\n"
                "Welcome to Rightly Dividing KJV — a daily Korean/English "
                "dispensational Bible teaching channel.\n\n"
                "📖 Study to shew thyself approved unto God, a workman that needeth "
                "not to be ashamed, rightly dividing the word of truth. — 2 Timothy 2:15 KJV\n\n"
                "🌐 https://henrynkoh.github.io/rightlydividingkjv/\n"
                "✍️ https://rightlydividingtruth.blogspot.com\n\n"
                "#RightlyDividing #KJV #BibleStudy #Dispensational #한국어성경"
            ),
            "tags": v["tags"],
            "categoryId": "27",
            "defaultLanguage": "ko",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_dt.isoformat(),
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    req = service.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    video_id = resp["id"]
    try:
        service.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(str(img_path), mimetype="image/png")
        ).execute()
    except Exception as e:
        print(f"  [thumbnail warn] {e}")
    return video_id

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("=== Rightly Dividing KJV Week 4 Pipeline (89-116) ===\n")
    service  = get_youtube_service()
    uploaded = load_uploaded()

    for i, v in enumerate(VIDEOS):
        print(f"\n[{i+1}/28] Script {v['id']}: {v['title'][:50]}...")
        if v["id"] in uploaded:
            print(f"  [skip] already uploaded → https://youtu.be/{uploaded[v['id']]}")
            continue

        audio_path = make_audio(v)
        img_path   = make_thumbnail(v)
        video_path = make_video(v, audio_path, img_path)
        pub_dt     = schedule_time(i)

        print(f"  [upload] scheduled {pub_dt.strftime('%Y-%m-%d %H:%M KST')}")
        try:
            video_id = upload_video(service, v, video_path, img_path, pub_dt)
            uploaded[v["id"]] = video_id
            save_uploaded(uploaded)
            print(f"  ✓ https://youtu.be/{video_id}")
        except Exception as e:
            print(f"  ✗ Upload failed: {e}")

    print("\n=== Week 4 Pipeline Complete ===")

if __name__ == "__main__":
    main()
