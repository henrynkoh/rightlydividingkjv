"""
Rightly Dividing – Week 2 Pipeline (macOS TTS)
===============================================
Week 2 Theme: Law vs Grace / Moses vs Paul
Scripts 29-58 → Days 8-14 (7AM/12PM/4PM/8PM KST)

Run:
    cd ~/Documents/Claude/Projects/rightlydividing
    python3 pipeline_week2.py
"""

import os, datetime, pytz, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# ─── CONFIG ───────────────────────────────────────────────────────────────────
MACOS_VOICE = "Yuna"

KST   = pytz.timezone("Asia/Seoul")
TODAY = datetime.datetime.now(KST).date()

SCHEDULE_TIMES = ["07:00", "12:00", "16:00", "20:00"]   # KST

YOUTUBE_SCOPES     = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_PICKLE       = "token.pickle"

OUT_DIR   = Path("output")
AUDIO_DIR = OUT_DIR / "audio"
IMG_DIR   = OUT_DIR / "images"
VIDEO_DIR = OUT_DIR / "videos"
for d in [AUDIO_DIR, IMG_DIR, VIDEO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─── WEEK 2 SCRIPTS (29-58) ──────────────────────────────────────────────────
# Scheduling: i=0 → Day+1 7AM, i=1 → Day+1 12PM … i=29 → Day+8 8PM
VIDEOS = [
    # ── DAY 8 ──────────────────────────────────────────────────────────────────
    {
        "id": "29",
        "title": "Exodus 20: The Ten Commandments – For Israel or All People? KJV Right Division",
        "tags": ["Exodus 20","Ten Commandments","Israel","KJV","dispensational","law vs grace","한국어"],
        "thumbnail_text": "Ten Commandments:\nFor Israel or All?",
        "thumbnail_sub": "Exodus 20 | KJV Right Division",
        "thumbnail_bg": (10, 20, 50),
        "script": """I am the LORD thy God, which have brought thee out of the land of Egypt, out of the house of bondage. Exodus 20:2 KJV.

Hello, dear friends. Before God gave even one commandment, He identified His audience. I am the LORD thy God, which brought thee out of Egypt. He was speaking to Israel — the nation He had just delivered from slavery.

Who received the Ten Commandments? Israel. The very introduction tells us. The Gentile nations were never brought out of Egypt. This covenant was made specifically with the nation of Israel at Mount Sinai. Deuteronomy 5:3 confirms — The LORD made not this covenant with our fathers, but with us, even us, who are all of us here alive this day.

Does this mean moral principles — do not murder, do not steal — have no value for us? Absolutely not. These reflect the holy character of God. But as a legal covenant demanding obedience for blessing, the Mosaic Law was given to Israel, not to the Gentile Church. Paul makes this clear — Galatians 3:17 — the Law came 430 years after the promise to Abraham and cannot disannul that promise of grace.

Friend, if you have been carrying the weight of the Ten Commandments as your standard of salvation, hear the good news: you live in the age of grace. Romans 3:28 — we conclude that a man is justified by faith without the deeds of the law.

Leave a comment below and subscribe. Let us rightly divide this Word of Truth together every day. Father, thank You for Your perfect Law that reveals our need, and Your perfect grace that meets that need. In Jesus name. Amen.""",
    },
    {
        "id": "30",
        "title": "Why Was the Law Given? Galatians 3:19 KJV Explained",
        "tags": ["Galatians 3:19","purpose of law","KJV","dispensational","grace","한국어"],
        "thumbnail_text": "Why Was the\nLaw Given?",
        "thumbnail_sub": "Galatians 3:19 | KJV",
        "thumbnail_bg": (30, 15, 45),
        "script": """Wherefore then serveth the law? It was added because of transgressions, till the seed should come to whom the promise was made. Galatians 3:19 KJV.

Hello, dear friends. Today we answer one of the most important questions in all of theology — why did God give the Law?

Notice two key words — added and till. The Law was not the eternal plan. It was added. And it was temporary — only till the seed should come. That seed is Christ Jesus.

Paul is writing to Gentile believers in Galatia who were being pressured to come under the Mosaic Law. His answer is breathtaking — the Law was never meant to be permanent, and it was never meant to save. It was given for a specific purpose, for a specific people, for a specific time.

What was its purpose? Three things. First, to expose transgression — Romans 3:20 says by the law is the knowledge of sin. Second, it was a schoolmaster — Galatians 3:24 says the Law was our schoolmaster to bring us unto Christ. Third, it was temporary — till the seed should come.

Galatians 3:25 — But after that faith is come, we are no longer under a schoolmaster. You have graduated from the Law into grace. Walk in that freedom today.

Leave a comment and subscribe. Let us keep rightly dividing together every day. Lord Jesus, thank You for being the fulfillment of every promise and every requirement. We rest in You alone. Amen.""",
    },
    {
        "id": "31",
        "title": "Romans 6:14 – Not Under Law but Under Grace KJV",
        "tags": ["Romans 6:14","not under law","under grace","KJV","dispensational","한국어"],
        "thumbnail_text": "Not Under Law\nbut Under Grace",
        "thumbnail_sub": "Romans 6:14 | KJV",
        "thumbnail_bg": (10, 40, 20),
        "script": """For sin shall not have dominion over you: for ye are not under the law, but under grace. Romans 6:14 KJV.

Hello, dear friends. Read that again slowly. Ye are not under the law, but under grace. This is not a suggestion — it is a statement of fact about every believer in this age of grace.

What does under the law mean? It means your standing depends on your obedience to His commands. Every failure brings a curse. James 2:10 tells us that whosoever shall keep the whole law, and yet offend in one point, he is guilty of all. Being under law is an impossible and exhausting position.

What does under grace mean? Your standing before God is entirely based on what Christ has done, not what you do. His perfect obedience is credited to your account. His death paid your penalty. His resurrection is your life.

And notice what Paul says results from being under grace — sin shall not have dominion over you. Ironically, it is grace — not law — that gives you power over sin. The Law tells you what not to do but gives you no power to do it. Grace changes your heart from the inside out.

Friend, stop trying to live under a covenant that was never meant for you. You are not a child of the Mosaic covenant — you are a child of grace. Let that truth sink deep today.

Have you experienced the freedom of grace? Tell me in the comments. Subscribe and let us discover more of this grace together every day. Lord, thank You that we are not under law but under grace. Amen.""",
    },
    {
        "id": "32",
        "title": "Colossians 2:14 – The Law Was Nailed to the Cross! KJV",
        "tags": ["Colossians 2:14","nailed to the cross","law","KJV","dispensational","한국어"],
        "thumbnail_text": "The Law Was Nailed\nto the Cross!",
        "thumbnail_sub": "Colossians 2:14 | KJV",
        "thumbnail_bg": (50, 10, 10),
        "script": """Blotting out the handwriting of ordinances that was against us, which was contrary to us, and took it out of the way, nailing it to his cross. Colossians 2:14 KJV.

Hello, beloved friends. Every ordinance, every requirement, every debt we owed to the Law — taken by Christ and nailed to the cross. Gone. Paid. Done.

The handwriting of ordinances refers to the written legal requirements of the Mosaic Law — the Law that stood against us as a record of our failures. Paul says it was against us and contrary to us. The Law could only condemn — it could never save. But Christ took that entire record and nailed it to His cross.

This is why Paul says in verse 16 — Let no man therefore judge you in meat, or in drink, or in respect of an holyday, or of the new moon, or of the sabbath days. Because the Law was nailed to the cross, no one has the right to put you back under its ordinances.

This is a completed act. Verse 14 uses the past tense — nailing it. It is done.

Friend, are you still carrying ordinances that Christ already nailed to His cross? Look to the cross. It is finished. The debt is paid. Walk in the glorious freedom of Colossians 2.

Share what Christ nailed to the cross that used to weigh you down. Subscribe and join us every day. Thank You, Lord Jesus, for the cross that freed us from every ordinance against us. Amen.""",
    },
    # ── DAY 9 ──────────────────────────────────────────────────────────────────
    {
        "id": "33",
        "title": "Hebrews 7:12 – Change of Priesthood, Change of Law | KJV",
        "tags": ["Hebrews 7:12","priesthood changed","law changed","KJV","dispensational","한국어"],
        "thumbnail_text": "Priesthood Changed\n= Law Changed",
        "thumbnail_sub": "Hebrews 7:12 | KJV",
        "thumbnail_bg": (20, 30, 55),
        "script": """For the priesthood being changed, there is made of necessity a change also of the law. Hebrews 7:12 KJV.

Hello, dear friends. Change the priesthood, and the law must change with it. This is a logical and theological statement the writer of Hebrews presents as undeniable.

The Mosaic Law and the Levitical priesthood were inseparably linked. The entire legal system was administered through the tribe of Levi. But Christ came from the tribe of Judah, not Levi. So when God appointed Christ as our High Priest after the order of Melchisedec, it was a declaration that the entire Levitical system had been superseded.

If the priesthood has changed, then the law governing that priesthood has also changed. Christ is our High Priest forever. He offered not the blood of bulls and goats, but His own precious blood. He entered not the earthly tabernacle, but heaven itself. He made not a temporary atonement, but an eternal one.

The old system has given way to the new — not because it was bad, but because it was a shadow pointing to this glorious reality.

Friend, we now have a High Priest who ever liveth to make intercession for us — Hebrews 7:25. You do not need a human priest or a religious ritual to approach God. You come boldly, directly, through Christ.

Leave a comment below. Subscribe and we will keep exploring these glorious truths together. Father, we thank You for our Great High Priest, the Lord Jesus Christ. Amen.""",
    },
    {
        "id": "34",
        "title": "Matthew 5:17-18 – Did Jesus Abolish the Law? KJV Right Division",
        "tags": ["Matthew 5:17","fulfilled not abolished","KJV","dispensational","Jesus and law","한국어"],
        "thumbnail_text": "Did Jesus\nAbolish the Law?",
        "thumbnail_sub": "Matthew 5:17-18 | KJV Right Division",
        "thumbnail_bg": (40, 25, 10),
        "script": """Think not that I am come to destroy the law, or the prophets: I am not come to destroy, but to fulfil. Matthew 5:17 KJV.

Hello, dear friends. Did Jesus abolish the Law? He says — No. He came to fulfil it. But what does that mean for us today?

Context is everything. Jesus spoke these words during His earthly ministry to Israel, before the cross, before Calvary, before His resurrection. At this point, the Law was still fully in effect.

The keyword is fulfilled. Jesus came to fulfil — to completely accomplish — everything the Law required and everything it pointed to. The sacrifices fulfilled in His death. The priesthood fulfilled in His eternal intercession. When Christ cried It is finished on the cross, He was announcing the completion of the Law's requirements.

This is why Paul says in Romans 10:4 — Christ is the end of the law for righteousness to every one that believeth. Not destroyed — ended by fulfillment. A fulfilled contract is not torn up — it is completed. Once a building is built, you do not need the blueprint anymore. The Law was the blueprint; Christ is the building.

Friend, Jesus did not destroy the Law — He honored it perfectly and fulfilled it completely, on your behalf. You stand before God not on your record against the Law, but in Christ who met every requirement.

Share your thoughts in the comments. Subscribe and let us keep rightly dividing together. Lord Jesus, You fulfilled every jot and tittle. Thank You for standing in our place. Amen.""",
    },
    {
        "id": "35",
        "title": "Romans 7:4 – Dead to the Law Through Christ | KJV",
        "tags": ["Romans 7:4","dead to the law","KJV","dispensational","grace","한국어"],
        "thumbnail_text": "Dead to the Law\nThrough Christ",
        "thumbnail_sub": "Romans 7:4 | KJV",
        "thumbnail_bg": (10, 10, 40),
        "script": """Wherefore, my brethren, ye also are become dead to the law by the body of Christ; that ye should be married to another, even to him who is raised from the dead, that we should bring forth fruit unto God. Romans 7:4 KJV.

Hello, dear friends. Paul uses the image of marriage to explain our relationship to the Law. When a husband dies, his wife is free from the marriage law. In the same way, we have died to the Law through Christ — and we are now married to the risen Lord.

In the age of the Law, Israel was married to the Mosaic covenant. Their spiritual identity was defined by the Law. But through Christ's death — and our union with Him in that death — we have died to the Law. We are no longer bound to that old covenant.

Notice the purpose of this new union — that we should bring forth fruit unto God. Fruit — not through striving under legal obligation, but through loving union with the risen Christ. Galatians 5:22 — the fruit of the Spirit.

Romans 7:6 confirms — But now we are delivered from the law, that being dead wherein we were held; that we should serve in newness of spirit, and not in the oldness of the letter.

Friend, you cannot produce spiritual fruit through legal effort. You were designed for a relationship. You are married to Christ — and fruit comes naturally in a loving, living relationship. Abide in Him.

Tell me what fruit your relationship with Christ has produced. Subscribe and let us keep growing. Lord, thank You that we are dead to the law and alive to You. Bear Your fruit in us today. Amen.""",
    },
    {
        "id": "36",
        "title": "Galatians 2:21 – If Law Saves, Christ Died for Nothing | KJV",
        "tags": ["Galatians 2:21","Christ died in vain","law vs grace","KJV","dispensational","한국어"],
        "thumbnail_text": "If Law Saves,\nChrist Died in Vain",
        "thumbnail_sub": "Galatians 2:21 | KJV",
        "thumbnail_bg": (50, 10, 30),
        "script": """I do not frustrate the grace of God: for if righteousness come by the law, then Christ is dead in vain. Galatians 2:21 KJV.

Hello, dear friends. If you can achieve righteousness through keeping the Law — if human effort can make you right with God — then the death of Christ was unnecessary. It was a waste. Paul calls it dying in vain.

To add law-keeping to grace is to frustrate — literally to set aside, to nullify — the grace of God. This is the most dangerous error in the Church in every age. It takes many forms: you must be baptized to be saved; you must tithe; you must keep the sabbath; you must observe the feasts. All of these, when presented as requirements for salvation, are forms of law-keeping that make Christ's death unnecessary.

Either Christ's death was sufficient — fully, completely, eternally sufficient — or it was not enough and we must add something to it. There is no middle ground. Paul says clearly — if law saves, Christ died in vain.

Friend, do not frustrate the grace of God. Do not add one single requirement to the finished work of Christ. Believe on the Lord Jesus Christ — His death for your sins, His burial, His resurrection — and thou shalt be saved. Nothing to add. Nothing to subtract.

Have you ever been taught to add something to Christ for salvation? Share your story below. Subscribe so we can keep protecting this precious Gospel together. Lord Jesus, Your death was not in vain — it was all-sufficient. Amen.""",
    },
    # ── DAY 10 ─────────────────────────────────────────────────────────────────
    {
        "id": "37",
        "title": "What Is the New Covenant? Jeremiah 31 vs Hebrews 8 KJV",
        "tags": ["New Covenant","Jeremiah 31","Hebrews 8","KJV","dispensational","한국어"],
        "thumbnail_text": "What Is the\nNew Covenant?",
        "thumbnail_sub": "Jeremiah 31 vs Hebrews 8 | KJV",
        "thumbnail_bg": (15, 40, 30),
        "script": """Behold, the days come, saith the LORD, that I will make a new covenant with the house of Israel, and with the house of Judah. Jeremiah 31:31 KJV.

Hello, beloved friends. Today we explore one of the most beautiful themes in all of Scripture — the New Covenant.

Jeremiah 31 was written to Israel — specifically the house of Israel and the house of Judah. This is a prophecy of Israel's future restoration, when God will write His law on their hearts and be their God in the fullness of the earthly Kingdom.

Hebrews 8 quotes this prophecy in the context of Christ's superior priesthood. But here is where right division is essential — the New Covenant of Hebrews is specifically with Israel. This is a covenant that will be fully realized in Israel's future kingdom.

The Church — the Body of Christ — participates in the spiritual blessings that flow from Christ's blood. Luke 22:20 — This cup is the new testament in my blood. We benefit from the New Covenant blood of Christ.

The faultiness of the old covenant was not in God — it was in the people. Hebrews 8:8 says — finding fault with them. The Law was holy and good. But it could not change the heart. The New Covenant does what the Law could never do — it transforms from the inside out.

Friend, we live in the blessing of the shed blood of the New Covenant. We have the Holy Spirit, the indwelling presence of God, the forgiveness of sins. This is breathtaking grace.

What does the New Covenant mean to you? Share below. Subscribe and let us keep exploring. Lord, thank You for the New Covenant sealed with the precious blood of Christ. Write Your truth on our hearts. Amen.""",
    },
    {
        "id": "38",
        "title": "2 Corinthians 3:7-11 – Old Glory vs New Glory | KJV",
        "tags": ["2 Corinthians 3:7","old covenant","new covenant","glory","KJV","dispensational","한국어"],
        "thumbnail_text": "Old Glory\nvs New Glory",
        "thumbnail_sub": "2 Corinthians 3:7-11 | KJV",
        "thumbnail_bg": (40, 35, 10),
        "script": """For if the ministration of condemnation be glory, much more doth the ministration of righteousness exceed in glory. 2 Corinthians 3:9 KJV.

Hello, dear friends. Even the Old Covenant had glory. When Moses came down from Sinai, his face shone so brightly that Israel could not look at him. That was real glory. But Paul says that glory was fading — and it was a ministration of condemnation.

Paul draws a four-way contrast. The Old was written on stones — the New is written on hearts. The Old brought death — the New brings life. The Old was a ministration of condemnation — the New is a ministration of righteousness. The Old was fading glory — the New is surpassing, permanent glory.

The Law was glorious — it revealed the holiness of God. But it was designed to fade, to give way, to point forward to something infinitely better. The New Covenant in Christ's blood shines with a glory that does not fade because it is rooted in what Christ accomplished — eternal, perfect, unshakeable.

Verse 11 says — For if that which is done away was glorious, much more that which remaineth is glorious. The old is done away. The new remains. We live in the remaineth.

Friend, you are not living in a fading glory. You are living in the surpassing glory of the New Covenant. Your righteousness flows from Christ's perfect work. That is glory that never fades.

Share in the comments how this changes your day. Subscribe and let us keep shining together. Father, thank You for bringing us out of fading glory into Your surpassing, eternal light. Amen.""",
    },
    {
        "id": "39",
        "title": "Sabbath: Saturday Worship or Grace Principle? Colossians 2:16 KJV",
        "tags": ["Sabbath","Colossians 2:16","Saturday","grace","KJV","dispensational","한국어"],
        "thumbnail_text": "Sabbath: Saturday\nor Grace Principle?",
        "thumbnail_sub": "Colossians 2:16-17 | KJV",
        "thumbnail_bg": (10, 30, 55),
        "script": """Let no man therefore judge you in meat, or in drink, or in respect of an holyday, or of the new moon, or of the sabbath days: Which are a shadow of things to come; but the body is of Christ. Colossians 2:16-17 KJV.

Hello, dear friends. Paul groups the sabbath with other Jewish observances — holydays, new moons, dietary laws. And he says these are a shadow of things to come; but the body is of Christ.

The Sabbath was given to Israel. Exodus 31:17 is explicit — It is a sign between me and the children of Israel for ever. Not between God and all humanity — between God and Israel.

The shadow is the Sabbath — one day of rest pointing forward to something. The body — the substance, the reality — is Christ. Jesus is our rest. Matthew 11:28 — Come unto me, all ye that labour and are heavy laden, and I will give you rest. We enter into His rest not one day a week, but continuously, by faith.

Hebrews 4:9-10 speaks of a remaining Sabbath rest for the people of God — but it is the rest of ceasing from our own works, trusting in Christ's finished work.

Romans 14:5 — One man esteemeth one day above another: another esteemeth every day alike. Let every man be fully persuaded in his own mind. There is no condemnation here.

Friend, in Christ every day is a sabbath. Every moment of trusting His finished work is rest. Live in that rest today.

What day do you worship, and why? Share below. Subscribe and keep rightly dividing with us. Lord Jesus, You are our Sabbath rest. We cease from striving and rest in You. Amen.""",
    },
    {
        "id": "40",
        "title": "Dietary Laws: Still Required? 1 Timothy 4:4-5 KJV Right Division",
        "tags": ["dietary laws","1 Timothy 4:4","clean unclean","KJV","dispensational","한국어"],
        "thumbnail_text": "Dietary Laws:\nStill Required?",
        "thumbnail_sub": "1 Timothy 4:4-5 | KJV",
        "thumbnail_bg": (30, 50, 15),
        "script": """For every creature of God is good, and nothing to be refused, if it be received with thanksgiving: For it is sanctified by the word of God and prayer. 1 Timothy 4:4-5 KJV.

Hello, dear friends. Must Christians observe Old Testament dietary laws? Paul calls the teaching that certain foods must be refused a doctrine of demons — verse 1. And he declares that every creature of God is good and nothing is to be refused.

The dietary laws of Leviticus 11 were given to Israel as part of the Mosaic covenant. Clean and unclean animals were covenant markers — they set Israel apart from surrounding nations.

When Christ came, He declared all foods clean. Mark 7:19 — purging all meats. Acts 10 records God giving Peter a vision of unclean animals and commanding him — What God hath cleansed, that call not thou common. This was a powerful statement that Gentiles, once considered unclean, were now welcomed into God's family through Christ.

Colossians 2:16 echoes this — Let no man judge you in meat, or in drink. Romans 14:14 — I know, and am persuaded by the Lord Jesus, that there is nothing unclean of itself.

This does not mean we throw health wisdom away — eating well is stewardship. But you will not stand before God and be judged for eating pork or shellfish. Those covenant markers belonged to Israel and are fulfilled in Christ.

Friend, receive your food with thanksgiving. That is the New Covenant approach — gratitude, not religious regulation. Subscribe and let us keep studying this glorious grace together. Lord, thank You for grace that sets us free from shadows and gives us substance in Christ. Amen.""",
    },
    # ── DAY 11 ─────────────────────────────────────────────────────────────────
    {
        "id": "41",
        "title": "Tithing: Law Obligation or Grace Giving? 2 Corinthians 9 KJV",
        "tags": ["tithing","grace giving","2 Corinthians 9","KJV","dispensational","한국어"],
        "thumbnail_text": "Tithing: Law\nor Grace Giving?",
        "thumbnail_sub": "2 Corinthians 9 | KJV",
        "thumbnail_bg": (45, 20, 10),
        "script": """Every man according as he purposeth in his heart, so let him give; not grudgingly, or of necessity: for God loveth a cheerful giver. 2 Corinthians 9:7 KJV.

Hello, dear friends. Not grudgingly. Not of necessity. Cheerfully. This is the New Covenant approach to giving — and it is radically different from the tithe.

The tithe — giving ten percent — was commanded in the Mosaic Law. Leviticus 27, Numbers 18, Deuteronomy 14. It was Israel's system for supporting the Levitical priesthood, funding the temple, and providing for the poor. It was a tax built into the theocratic government of Israel.

Malachi 3:10, the famous bring ye all the tithes, was spoken to Israel — specifically to the priests who had been robbing God. Applying it directly to the New Covenant Church removes it entirely from its historical and dispensational context.

In the age of grace, Paul's instruction is completely different. First Corinthians 16:2 — Upon the first day of the week let every one of you lay by him in store, as God hath prospered him. As God has prospered — proportional, voluntary, from the heart.

Second Corinthians 9:6 — He which soweth sparingly shall reap also sparingly; and he which soweth bountifully shall reap also bountifully. The principle is generosity, not a fixed percentage.

Friend, give from your heart, not from legal obligation. Ask God what He would have you give — and give it joyfully, as a worshipping response to His grace.

What does grace giving look like in your life? Share below. Subscribe and let us keep growing in grace together. Lord, You gave Your Son freely. Teach us to give freely and joyfully in return. Amen.""",
    },
    {
        "id": "42",
        "title": "Circumcision Required for Christians? Galatians 5:2-3 KJV Right Division",
        "tags": ["circumcision","Galatians 5:2","KJV","dispensational","grace","한국어"],
        "thumbnail_text": "Circumcision:\nRequired Today?",
        "thumbnail_sub": "Galatians 5:2-3 | KJV",
        "thumbnail_bg": (20, 10, 50),
        "script": """Behold, I Paul say unto you, that if ye be circumcised, Christ shall profit you nothing. For I testify again to every man that is circumcised, that he is a debtor to do the whole law. Galatians 5:2-3 KJV.

Hello, dear friends. If you seek circumcision as a religious requirement for salvation or spiritual standing, you are declaring yourself a debtor to keep the entire Law — and Christ profits you nothing in that arrangement.

Circumcision was the covenant sign of the Abrahamic and Mosaic covenants with Israel. Genesis 17 established it as the physical mark of belonging to God's covenant people. But we are not in the Mosaic covenant — we are in the dispensation of grace.

Galatians 6:15 — For in Christ Jesus neither circumcision availeth any thing, nor uncircumcision, but a new creature. What matters is not the external mark but the internal transformation.

Galatians 5:4 follows with the sobering consequence — those who seek circumcision for righteousness have fallen from grace. They have left the principle of faith and returned to the principle of works.

First Corinthians 7:19 — Circumcision is nothing, and uncircumcision is nothing, but the keeping of the commandments of God. And in the age of grace, the commandment of God is to believe on His Son — First John 3:23.

Friend, your standing before God has nothing to do with any external religious rite. It is entirely about Christ — His work, His blood, His righteousness credited to you by faith. You are sealed by the Holy Spirit of God — Ephesians 1:13. That is your mark.

Subscribe and keep rightly dividing with us every day. Lord Jesus, thank You that we are marked not by flesh but by Your Spirit. Amen.""",
    },
    {
        "id": "43",
        "title": "Paul's Gospel vs Peter's Gospel – Are They the Same? Galatians 2 KJV",
        "tags": ["Paul vs Peter","Galatians 2","KJV","dispensational","gospel","한국어"],
        "thumbnail_text": "Paul vs Peter:\nDifferent Gospels?",
        "thumbnail_sub": "Galatians 2 | KJV Right Division",
        "thumbnail_bg": (50, 25, 5),
        "script": """But when Peter was come to Antioch, I withstood him to the face, because he was to be blamed. Galatians 2:11 KJV.

Hello, dear friends. Paul opposed Peter publicly. Why? And what does this teach us about the Gospel?

Galatians 2 reveals something profound about the dispensational transition happening in the early church. Peter had been sent to the circumcision — to Israel. Paul had been sent to the Gentiles — to the nations. Verse 7 makes this explicit — the gospel of the uncircumcision was committed unto me, as the gospel of the circumcision was unto Peter.

The issue at Antioch was this — Jewish believers, when certain men came from Jerusalem, withdrew from eating with Gentile believers. Paul saw clearly — this behavior contradicted the Gospel of grace. If Gentiles must live as Jews, then Christ's work is not sufficient for Gentiles as Gentiles. The walls that the cross broke down were being rebuilt.

Both Paul and Peter proclaimed Christ crucified. But Paul's revelation of the mystery of the Body of Christ, where all distinctions are erased, was the fuller revelation for this age of grace.

Friend, the grace you have received levels every human distinction. Rich and poor, Jew and Gentile, educated and unlearned — all stand on exactly the same ground at the foot of the cross. Never let anyone build walls that the cross has torn down.

How has the unity of the Body of Christ impacted your life? Share below. Subscribe and let us keep learning. Father, thank You for the Body of Christ where all are one in Him. Help us to live that unity. Amen.""",
    },
    {
        "id": "44",
        "title": "Acts 15 – The Jerusalem Council's Decision on Law and Grace | KJV",
        "tags": ["Acts 15","Jerusalem Council","law vs grace","KJV","dispensational","한국어"],
        "thumbnail_text": "Acts 15:\nJerusalem Council",
        "thumbnail_sub": "Decision on Law & Grace | KJV",
        "thumbnail_bg": (10, 45, 35),
        "script": """Now therefore why tempt ye God, to put a yoke upon the neck of the disciples, which neither our fathers nor we were able to bear? But we believe that through the grace of the Lord Jesus Christ we shall be saved, even as they. Acts 15:10-11 KJV.

Hello, dear friends. Peter himself — speaking to the Jerusalem council — calls the Law a yoke which neither our fathers nor we were able to bear. The foremost apostle of the circumcision admits — the Law was unbearable.

The crisis at Acts 15 was exactly what we face today. Teachers had come to Antioch saying — Except ye be circumcised after the manner of Moses, ye cannot be saved. They were mixing Law and Grace. The Jerusalem Council gathered to settle the matter.

James gives the verdict in verse 19 — Wherefore my sentence is, that we trouble not them, which from among the Gentiles are turned to God. The council wrote to the Gentile churches — you are not required to keep Moses.

The four practical guidelines they gave in verse 29 — abstaining from idols, blood, things strangled, and fornication — were for harmony between Jewish and Gentile believers in mixed communities, not a new Law for salvation.

This council made official what Paul had been preaching — Gentile believers are not under the Mosaic Law. The decision was unanimous, Spirit-led, and recorded in Scripture as precedent for the Church age.

Friend, the question of Acts 15 has already been answered. Definitively. By the council, by the Holy Spirit, by the Word of God. You are saved through the grace of the Lord Jesus Christ.

What yokes have you been freed from? Share below. Subscribe and keep rightly dividing with us. Lord, thank You for freedom from the unbearable yoke and for the easy yoke of Your grace. Amen.""",
    },
    # ── DAY 12 ─────────────────────────────────────────────────────────────────
    {
        "id": "45",
        "title": "Romans 10:4 – Christ Is the End of the Law for Righteousness | KJV",
        "tags": ["Romans 10:4","end of the law","righteousness","KJV","dispensational","한국어"],
        "thumbnail_text": "Christ: End of\nthe Law",
        "thumbnail_sub": "Romans 10:4 | KJV",
        "thumbnail_bg": (35, 10, 50),
        "script": """For Christ is the end of the law for righteousness to every one that believeth. Romans 10:4 KJV.

Hello, beloved friends. Christ is the end of the Law. For righteousness. For everyone who believes.

The word end here is the Greek telos — it means goal, purpose, culmination. Christ is the goal toward which the Law always pointed. The Law was never the destination — it was the road leading to the destination, who is Christ.

What was the Law's goal? Righteousness — being right before God. But the Law could never produce righteousness. Romans 3:20 — by the deeds of the law there shall no flesh be justified. The Law shows us the standard, exposes our failure, and points us to the One who met the standard perfectly.

Now Christ has come. The goal has been reached. And this is to every one that believeth — not to the circumcised, not to the religiously observant, not to the law-keeper. To every one who believes.

Romans 10:9-10 follows immediately — That if thou shalt confess with thy mouth the Lord Jesus, and shalt believe in thine heart that God hath raised him from the dead, thou shalt be saved. Righteousness through belief — not through law.

This means the endless treadmill of trying to earn God's approval through religious performance is over. Christ met every requirement of the Law on your behalf. His perfect righteousness is credited to your account the moment you believe.

Friend, stop running on the treadmill. The race was run. Christ finished it. Believe, and receive His righteousness today. Subscribe and let us keep growing together. Lord Jesus, You are the end — the goal — of every longing and every law. We rest in You. Amen.""",
    },
    {
        "id": "46",
        "title": "Galatians 5:18 – Led by the Spirit, Not Under the Law | KJV",
        "tags": ["Galatians 5:18","led by Spirit","not under law","KJV","dispensational","한국어"],
        "thumbnail_text": "Led by the Spirit,\nNot Under Law",
        "thumbnail_sub": "Galatians 5:18 | KJV",
        "thumbnail_bg": (10, 35, 55),
        "script": """But if ye be led of the Spirit, ye are not under the law. Galatians 5:18 KJV.

Hello, dear friends. This single sentence answers one of the great anxieties of the Christian life — if I am not under the Law, what guides me? What stops me from living any way I please? The answer — the Spirit.

The Law works from the outside in — rules imposed from without. The Spirit works from the inside out — transformation from within. The Law says Thou shalt not — and leaves you to your own strength. The Spirit produces fruit naturally in a yielded heart — love, joy, peace, longsuffering, gentleness, goodness, faith, meekness, temperance. No law is needed to tell you that love is good.

Galatians 5:17 acknowledges the conflict — the flesh lusts against the Spirit. But the solution to that conflict is not more law — it is more Spirit. Walk in the Spirit — verse 16 — and you will not fulfill the lust of the flesh.

This is the radical difference between the dispensation of Law and the dispensation of Grace. Israel had the Law written on stone. We have the Spirit dwelling within. Ezekiel 36:27 prophesied it — I will put my spirit within you, and cause you to walk in my statutes. The Spirit does what the Law never could.

Friend, you do not need a list of rules to live righteously. You need the Spirit — and if you are saved, He already lives in you. Yield to Him. Listen to Him. Follow His leading.

How has the Spirit led you recently? Share below. Subscribe and let us keep following Him together. Holy Spirit, lead us today. We yield ourselves to Your guidance and power. Amen.""",
    },
    {
        "id": "47",
        "title": "1 Timothy 1:8-9 – The Law Is Good When Used Lawfully | KJV",
        "tags": ["1 Timothy 1:8","law is good","lawfully","KJV","dispensational","한국어"],
        "thumbnail_text": "Law Is Good\nWhen Used Lawfully",
        "thumbnail_sub": "1 Timothy 1:8-9 | KJV",
        "thumbnail_bg": (45, 30, 10),
        "script": """But we know that the law is good, if a man use it lawfully; Knowing this, that the law is not made for a righteous man, but for the lawless and disobedient, for the ungodly and for sinners. 1 Timothy 1:8-9 KJV.

Hello, dear friends. The Law is good — Paul affirms that. But it must be used lawfully. And here is the key — it is not made for the righteous. It is made for the lawless.

This is a crucial dispensational insight. The Law serves as a restrainer and revealer of sin among the unrighteous. It exposes lawlessness, defines transgression, and points the sinner to his need for a Savior. That is its proper, lawful use.

But when you take the Law and apply it to a justified believer — someone who is already righteous in Christ — you are using it unlawfully. The Law was not designed for those who are already declared righteous by God through faith.

Paul goes on to list the kinds of people the Law addresses — lawless, disobedient, ungodly, sinners, unholy, profane, murderers. The Law speaks directly to unrestrained sin and rebellion. It is a legal instrument for a courtroom, not a nourishment tool for a family.

We who are in Christ have been declared righteous — Romans 5:1 and 8:1. The Law's condemning, restraining function is not directed at us. We are guided by the Spirit of God who lives within us.

Friend, preach the Law to the sinner to reveal his need for Christ. But do not use it to condemn the believer who stands righteous in Christ. That is using the Law lawfully.

Share your thoughts below. Subscribe and let us keep learning together. Lord, help us to use Your Law as You intended — to point sinners to Christ. Amen.""",
    },
    {
        "id": "48",
        "title": "Hebrews 10:1 – The Law Was a Shadow; Christ Is the Reality | KJV",
        "tags": ["Hebrews 10:1","shadow vs reality","law","KJV","dispensational","한국어"],
        "thumbnail_text": "Law Was a Shadow;\nChrist Is Reality",
        "thumbnail_sub": "Hebrews 10:1 | KJV",
        "thumbnail_bg": (20, 20, 60),
        "script": """For the law having a shadow of good things to come, and not the very image of the things, can never with those sacrifices which they offered year by year continually make the comers thereunto perfect. Hebrews 10:1 KJV.

Hello, beloved. Think about what a shadow is — it is a real indicator that something solid is nearby, but it has no substance of its own. You cannot hold a shadow. You cannot be nourished by a shadow. The shadow's entire value is in pointing you to the object that casts it.

The Law was a shadow — a real, God-given shadow — of good things to come. The sacrifices were shadows of Christ's one perfect sacrifice. The priesthood was a shadow of Christ's eternal priesthood. The tabernacle was a shadow of the true heavenly sanctuary. The feasts were shadows of Christ's death, resurrection, and coming kingdom.

The writer's argument is devastating to any system that tries to keep Christians under the Law — Can never with those sacrifices which they offered year by year continually make the comers thereunto perfect. Year after year, the same sacrifices, the same blood of animals — and still no perfection. Because they were shadows, not the reality.

Then comes chapter 10:12 — But this man, after he had offered one sacrifice for sins for ever, sat down on the right hand of God. One sacrifice. For sins. For ever. He sat down — because the work is finished.

Friend, why would you return to shadows when you have the substance Himself? Every shadow in the Old Testament was pointing you to Jesus — receive Him fully today.

Which shadow-to-reality connection most amazes you? Tell me below. Subscribe and let us keep marveling together. Lord Jesus, You are the reality behind every shadow. We come to You. Amen.""",
    },
    # ── DAY 13 ─────────────────────────────────────────────────────────────────
    {
        "id": "49",
        "title": "Why Study the Old Testament If We Are Under Grace? | KJV Right Division",
        "tags": ["Old Testament","why study","grace","KJV","dispensational","2 Timothy 3:16","한국어"],
        "thumbnail_text": "Why Study\nthe Old Testament?",
        "thumbnail_sub": "2 Timothy 3:16 | KJV Right Division",
        "thumbnail_bg": (40, 20, 10),
        "script": """All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness. 2 Timothy 3:16 KJV.

Hello, dear friends. If we are under grace and not the Law, why bother studying the Old Testament? All Scripture. That includes every book of the Old Testament.

Here is the key distinction — all Scripture is written for us, but not all Scripture is written to us. The dietary laws of Leviticus were written to Israel. The sacrificial system was given to Israel's priests. These are not binding on the Church as law. But they are infinitely valuable as revelation.

Romans 15:4 — For whatsoever things were written aforetime were written for our learning, that we through patience and comfort of the scriptures might have hope. Written for our learning. Our patience. Our hope.

What do we gain from the Old Testament? History of God's dealings with mankind — so we understand His character. Prophecy — so we see His sovereignty over all ages. Types and shadows — so we appreciate the fullness of Christ. Wisdom literature — Psalms, Proverbs — timeless principles of human life under God.

First Corinthians 10:11, speaking of Israel's wilderness experiences — Now all these things happened unto them for ensamples: and they are written for our admonition. Their story is our warning and our encouragement.

Friend, read your whole Bible. But read it rightly divided — asking always: to whom was this written? In which dispensation? How does this point to Christ? And how does this nourish my soul today? That is right division in practice.

What Old Testament passage most impacts your faith? Share below. Subscribe and let us keep studying together. Lord, show us how all Scripture glorifies Jesus. Amen.""",
    },
    {
        "id": "50",
        "title": "Types and Shadows – How the Law Points to Christ | KJV",
        "tags": ["types and shadows","law points to Christ","KJV","dispensational","typology","한국어"],
        "thumbnail_text": "Types & Shadows:\nPointing to Christ",
        "thumbnail_sub": "Colossians 2:17 | KJV",
        "thumbnail_bg": (15, 45, 25),
        "script": """These are a shadow of things to come; but the body is of Christ. Colossians 2:17 KJV.

Hello, dear friends. The body — the substance, the reality — is of Christ. Everything in the Law was a finger pointing forward to Him.

A type is an Old Testament person, event, or institution that prefigures something greater in the New Testament — specifically Christ and His work. Once you see them, you cannot unsee them — and the Word comes alive in a new way.

Consider just a few. Adam — the first Adam brought death; Christ, the last Adam, brings life. First Corinthians 15:45. The Passover Lamb — slain without blemish, blood on the doorposts, death passes over. Christ is our Passover sacrificed for us. First Corinthians 5:7. The brazen serpent — lifted up on a pole so that whoever looked would live. Jesus said — As Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up. John 3:14. Jonah's three days in the whale — Christ's three days in the earth. Matthew 12:40.

This is not fanciful interpretation — Jesus himself taught it. Luke 24:27 — And beginning at Moses and all the prophets, he expounded unto them in all the scriptures the things concerning himself.

Friend, when you read the Old Testament and see a type of Christ, worship. God was announcing the Gospel in pictures for thousands of years before the cross. His plan was never uncertain. It was always Christ — from Genesis to Malachi.

What is your favorite type of Christ in the Old Testament? Please share below. Subscribe and let us keep finding Christ on every page. Lord Jesus, You are on every page. Open our eyes to see You. Amen.""",
    },
    {
        "id": "51",
        "title": "Moral Law vs Ceremonial Law – Does the Distinction Hold? | KJV Right Division",
        "tags": ["moral law","ceremonial law","KJV","dispensational","right division","한국어"],
        "thumbnail_text": "Moral vs Ceremonial\nLaw: Right Division",
        "thumbnail_sub": "KJV Dispensational Study",
        "thumbnail_bg": (50, 15, 35),
        "script": """For verily I say unto you, Till heaven and earth pass, one jot or one tittle shall in no wise pass from the law, till all be fulfilled. Matthew 5:18 KJV.

Hello, dear friends. Many teachers divide the Mosaic Law into moral law, which is permanent, and ceremonial law, which is temporary. Is this a valid biblical distinction?

The idea has practical appeal — it explains why we do not offer animal sacrifices but do still say do not murder. But here is the challenge — the Bible never divides the Law this way. The Law of Moses was presented as a unified whole. James 2:10 says breaking one point makes you guilty of all.

What the Bible does teach is that the entire Mosaic covenant was a package given to one nation for one dispensation. Romans 7:6 says we are delivered from the law.

Does that mean thou shalt not murder is now optional? Absolutely not. But here is the important distinction — the moral principles behind the Law reflect God's eternal character — and these are restated and reaffirmed in Paul's letters for the Church. Nine of the Ten Commandments appear in Paul's epistles. The Sabbath commandment is the one not restated — because Christ is our sabbath rest.

So it is not that the moral law is eternal as a legal system — it is that the moral character of God reflected in those commands never changes. And in Christ, we fulfill the righteousness of the Law naturally through love and the Spirit — Romans 8:4.

Friend, God's character never changes. But your relationship to His commands has changed — from legal obligation to loving response. You love others because Christ has loved you. That is grace.

Share your thoughts below. Subscribe and keep rightly dividing with us. Lord, thank You that love fulfills every righteous requirement. Amen.""",
    },
    {
        "id": "52",
        "title": "Romans 13:8-10 – Love Fulfills the Law | KJV Right Division",
        "tags": ["Romans 13:8","love fulfills law","KJV","dispensational","grace","한국어"],
        "thumbnail_text": "Love Fulfills\nthe Law",
        "thumbnail_sub": "Romans 13:8-10 | KJV",
        "thumbnail_bg": (10, 40, 20),
        "script": """Owe no man any thing, but to love one another: for he that loveth another hath fulfilled the law. Love worketh no ill to his neighbour: therefore love is the fulfilling of the law. Romans 13:8 and 10 KJV.

Hello, beloved friends. He that loveth another hath fulfilled the law. Love is the fulfilling of the law.

Paul lists several commandments — do not commit adultery, do not kill, do not steal, do not bear false witness — and says they are briefly comprehended in this saying — Thou shalt love thy neighbour as thyself.

This does not mean the commandments are irrelevant. It means love naturally produces what the commandments required. If you genuinely love your neighbor, you will not murder him, steal from him, or lie about him. Love is not less than the Law — it is more. It goes beyond external compliance to internal transformation.

Jesus called love the greatest commandment — Matthew 22:37-40. Paul builds on that foundation. In Christ, we are not less moral than law-keepers — we are more moral, because love motivates from within rather than compulsion from without.

First John 4:19 — We love him, because he first loved us. The sequence matters — God's love to us first, our love to others as a response. Grace motivates love. Love fulfills the Law. No whip needed. No threat of punishment. Just the overwhelming reality of having been loved at infinite cost.

Friend, if you want to keep the Law, love. Love God with everything you have, and love your neighbor as yourself. You will find that you have fulfilled its every requirement — not as a legal duty, but as a joyful expression of who you are in Christ.

Who has God put in your life to love this week? Share below. Subscribe and let us keep loving and learning together. Lord, Your love has been shed abroad in our hearts. May it overflow to everyone around us. Amen.""",
    },
    # ── DAY 14 ─────────────────────────────────────────────────────────────────
    {
        "id": "53",
        "title": "Freedom in Christ – What Does It Really Mean? Galatians 5:1 KJV",
        "tags": ["freedom in Christ","Galatians 5:1","liberty","KJV","dispensational","한국어"],
        "thumbnail_text": "Freedom in Christ:\nWhat Does It Mean?",
        "thumbnail_sub": "Galatians 5:1 | KJV",
        "thumbnail_bg": (30, 50, 10),
        "script": """Stand fast therefore in the liberty wherewith Christ hath made us free, and be not entangled again with the yoke of bondage. Galatians 5:1 KJV.

Hello, dear friends. Christ has made us free. Stand fast in that freedom. Do not get entangled again in a yoke of bondage.

Paul is writing to Gentile believers who were being pressured to adopt Jewish law observance. He calls this legal system a yoke of bondage — not because it was evil, but because it was never designed for Gentile believers in this age of grace, and because it could never justify and sanctify believers before God.

What is the freedom Christ gives? Three dimensions. First, freedom from the guilt of sin — Romans 8:1 — There is therefore now no condemnation to them which are in Christ Jesus. Your past is forgiven, your record is clean. Second, freedom from the power of sin — Romans 6:14 — sin shall not have dominion over you. Third, freedom from the bondage of religious performance — you do not earn God's love or maintain it by your spiritual efforts. It is given freely and held securely by God Himself.

But Paul is clear — freedom is not license. Galatians 5:13 — use not liberty for an occasion to the flesh, but by love serve one another. Freedom from law is not freedom to sin. It is freedom to love.

Friend, stand fast. When someone tries to put you back under religious rules, stand fast. When guilt tries to steal your peace, stand fast. Christ has made you free. Live it.

What has Christ freed you from? Please share below. Subscribe and let us keep standing fast together. Lord Jesus, You have set us free. Help us to stand firm in that freedom and use it to love. Amen.""",
    },
    {
        "id": "54",
        "title": "Legalism – The Danger in Today's Church | KJV Right Division",
        "tags": ["legalism","danger","church","KJV","dispensational","grace","한국어"],
        "thumbnail_text": "Legalism:\nDanger in the Church",
        "thumbnail_sub": "Galatians 5:16 | KJV Right Division",
        "thumbnail_bg": (55, 10, 10),
        "script": """This I say then, Walk in the Spirit, and ye shall not fulfil the lust of the flesh. Galatians 5:16 KJV.

Hello, dear friends. Legalism does not solve the flesh problem. Only the Spirit does.

Legalism is the error of adding human rules and religious requirements to the grace of God — either for salvation or for spiritual growth and acceptance. It takes many forms in today's church. You must follow a specific dress code to be truly holy. You must attend a certain number of services to be a good Christian. You must abstain from certain entertainment or music that is not sinful in itself. You must give a specific percentage or face spiritual consequence. You must speak in tongues to be truly Spirit-filled.

Each of these, when elevated to a requirement for God's acceptance, is legalism. And legalism has devastating effects. It produces pride in those who manage to comply — and shame and defeat in those who cannot. It turns the Christian life into a performance review rather than a love relationship. It keeps people focused on external behavior rather than internal transformation. And ultimately, it empties the cross of its glory — because it implies that Christ's work is not enough.

Colossians 2:23 — Paul describes human-made religious rules as having a shew of wisdom in will worship, and humility, and neglecting of the body; not in any honour to the satisfying of the flesh. They look spiritual, but they do not actually produce holiness.

Friend, examine the standards you are living by. Which come from God's Word, rightly divided? And which come from human tradition, church culture, or religious pressure? God's requirements bring life. Legalistic requirements bring bondage.

Have you experienced legalism in your church journey? Share below. Subscribe and let us keep walking in freedom together. Lord, free Your Church from the chains of legalism and lead us into the glorious freedom of Your grace. Amen.""",
    },
    {
        "id": "55",
        "title": "Grace Giving vs Law Tithing – A Deeper Look | 2 Corinthians 8-9 KJV",
        "tags": ["grace giving","tithing","2 Corinthians 8","KJV","dispensational","한국어"],
        "thumbnail_text": "Grace Giving vs\nLaw Tithing",
        "thumbnail_sub": "2 Corinthians 8-9 | KJV Deep Dive",
        "thumbnail_bg": (20, 40, 50),
        "script": """For ye know the grace of our Lord Jesus Christ, that, though he was rich, yet for your sakes he became poor, that ye through his poverty might be rich. 2 Corinthians 8:9 KJV.

Hello, beloved friends. This is the model and motivation for grace giving — not a percentage, but the example of Christ Himself.

Second Corinthians chapters 8 and 9 are Paul's masterful teaching on Christian generosity. Nowhere in these chapters does he command a tithe. Nowhere does he invoke Malachi 3. The giving he describes is characterized by completely different principles.

In Second Corinthians 8:3, Paul commends the Macedonian churches who gave beyond their power — willingly. Not ten percent — beyond their ability, out of joy. Verse 12 — if there be first a willing mind, it is accepted according to that a man hath. Willingness, not percentage.

Chapter 9 verse 6 — He which soweth sparingly shall reap also sparingly; and he which soweth bountifully shall reap also bountifully. This is agricultural imagery of proportional, voluntary sowing — not legal obligation. Verse 7 — not grudgingly, or of necessity. The tithe was of necessity — it was law. Grace giving is never of necessity.

The model is Christ — who became poor so we could be rich. Giving that flows from contemplating that sacrifice is the most powerful giving in the universe. It has no percentage ceiling.

Friend, give from the overflow of your gratitude for Christ. Let the generosity of the cross inspire the generosity of your life. Every gift motivated by love for Christ and compassion for others is precious to God.

How has your understanding of giving changed through grace? Share below. Subscribe and let us keep learning together. Lord Jesus, You gave everything. May Your generosity overflow through us. Amen.""",
    },
    {
        "id": "56",
        "title": "Israel's Feasts vs Church Holy Days – Right Division | KJV",
        "tags": ["feasts of Israel","holy days","church","KJV","dispensational","Colossians 2:16","한국어"],
        "thumbnail_text": "Israel's Feasts\nvs Church Holy Days",
        "thumbnail_sub": "Colossians 2:16-17 | KJV",
        "thumbnail_bg": (40, 25, 50),
        "script": """Let no man therefore judge you in meat, or in drink, or in respect of an holyday, or of the new moon, or of the sabbath days: Which are a shadow of things to come; but the body is of Christ. Colossians 2:16-17 KJV.

Hello, dear friends. Today we look at Israel's feasts and their relationship to the Church.

God gave Israel seven feasts in Leviticus 23 — Passover, Unleavened Bread, Firstfruits, Pentecost, Trumpets, Atonement, and Tabernacles. These were covenant obligations for Israel, calendar markers of their national and spiritual identity.

But they were also something more — they were prophetic shadows of Christ's work. Passover was fulfilled when Christ, our Passover Lamb, was crucified on Passover day. Unleavened Bread — His sinless body in the grave. Firstfruits — His resurrection, the firstfruits of those who sleep. Pentecost — the giving of the Spirit to the Church, exactly fifty days after resurrection.

The fall feasts — Trumpets, Atonement, Tabernacles — have not yet been fulfilled. They point to Christ's second coming, Israel's national repentance, and the millennial kingdom. Breathtaking prophetic precision.

For the Church today — Colossians 2:16 says clearly — let no man judge you regarding these observances. They are shadows. The body is Christ. We are not required to observe the Jewish feasts. But studying them reveals Christ on every page.

Friend, when you see the feasts of Israel, see Christ. Every feast is a portrait of Him. Worship Him who fulfilled them all.

Which feast most excites you as a portrait of Christ? Share below. Subscribe and let us keep marveling at Christ together. Lord Jesus, You are the fulfillment of every feast. We celebrate You. Amen.""",
    },
    {
        "id": "57",
        "title": "Priesthood of All Believers – 1 Peter 2:9 vs Old Testament | KJV",
        "tags": ["priesthood of believers","1 Peter 2:9","KJV","dispensational","access to God","한국어"],
        "thumbnail_text": "All Believers\nAre Priests",
        "thumbnail_sub": "1 Peter 2:9 | KJV Right Division",
        "thumbnail_bg": (10, 50, 40),
        "script": """But ye are a chosen generation, a royal priesthood, an holy nation, a peculiar people; that ye should shew forth the praises of him who hath called you out of darkness into his marvellous light. 1 Peter 2:9 KJV.

Hello, beloved friends. A royal priesthood. Every believer.

In the Old Testament, the priesthood was strictly limited. Only the tribe of Levi could serve as priests. Only the family of Aaron could offer sacrifices. Only the High Priest could enter the Holy of Holies — and only once a year, with blood. The distance between ordinary Israelite and the presence of God was structured, mediated, and heavily regulated.

When Christ died on the cross, the veil of the temple was torn from top to bottom — Matthew 27:51. That veil had separated the Holy of Holies from the rest of the temple. Its tearing was God's announcement — the way into His presence is now open to all.

Hebrews 4:16 — Let us therefore come boldly unto the throne of grace, that we may obtain mercy, and find grace to help in time of need. Boldly — not trembling at a distance, but boldly. Why? Because we have a High Priest — Christ — who has gone before us and opened the way.

Now every believer is a priest. You do not need a human mediator to access God. You come directly, personally, boldly — through Christ alone. First Timothy 2:5 — For there is one God, and one mediator between God and men, the man Christ Jesus.

Friend, you are a priest. You have direct access to the throne of God right now. Use it. Come boldly. Bring your needs, your praise, your intercession — directly to the Father through Christ.

What does direct access to God mean to you? Share below. Subscribe and let us keep approaching the throne together. Father, thank You for the open way through Jesus. We come boldly to Your throne right now. Amen.""",
    },
    {
        "id": "58",
        "title": "One Mediator: Moses vs Christ – 1 Timothy 2:5 KJV",
        "tags": ["1 Timothy 2:5","one mediator","Moses vs Christ","KJV","dispensational","한국어"],
        "thumbnail_text": "One Mediator:\nMoses vs Christ",
        "thumbnail_sub": "1 Timothy 2:5 | KJV",
        "thumbnail_bg": (25, 15, 55),
        "script": """For there is one God, and one mediator between God and men, the man Christ Jesus; Who gave himself a ransom for all, to be testified in due time. 1 Timothy 2:5-6 KJV.

Welcome, dear friends. We come to the final message of Week 2. One mediator. Not Moses. Not Mary. Not the church. Not a priest. Not your pastor. One — the man Christ Jesus.

In the dispensation of Law, Moses served as a mediator between God and Israel. He received the Law on their behalf, interceded when they sinned, and stood in the gap for the nation. Deuteronomy 5:5 — I stood between the LORD and you at that time. Moses was a type — a shadow — of the perfect Mediator to come.

But Moses was finite, sinful himself — he needed a sacrifice for his own sin. He could not bear the full weight of God's holiness and human need simultaneously. He was a picture, not the reality.

Christ is the reality. He is the God-Man — fully God, fully man — uniquely qualified to stand between a holy God and sinful humanity. He did not just deliver God's law — He fulfilled it. He did not just intercede for sin — He bore sin. He did not just stand in the gap — He closed it permanently through His own blood.

Who gave himself a ransom for all — this is the ground of the mediation. He paid the ransom. The price is settled. The debt is cleared.

Friend, you need no earthly mediator. No saint, no priest, no religious system can bring you to God. But you have One who can — and He is alive, risen, interceding for you right now at the right hand of the Father.

Thank you for studying Law vs Grace with me this week. Leave a comment, share this channel, and subscribe so we can keep rightly dividing this glorious Word together every day. Lord Jesus, You are our one Mediator, our ransom, our righteousness. All glory to Your name. Forever and ever. Amen.""",
    },
]

# ─── STEP 1: AUDIO ────────────────────────────────────────────────────────────
def generate_audio():
    print("\n=== STEP 1: Generating Audio (macOS TTS) ===")
    for v in VIDEOS:
        aiff_path = AUDIO_DIR / f"{v['id']}.aiff"
        if aiff_path.exists():
            print(f"  [skip] {aiff_path.name} already exists")
            continue
        print(f"  Generating {aiff_path.name} ...")
        subprocess.run([
            "say", "-v", MACOS_VOICE, "-o", str(aiff_path), v["script"]
        ], check=True)
        print(f"  Saved → {aiff_path}")

# ─── STEP 2: THUMBNAIL ────────────────────────────────────────────────────────
def make_thumbnail(v):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), color=v["thumbnail_bg"])
    draw = ImageDraw.Draw(img)

    border = 24
    draw.rectangle([border, border, W-border, H-border], outline=(212, 175, 55), width=4)
    draw.rectangle([border+4, H//2-6, W-border-4, H//2+6], fill=(212, 175, 55))

    try:
        font_big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except Exception:
        font_big = font_sub = ImageFont.load_default()

    lines = v["thumbnail_text"].split("\n")
    y = 120
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=font_big)
        x = (W - (bb[2] - bb[0])) // 2
        draw.text((x, y), line, font=font_big, fill=(255, 255, 255))
        y += 110

    bb = draw.textbbox((0, 0), v["thumbnail_sub"], font=font_sub)
    x = (W - (bb[2] - bb[0])) // 2
    draw.text((x, H - 140), v["thumbnail_sub"], font=font_sub, fill=(212, 175, 55))

    tag = "@ohhenry6524  |  Rightly Dividing"
    bb = draw.textbbox((0, 0), tag, font=font_sub)
    x = (W - (bb[2] - bb[0])) // 2
    draw.text((x, H - 80), tag, font=font_sub, fill=(180, 180, 180))

    path = IMG_DIR / f"{v['id']}.png"
    img.save(path)
    return path

# ─── STEP 3: VIDEO ────────────────────────────────────────────────────────────
def generate_videos():
    print("\n=== STEP 2: Generating Thumbnails & Videos ===")
    for v in VIDEOS:
        vpath = VIDEO_DIR / f"{v['id']}.mp4"
        if vpath.exists():
            print(f"  [skip] {vpath.name} already exists")
            continue
        thumb = make_thumbnail(v)
        audio_path = AUDIO_DIR / f"{v['id']}.aiff"
        audio = AudioFileClip(str(audio_path))
        clip  = ImageClip(str(thumb)).set_duration(audio.duration).set_audio(audio)
        clip.write_videofile(str(vpath), fps=1, codec="libx264", audio_codec="aac", logger=None)
        print(f"  Saved → {vpath}")

# ─── STEP 4: YOUTUBE AUTH ─────────────────────────────────────────────────────
def get_youtube_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, "wb") as f:
            pickle.dump(creds, f)
    return build("youtube", "v3", credentials=creds)

# ─── STEP 5: UPLOAD ───────────────────────────────────────────────────────────
def upload_videos():
    print("\n=== STEP 3: Uploading to YouTube (scheduled) ===")
    yt = get_youtube_service()

    for i, v in enumerate(VIDEOS):
        day_offset = i // 4 + 1          # i=0 → Day+1, i=4 → Day+2 …
        slot       = i % 4               # 0→7AM, 1→12PM, 2→4PM, 3→8PM
        h, m = SCHEDULE_TIMES[slot].split(":")
        publish_dt = datetime.datetime(
            TODAY.year, TODAY.month, TODAY.day,
            int(h), int(m), 0,
            tzinfo=KST
        ) + datetime.timedelta(days=day_offset)

        publish_iso = publish_dt.isoformat()
        vpath = VIDEO_DIR / f"{v['id']}.mp4"
        tpath = IMG_DIR    / f"{v['id']}.png"

        print(f"  Uploading: {v['title'][:60]}...")
        print(f"  Schedule:  {publish_iso}")

        body = {
            "snippet": {
                "title": v["title"],
                "description": (
                    "📖 Study to shew thyself approved unto God, a workman that needeth not to be ashamed, "
                    "rightly dividing the word of truth. (2 Timothy 2:15 KJV)\n\n"
                    "Subscribe for daily KJV Right Division Bible study.\n"
                    "@ohhenry6524\n\n"
                    "#RightlyDividing #KJV #BibleStudy #Dispensational #은혜의복음 #LawVsGrace"
                ),
                "tags": v["tags"],
                "categoryId": "27",
                "defaultLanguage": "ko",
                "defaultAudioLanguage": "ko",
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_iso,
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(str(vpath), chunksize=-1, resumable=True, mimetype="video/mp4")
        req   = yt.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            _, response = req.next_chunk()

        video_id = response["id"]

        try:
            yt.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(tpath), mimetype="image/png")
            ).execute()
            print(f"  ✓ Thumbnail set")
        except Exception as e:
            print(f"  ⚠ Thumbnail skipped: {e}")

        print(f"  ✓ Uploaded → https://youtu.be/{video_id}  (publishes {publish_iso})")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    generate_audio()
    generate_videos()
    upload_videos()
    print("\n✅ All done! 30 videos (Week 2) scheduled on @ohhenry6524.")
