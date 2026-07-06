"""
Rightly Dividing KJV – Blogspot Auto-Poster
============================================
Posts all 88 blog posts to rightlydividing.blogspot.com
Scheduled 4x/day: 7AM, 12PM, 4PM, 8PM KST

Run:
    cd ~/Documents/Claude/Projects/rightlydividing
    python3 blog_poster.py
"""

import os, datetime, json, pickle
import pytz
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BLOG_ID            = None          # auto-fetched from rightlydividing.blogspot.com
BLOG_URL           = "rightlydividingtruth.blogspot.com"
CLIENT_SECRET_FILE = "client_secret.json"
BLOG_TOKEN_PICKLE  = "token_blog.pickle"
SCOPES             = ["https://www.googleapis.com/auth/blogger"]
KST                = pytz.timezone("Asia/Seoul")
TODAY              = datetime.datetime.now(KST).date()
SCHEDULE_TIMES     = ["07:00", "12:00", "16:00", "20:00"]

# ─── HTML TEMPLATE ────────────────────────────────────────────────────────────
def make_html(p):
    labels_str = " · ".join(f'<span style="background:rgba(212,175,55,0.15);color:#d4af37;padding:2px 10px;border-radius:12px;font-size:0.75rem;">{l}</span>' for l in p["labels"])
    return f"""<div style="font-family:Georgia,serif;max-width:700px;margin:0 auto;padding:8px 0;color:#1a1a2e;">

<!-- Badge -->
<div style="text-align:center;margin-bottom:22px;">
  <span style="background:#0d1f3c;color:#d4af37;font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;padding:6px 18px;border-radius:20px;">Week {p['week']} · Day {p['day']}-{p['slot']} · 2 Timothy 2:15 KJV</span>
</div>

<!-- KJV Verse -->
<div style="background:#0d1f3c;border-left:5px solid #d4af37;padding:20px 24px;border-radius:0 8px 8px 0;margin-bottom:26px;">
  <p style="color:#e8e0d0;font-style:italic;font-size:1.05rem;margin:0 0 10px;line-height:1.65;">&ldquo;{p['verse_text']}&rdquo;</p>
  <cite style="color:#d4af37;font-size:0.82rem;font-style:normal;letter-spacing:1px;">— {p['verse_ref']}</cite>
</div>

<!-- Intro -->
<p style="font-size:1.02rem;line-height:1.78;margin-bottom:18px;color:#2c2c3e;">{p['intro']}</p>

<!-- Right Division -->
<div style="background:#f5f0e8;border-left:4px solid #d4af37;padding:16px 20px;margin:22px 0;border-radius:0 6px 6px 0;">
  <strong style="color:#8b1a1a;font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;">✂ Right Division</strong>
  <p style="margin:10px 0 0;font-size:0.97rem;color:#2c2c3e;line-height:1.68;">{p['right_division']}</p>
</div>

<!-- Application -->
<div style="background:#eaf3e8;border-left:4px solid #2d6a4f;padding:16px 20px;margin:22px 0;border-radius:0 6px 6px 0;">
  <strong style="color:#2d6a4f;font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;">✦ Application</strong>
  <p style="margin:10px 0 0;font-size:0.97rem;color:#2c2c3e;line-height:1.68;">{p['application']}</p>
</div>

<!-- Labels -->
<div style="margin:20px 0;display:flex;flex-wrap:wrap;gap:6px;">{labels_str}</div>

<!-- CTA -->
<div style="text-align:center;background:linear-gradient(135deg,#0d1f3c 0%,#152a4a 100%);padding:26px 20px;border-radius:8px;margin-top:28px;">
  <p style="color:#d4af37;font-size:0.78rem;letter-spacing:3px;text-transform:uppercase;margin:0 0 14px;">Watch the Full Video</p>
  <a href="https://youtube.com/@ohhenry6524" style="display:inline-block;background:#d4af37;color:#0d1f3c;padding:12px 30px;border-radius:4px;text-decoration:none;font-weight:bold;font-size:0.95rem;font-family:Georgia,serif;">▶ @ohhenry6524 on YouTube</a>
  <p style="color:#9aa3b0;font-size:0.78rem;margin:14px 0 0;">New videos daily · 7AM · 12PM · 4PM · 8PM KST<br>
  <a href="https://henrynkoh.github.io/rightlydividingkjv/" style="color:#d4af37;text-decoration:none;">rightlydividingkjv.github.io</a></p>
</div>

</div>"""

# ─── ALL 88 POSTS ─────────────────────────────────────────────────────────────
POSTS = [
  # ══ WEEK 1 ══ Rightly Dividing: The Foundation ══════════════════════════════
  {"week":1,"day":1,"slot":1,
   "title":"2 Timothy 2:15 – What Does 'Rightly Dividing' Really Mean? | KJV",
   "labels":["Rightly Dividing","2 Timothy 2:15","KJV","Dispensational","Bible Study"],
   "verse_text":"Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth.",
   "verse_ref":"2 Timothy 2:15 KJV",
   "intro":"Why does Christianity have thousands of denominations, all reading the same Bible yet reaching different conclusions? The answer lies in one phrase — <strong>rightly dividing</strong>. God gave different instructions to different people in different ages, and confusing them produces confusion in every direction.",
   "right_division":"Rightly dividing is not about picking your favorite verses — it is about identifying <em>who</em> God is speaking to, <em>when</em>, and <em>under which covenant</em>. The Law was for Israel. The Kingdom Gospel was for Israel. The Grace Gospel through Paul is for us today, the Body of Christ.",
   "application":"Start every Bible reading session with one question: <em>Is this written to me, about me, or for me to learn from?</em> That single discipline will transform your Bible study from confusion into crystal clarity."},

  {"week":1,"day":1,"slot":2,
   "title":"Who Is the Word of Truth For? Context Is Everything | KJV Right Division",
   "labels":["Context","KJV","Who Is It For","Bible Study","Dispensational"],
   "verse_text":"All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness.",
   "verse_ref":"2 Timothy 3:16 KJV",
   "intro":"All Scripture is inspired — but not all Scripture is addressed to you. God told Noah to build an ark. That was Scripture. It was not your assignment. The same principle runs through every page of the Bible, and recognizing it is the beginning of real understanding.",
   "right_division":"The Bible contains God's word <em>to</em> Israel, <em>to</em> the Church, and <em>to</em> the nations. Right division identifies the recipient before applying the content. Peter's Pentecost sermon was for Israel. Paul's prison epistles are for the Body of Christ. Treat them accordingly.",
   "application":"Before applying any verse, ask: <em>Who received this? When? Under which dispensation?</em> This three-second habit will protect you from misapplication and flood your study with new light."},

  {"week":1,"day":1,"slot":3,
   "title":"Kingdom Gospel vs Grace Gospel – Matthew 4:23 vs 1 Corinthians 15 | KJV",
   "labels":["Gospel","Kingdom Gospel","Grace Gospel","1 Corinthians 15","KJV"],
   "verse_text":"How that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures.",
   "verse_ref":"1 Corinthians 15:3-4 KJV",
   "intro":"Jesus preached the <em>gospel of the kingdom</em> — Matthew 4:23. Paul preached the <em>gospel of the grace of God</em> — Acts 20:24. These are not the same message. Confusing them is why millions are unsure whether they are truly saved.",
   "right_division":"The Kingdom Gospel announced Israel's King had come, confirmed by miracles and signs. The Grace Gospel proclaims Christ's death, burial, and resurrection for the justification of all who believe — apart from signs, apart from works, apart from law-keeping.",
   "application":"The Gospel that saves you today is four facts: Christ <strong>died</strong> for your sins, was <strong>buried</strong>, <strong>rose</strong> the third day — all according to Scripture. Believe it. Rest in it. It is finished."},

  {"week":1,"day":1,"slot":4,
   "title":"Why So Many Denominations? The Failure to Rightly Divide | KJV",
   "labels":["Denominations","Rightly Dividing","KJV","Church","Law vs Grace"],
   "verse_text":"For Christ sent me not to baptize, but to preach the gospel: not with wisdom of words, lest the cross of Christ should be made of none effect.",
   "verse_ref":"1 Corinthians 1:17 KJV",
   "intro":"Thousands of denominations, one Bible. How? Because for centuries, believers have applied to the Church what God said to Israel, and applied to Israel what God revealed to Paul. The result is a mixture that confuses everyone and satisfies no one.",
   "right_division":"Right division is not the cause of division — it is the <em>cure</em> for it. When every believer recognizes that Paul's epistles (Romans through Philemon) are the Church's operating instructions for this age of grace, doctrinal confusion dissolves.",
   "application":"Choose one of Paul's epistles this week — Ephesians or Colossians — and read it as your direct address from God for this age. Notice how clearly it speaks when you read it as intended."},

  # ── Day 2 ──
  {"week":1,"day":2,"slot":1,
   "title":"Acts 2:38 – 'Repent and Be Baptized' – Kingdom or Grace? | KJV Right Division",
   "labels":["Acts 2:38","Water Baptism","Kingdom","Peter","KJV","Dispensational"],
   "verse_text":"Then Peter said unto them, Repent, and be baptized every one of you in the name of Jesus Christ for the remission of sins.",
   "verse_ref":"Acts 2:38 KJV",
   "intro":"Acts 2:38 is cited to demand water baptism for salvation. But right division reveals that Peter was speaking to <strong>Jewish men</strong> on the Day of Pentecost, offering the Kingdom to the nation of Israel — not addressing the Church age believer.",
   "right_division":"Compare Acts 2:38 (Peter to Israel) with Romans 10:9-10 (Paul to the Church): <em>Believe in thine heart… confess with thy mouth.</em> No water formula. Faith alone. Paul's Gospel is the operating Gospel for this age of grace.",
   "application":"Your salvation today rests on 1 Corinthians 15:1-4 and Romans 10:9-10 — faith alone in Christ alone. Water baptism is a beautiful public testimony, but it does not save in this age of grace."},

  {"week":1,"day":2,"slot":2,
   "title":"Sermon on the Mount – Kingdom Ethics, Not Church Doctrine | KJV",
   "labels":["Sermon on the Mount","Kingdom","Matthew 5","KJV","Dispensational"],
   "verse_text":"Think not that I am come to destroy the law, or the prophets: I am not come to destroy, but to fulfil.",
   "verse_ref":"Matthew 5:17 KJV",
   "intro":"The Sermon on the Mount is glorious — but it is misapplied when treated as the Church's standard of justification. Jesus delivered it as the ethics of the coming Kingdom, intensifying the Law to show Israel that no one could meet God's standard apart from grace.",
   "right_division":"Matthew 5:20 — <em>Except your righteousness shall exceed the scribes and Pharisees, ye shall in no case enter the kingdom.</em> This is Kingdom standard. For the Church: Romans 3:28 — <em>justified by faith without the deeds of the law.</em>",
   "application":"Read the Sermon on the Mount and marvel at Christ's perfection and the standard He embodies. But stand on Paul's Gospel of grace — not the Sermon's Law-intensified standard — for your righteousness before God."},

  {"week":1,"day":2,"slot":3,
   "title":"John 3:16 – The Most Loved Verse in Dispensational Context | KJV",
   "labels":["John 3:16","Grace","KJV","Dispensational","Salvation"],
   "verse_text":"For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
   "verse_ref":"John 3:16 KJV",
   "intro":"John 3:16 is the most beloved verse in Scripture — and it is absolutely, eternally true. But what did <em>believeth</em> mean when Jesus spoke it to Nicodemus before the cross, before the resurrection, before Paul's revelation of the full mystery?",
   "right_division":"The object of saving faith has always been Christ. But the full <em>content</em> of the Gospel — death, burial, resurrection — was not yet accomplished or revealed. Today we believe the completed Gospel of 1 Corinthians 15, which expands John 3:16 into its fullest expression.",
   "application":"God so loved <em>you</em>. That love is now revealed in all its fullness through the cross, the empty tomb, and the risen Christ. Believe in Him wholly, as Paul reveals Him fully."},

  {"week":1,"day":2,"slot":4,
   "title":"Hebrews – Written to Jews in Transition, Not to the Church | KJV",
   "labels":["Hebrews","Jewish","Transition","KJV","Dispensational","Warning Passages"],
   "verse_text":"God, who at sundry times and in divers manners spake in time past unto the fathers by the prophets, Hath in these last days spoken unto us by his Son.",
   "verse_ref":"Hebrews 1:1-2 KJV",
   "intro":"The book of Hebrews is addressed to — Hebrews. Jewish believers under pressure to return to the Mosaic system. Every warning in Hebrews — falling away, willful sinning, trampling the Son of God — must be read in that specific context.",
   "right_division":"Hebrews 6:4-6 and 10:26-29 are not warnings to Church age believers about losing salvation. They address Hebrew believers in the Acts transition period who were considering abandoning Christ and returning to the temple system. Context is everything.",
   "application":"Read Hebrews marveling at Christ's supremacy — better than angels, Moses, Aaron, the Levitical priesthood. But apply its warnings in their dispensational context before letting them shake your assurance in Christ."},

  # ── Day 3 ──
  {"week":1,"day":3,"slot":1,
   "title":"The Abrahamic Covenant – God's Unconditional Promise to Israel | KJV",
   "labels":["Abrahamic Covenant","Israel","Genesis 15","KJV","Dispensational"],
   "verse_text":"And I will establish my covenant between me and thee and thy seed after thee in their generations for an everlasting covenant.",
   "verse_ref":"Genesis 17:7 KJV",
   "intro":"God made an unconditional, unilateral promise to Abraham — land, seed, and blessing. In Genesis 15, God alone passed between the pieces while Abraham slept. This covenant did not depend on Abraham's performance. It depended solely on God's faithfulness.",
   "right_division":"The land promise — a specific geographic territory — has never been fully fulfilled. It awaits the Millennial Kingdom when Israel will possess the full extent of the promised land under King Jesus. God's promises to Israel are not cancelled; they are postponed.",
   "application":"The God who keeps His covenant with Abraham keeps His promises to you. If He cannot break His word to Israel, He will not break His word to you. His faithfulness is the foundation of your confidence."},

  {"week":1,"day":3,"slot":2,
   "title":"The Mosaic Covenant – Conditional Law Given at Sinai for Israel | KJV",
   "labels":["Mosaic Covenant","Law","Sinai","Israel","KJV","Dispensational"],
   "verse_text":"Now therefore, if ye will obey my voice indeed, and keep my covenant, then ye shall be a peculiar treasure unto me above all people.",
   "verse_ref":"Exodus 19:5 KJV",
   "intro":"Unlike the Abrahamic Covenant, the Mosaic Covenant was conditional — <em>if</em> ye will obey. Israel received the Law at Sinai as the terms of their national relationship with God. Obedience brought blessing; disobedience brought cursing — Deuteronomy 28.",
   "right_division":"Galatians 3:19 — the Law was <em>added</em> because of transgressions, <em>till</em> the seed should come. Two crucial words: added (not the original plan) and till (temporary by design). The Law pointed to Christ and was never intended to save.",
   "application":"The Law accomplished its purpose. Christ came. You are no longer under the schoolmaster. Stand in the grace of God through faith in Christ — free from the condemnation the Law could only announce."},

  {"week":1,"day":3,"slot":3,
   "title":"The Davidic Covenant – Israel's King and Eternal Throne | KJV",
   "labels":["Davidic Covenant","Kingdom","Messiah","2 Samuel 7","KJV"],
   "verse_text":"And thine house and thy kingdom shall be established for ever before thee: thy throne shall be established for ever.",
   "verse_ref":"2 Samuel 7:16 KJV",
   "intro":"God promised David a dynasty, a kingdom, and a throne that would last forever. This Davidic Covenant is the foundation of the Messianic hope — the coming King from the line of David who would reign on David's literal throne forever.",
   "right_division":"Jesus is that King — Matthew 1:1, Luke 1:32. But Israel rejected Him at His first coming. The Kingdom was not established then. It remains for the Second Coming — Revelation 20 — when He will literally reign from Jerusalem on David's throne for one thousand years.",
   "application":"The Davidic Covenant guarantees a literal future Kingdom. For us, our citizenship is heavenly — Philippians 3:20. But we rejoice that Israel's King is coming, and we will reign with Him — Revelation 20:6."},

  {"week":1,"day":3,"slot":4,
   "title":"The New Covenant – For Israel or the Church? | Jeremiah 31 KJV",
   "labels":["New Covenant","Israel","Jeremiah 31","KJV","Dispensational"],
   "verse_text":"Behold, the days come, saith the LORD, that I will make a new covenant with the house of Israel, and with the house of Judah.",
   "verse_ref":"Jeremiah 31:31 KJV",
   "intro":"Jeremiah 31 is explicit — the New Covenant was promised to the house of Israel and the house of Judah. Not Gentiles, not the Church. Right division shows this is Israel's national covenant, to be fully fulfilled in the Millennial Kingdom.",
   "right_division":"The Church participates in the blessings of the New Covenant — we have the Spirit, we have forgiveness. But our specific covenant reality is the mystery revealed through Paul: the Body of Christ, equally Jew and Gentile, with heavenly blessings in Christ.",
   "application":"God will fulfill the New Covenant with Israel in completeness. He will fulfill every promise to you as well. The God who cannot lie stands behind every word He has spoken — to Israel and to you."},

  # ── Day 4 ──
  {"week":1,"day":4,"slot":1,
   "title":"Paul's 'My Gospel' – Revelation, Not Tradition | Romans 16:25 KJV",
   "labels":["Paul","My Gospel","Romans 16:25","Mystery","KJV","Dispensational"],
   "verse_text":"Now to him that is of power to stablish you according to my gospel, and the preaching of Jesus Christ, according to the revelation of the mystery, which was kept secret since the world began.",
   "verse_ref":"Romans 16:25 KJV",
   "intro":"Paul calls it <em>my gospel</em> — Romans 2:16, 16:25. Not because he invented it, but because God gave it to him directly by revelation — Galatians 1:11-12. No other apostle preached the mystery of the Body of Christ as Paul did.",
   "right_division":"Peter preached the Kingdom Gospel to Israel. Paul preached the Grace Gospel to the world. Both are true, both are of God — but they are distinct in content, audience, and application. Paul's gospel is the Gospel for this Church age.",
   "application":"You are saved by Paul's Gospel — 1 Corinthians 15:1-4. No additions, no conditions. The death, burial, and resurrection of Christ, received by faith. That is your complete and eternal salvation."},

  {"week":1,"day":4,"slot":2,
   "title":"Romans 3:28 – Justified by Faith Without the Deeds of the Law | KJV",
   "labels":["Romans 3:28","Justification","Faith","KJV","Grace","Law vs Grace"],
   "verse_text":"Therefore we conclude that a man is justified by faith without the deeds of the law.",
   "verse_ref":"Romans 3:28 KJV",
   "intro":"<em>Without the deeds of the law.</em> Paul could not be clearer. Justification — being declared righteous before God — comes through faith alone, not through works, not through law-keeping, not through sacraments, not through religious performance.",
   "right_division":"Abraham believed God and it was counted to him for righteousness — Romans 4:3 — before circumcision, before the Law, before any religious act. Faith has always been the instrument of justification. The Law only reveals what faith receives.",
   "application":"You are justified by faith alone in Christ alone. Not faith plus baptism. Not faith plus obedience. Faith alone. Martin Luther rediscovered this in 1517. Paul wrote it in AD 57. Stand in that freedom today."},

  {"week":1,"day":4,"slot":3,
   "title":"Ephesians 2:8-9 – Grace Through Faith, Not of Works | KJV",
   "labels":["Ephesians 2:8-9","Grace","Faith","Works","KJV","Salvation"],
   "verse_text":"For by grace are ye saved through faith; and that not of yourselves: it is the gift of God: Not of works, lest any man should boast.",
   "verse_ref":"Ephesians 2:8-9 KJV",
   "intro":"Three declarations that secure your salvation. First — by <strong>grace</strong>: God's unearned, undeserved favor. Second — through <strong>faith</strong>: the hand that receives what grace provides. Third — <strong>not of works</strong>: human effort is explicitly excluded from the equation of salvation.",
   "right_division":"<em>Lest any man should boast.</em> If salvation involved any human effort, someone could boast. God eliminates boasting by making salvation wholly of grace, wholly received by faith. Verse 10 shows works are the <em>result</em> of salvation — not the cause.",
   "application":"You cannot earn it. You cannot add to it. You can only receive it. Receive it now — fully, freely, finally. That is the beauty of grace that Paul reveals to the Body of Christ."},

  {"week":1,"day":4,"slot":4,
   "title":"Galatians 2:16 – Not Justified by the Works of the Law | KJV",
   "labels":["Galatians 2:16","Justification","Law","Faith","KJV","Grace"],
   "verse_text":"Knowing that a man is not justified by the works of the law, but by the faith of Jesus Christ.",
   "verse_ref":"Galatians 2:16 KJV",
   "intro":"Paul says it three times in one verse — <em>not by the works of the law.</em> No flesh. Never. The repetition is deliberate. The Galatians were being told to add Law-keeping to faith. Paul calls this another gospel — Galatians 1:8-9 — and pronounces a curse on those who preach it.",
   "right_division":"The faith of Jesus Christ — His perfect obedience, His death, His resurrection — is the basis of our justification. We bring our faith to receive what His faithfulness accomplished. The Law can never justify because no one keeps it perfectly.",
   "application":"Any gospel that adds works to faith is a false gospel — no matter how sincere the preacher. Galatians 2:16 is your protection. Stand in it firmly. Grace alone, faith alone, Christ alone."},

  # ── Day 5 ──
  {"week":1,"day":5,"slot":1,
   "title":"Acts – A Transition Book, Not the Church's Rulebook | KJV Right Division",
   "labels":["Acts","Transition","KJV","Dispensational","Church Age"],
   "verse_text":"And he said unto them, It is not for you to know the times or the seasons, which the Father hath put in his own power.",
   "verse_ref":"Acts 1:7 KJV",
   "intro":"The book of Acts records a transition — from Israel's Kingdom program to the mystery of the Body of Christ through Paul. It is not a normative pattern for the Church age. Taking Acts as the Church's manual leads to chasing sign gifts and demanding tongues as evidence of the Spirit.",
   "right_division":"Read Acts for history and inspiration. Live by Paul's epistles — Romans through Philemon — for doctrine and practice. The transition in Acts is descriptive of what happened; Paul's letters are prescriptive of what we believe and how we live.",
   "application":"Your Christian life is not modeled on Acts 2 — it is modeled on Ephesians, Philippians, and Colossians. Paul is your apostle. His epistles are your operating instructions. Live accordingly."},

  {"week":1,"day":5,"slot":2,
   "title":"Peter vs Paul – Two Apostles, Two Distinct Programs | Galatians 2:7 KJV",
   "labels":["Peter","Paul","Two Programs","Galatians 2:7","KJV","Dispensational"],
   "verse_text":"But contrariwise, when they saw that the gospel of the uncircumcision was committed unto me, as the gospel of the circumcision was unto Peter.",
   "verse_ref":"Galatians 2:7 KJV",
   "intro":"God gave Peter the Gospel of the circumcision — to Israel. God gave Paul the Gospel of the uncircumcision — to Gentiles. Two apostles, two distinct commissions, operating simultaneously during the Acts transition period. This is not contradiction — it is dispensational design.",
   "right_division":"Peter: Jerusalem, Kingdom offer to Israel, signs and wonders, water baptism for remission. Paul: Antioch and beyond, the mystery of the Body of Christ, Grace Gospel, Spirit baptism. Confusing their ministries produces theological confusion in every direction.",
   "application":"For this age of grace, follow Paul as he followed Christ — 1 Corinthians 11:1. His 13 epistles are your direct instruction from God for life in the Body of Christ. Read them as addressed to you — because they are."},

  {"week":1,"day":5,"slot":3,
   "title":"Acts 9 – Paul's Conversion: The Birth of a New Dispensation | KJV",
   "labels":["Acts 9","Paul","Conversion","Dispensation","KJV","Grace"],
   "verse_text":"And he said, Who art thou, Lord? And the Lord said, I am Jesus whom thou persecutest: it is hard for thee to kick against the pricks.",
   "verse_ref":"Acts 9:5 KJV",
   "intro":"The conversion of Saul of Tarsus on the Damascus road was not just the salvation of one man — it was the beginning of a new dispensational program. God chose Paul as the pattern — 1 Timothy 1:16 — the first full recipient of grace expressed in all its mystery.",
   "right_division":"Before Paul, salvation was anticipated. After Paul, salvation is proclaimed in its fullness — the cross accomplished, the resurrection declared, the mystery revealed. Paul says he was shown mercy so that in him first, Jesus might display all longsuffering as a pattern for all who would believe.",
   "application":"Your salvation follows Paul's pattern — undeserved, unexpected, by grace alone. You are a trophy of Christ's longsuffering love, displayed before the watching universe as evidence of what grace can do."},

  {"week":1,"day":5,"slot":4,
   "title":"1 Corinthians 15:1-4 – The Gospel That Saves You Today | KJV",
   "labels":["1 Corinthians 15","Gospel","Salvation","KJV","Grace","Paul"],
   "verse_text":"How that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures.",
   "verse_ref":"1 Corinthians 15:3-4 KJV",
   "intro":"Here is the Gospel — concise, clear, complete. Four facts: Christ <strong>died</strong>. For our <strong>sins</strong>. He was <strong>buried</strong>. He <strong>rose</strong> the third day. All according to the Scriptures. This is what Paul received by revelation and delivered to the Corinthians — and to us.",
   "right_division":"Notice what is absent from the Gospel definition: no water baptism, no law-keeping, no tongues, no sacraments. Just the death, burial, and resurrection of Christ — received by faith. This is the Grace Gospel for the Church age.",
   "application":"The Gospel is four facts and one response — faith. Have you believed this Gospel? That is all that is required. If you have, your salvation is as certain as the historical resurrection of Jesus Christ."},

  # ── Day 6 ──
  {"week":1,"day":6,"slot":1,
   "title":"Dispensations – God's Different Administrations Through History | Ephesians 1:10 KJV",
   "labels":["Dispensations","Ephesians 1:10","KJV","Dispensational","Grace Age"],
   "verse_text":"That in the dispensation of the fulness of times he might gather together in one all things in Christ, both which are in heaven, and which are on earth.",
   "verse_ref":"Ephesians 1:10 KJV",
   "intro":"Dispensation — the Greek <em>oikonomia</em> — means a stewardship or administration. God has administered His relationship with mankind differently in different ages: Innocence, Conscience, Human Government, Promise, Law, Grace, Kingdom. Each has its own rules and revelation.",
   "right_division":"We live in the dispensation of Grace — the most favorable period in all of human history to be alive as a believer. No sacrifices, no temple, no priestly intermediary. Direct access to God through Christ by the indwelling Spirit. Recognize the privilege of your age.",
   "application":"Knowing your dispensation clarifies everything. You are not Abraham waiting for a promise, or Israel under the Law, or a Tribulation saint enduring to the end. You are a member of the Body of Christ in the age of grace. Live like it."},

  {"week":1,"day":6,"slot":2,
   "title":"The Mystery Hidden Since the World Began | Colossians 1:26 KJV",
   "labels":["Mystery","Colossians 1:26","KJV","Body of Christ","Dispensational","Paul"],
   "verse_text":"Even the mystery which hath been hid from ages and from generations, but now is made manifest to his saints.",
   "verse_ref":"Colossians 1:26 KJV",
   "intro":"Something was completely hidden until Paul — not hinted at, not foreshadowed, but <em>hidden</em>. The mystery of the Body of Christ: that Jew and Gentile would become one equal body in Christ, with heavenly blessings, during this age of grace between Israel's two national dealings with God.",
   "right_division":"Isaiah 53 prophesied the suffering Servant. Zechariah 14 prophesied the returning King. But the parenthesis between — the Church age — was sealed until God revealed it through Paul. This is why the Gospels and Acts do not fully teach Church truth. Paul is uniquely your teacher.",
   "application":"You are living in the age that Old Testament prophets longed to understand — 1 Peter 1:10-12. They searched diligently for what you hold in your hands. Treasure this mystery. Study it. Live it."},

  {"week":1,"day":6,"slot":3,
   "title":"One New Man in Christ – Ephesians 2:15 | KJV Right Division",
   "labels":["One New Man","Ephesians 2:15","Body of Christ","KJV","Dispensational"],
   "verse_text":"For to make in himself of twain one new man, so making peace.",
   "verse_ref":"Ephesians 2:15 KJV",
   "intro":"The mystery produced something entirely new — <em>one new man</em>. Not Jew, not Gentile, but a third entity: the Body of Christ. All previous distinctions are swallowed up in Christ. Galatians 3:28 — neither Jew nor Greek, bond nor free, male nor female — all one in Christ Jesus.",
   "right_division":"This new man has a new standing (in Christ), a new position (seated in heavenly places), a new calling (heavenly, not earthly), a new apostle (Paul), and new Scripture (the prison epistles). This is your identity — not Israel, not a Gentile, but the one new man.",
   "application":"You are a new creation — 2 Corinthians 5:17. Old distinctions do not define you. Christ defines you. You are in Him, and He is in you. Live from that identity of radical newness today."},

  {"week":1,"day":6,"slot":4,
   "title":"Sealed by the Holy Spirit – Ephesians 1:13 | KJV Right Division",
   "labels":["Sealed","Holy Spirit","Ephesians 1:13","KJV","Security","Grace"],
   "verse_text":"In whom ye also trusted, after that ye heard the word of truth, the gospel of your salvation: in whom also after that ye believed, ye were sealed with that holy Spirit of promise.",
   "verse_ref":"Ephesians 1:13 KJV",
   "intro":"At the moment of salvation, the Holy Spirit seals every believer. Immediately. Permanently. Unconditionally. You were sealed when you <em>believed</em> — not when you became good enough, not when you were baptized, not when you spoke in tongues.",
   "right_division":"A seal in the ancient world indicated ownership, authenticity, and security. God's seal on you declares: <em>this one is Mine, this one is genuine, this one is secure.</em> Romans 8:38-39 — nothing can separate you from the love of God in Christ Jesus.",
   "application":"You are sealed. Permanently. Unconditionally. The Holy Spirit Himself is God's guarantee that you belong to Him. Rest in the security of that seal today — especially if doubt has been knocking at your door."},

  # ── Day 7 ──
  {"week":1,"day":7,"slot":1,
   "title":"Seated in Heavenly Places – Ephesians 2:6 | KJV Right Division",
   "labels":["Heavenly Places","Ephesians 2:6","Position","KJV","Grace","Identity"],
   "verse_text":"And hath raised us up together, and made us sit together in heavenly places in Christ Jesus.",
   "verse_ref":"Ephesians 2:6 KJV",
   "intro":"Past tense — <em>hath raised us up, made us sit.</em> This is your present reality. Not a future hope, not a goal to achieve — a present position. You are, right now, seated with Christ in heavenly places. In God's sight, your position is as secure as Christ's own position at the Father's right hand.",
   "right_division":"Israel's hope is earthly — land, throne, Jerusalem. The Church's position is heavenly — blessings in heavenly places (Ephesians 1:3), citizenship in heaven (Philippians 3:20), life hidden with Christ in God (Colossians 3:3). This is the dispensational distinction of the Body of Christ.",
   "application":"You are not striving to get to heaven — you are already positioned there in Christ. Live today from a heavenly position rather than an earthly perspective. Let your seated position determine how you face your standing circumstances."},

  {"week":1,"day":7,"slot":2,
   "title":"Complete in Christ – Colossians 2:10 | KJV Right Division",
   "labels":["Complete","Colossians 2:10","KJV","Identity","Grace","Body of Christ"],
   "verse_text":"And ye are complete in him, which is the head of all principality and power.",
   "verse_ref":"Colossians 2:10 KJV",
   "intro":"Complete. Not partially complete. Not complete-when-you-mature. <strong>Complete now</strong>. In Him. Every spiritual blessing is already yours — Ephesians 1:3. Every need is met in Christ — Philippians 4:19. You lack nothing in your standing before God because you are in Christ, and Christ is complete.",
   "right_division":"The Colossians were told they needed additional experiences, angel worship, philosophy, dietary laws to be complete. Paul's answer cuts through it all: <em>ye are complete in Him.</em> Nothing can be added to what Christ has already made you. This is the mystery in full expression.",
   "application":"Stop striving for spiritual completeness through religious effort. You are already complete in Christ. Walk in that completeness today. Let it silence the voices that say you need more, do more, be more."},

  {"week":1,"day":7,"slot":3,
   "title":"Reconciled to God – 2 Corinthians 5:18-19 | KJV Right Division",
   "labels":["Reconciliation","2 Corinthians 5","KJV","Gospel","Ambassador","Grace"],
   "verse_text":"God was in Christ, reconciling the world unto himself, not imputing their trespasses unto them; and hath committed unto us the word of reconciliation.",
   "verse_ref":"2 Corinthians 5:19 KJV",
   "intro":"<em>Not imputing their trespasses unto them.</em> God is not counting sins against the world — that account was settled at the cross. Christ bore every sin. The sin question has been answered. The only question remaining is whether a person will receive the reconciliation God has already accomplished.",
   "right_division":"The ministry of reconciliation — verse 18 — is now ours. We are ambassadors of Christ — verse 20 — pleading with the world: <em>be ye reconciled to God.</em> Not <em>earn your way</em> but <em>be reconciled.</em> The work is done. Receive it.",
   "application":"You are God's ambassador. Your message is reconciliation — free, full, finished in Christ. Share it with someone today. You carry the most important message in the world."},

  {"week":1,"day":7,"slot":4,
   "title":"Week 1 Summary – The Foundation Is Set | 2 Timothy 2:15 KJV",
   "labels":["Summary","Week 1","Rightly Dividing","KJV","Dispensational","Foundation"],
   "verse_text":"Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth.",
   "verse_ref":"2 Timothy 2:15 KJV",
   "intro":"This week we laid the foundation. Rightly dividing clarifies who God is speaking to, when, and under which covenant. We distinguished Kingdom from Grace, Peter from Paul, Law from Grace, and Israel from the Church. The result: clarity where confusion once reigned.",
   "right_division":"You now know who you are — a member of the Body of Christ, sealed by the Spirit, seated in heavenly places, complete in Him, reconciled to God, an ambassador of grace. This is your identity in the age of grace. No confusion required.",
   "application":"Take one principle from Week 1 and share it with someone this week. The truth of rightly dividing sets people free. Be a faithful workman — approved, unashamed, accurate."},

  # ══ WEEK 2 ══ Law vs Grace / Moses vs Paul ═══════════════════════════════════
  {"week":2,"day":8,"slot":1,
   "title":"The Ten Commandments – For Israel or Everyone? | Exodus 20 KJV Right Division",
   "labels":["Ten Commandments","Exodus 20","Israel","Law","KJV","Dispensational"],
   "verse_text":"I am the LORD thy God, which have brought thee out of the land of Egypt, out of the house of bondage.",
   "verse_ref":"Exodus 20:2 KJV",
   "intro":"Before God gave even one commandment, He identified His audience: the nation He had just delivered from Egypt. The Ten Commandments opened with Israel's national identity. Deuteronomy 5:3 confirms — <em>The LORD made not this covenant with our fathers, but with us.</em>",
   "right_division":"The moral principles in the Commandments reflect God's holy character — always valuable. But as a legal covenant for justification, the Mosaic Law was given to Israel, not the Gentile Church. Galatians 3:17 — the Law came 430 years after Abraham's promise and cannot disannul grace.",
   "application":"You live in the age of grace — Romans 3:28: <em>justified by faith without the deeds of the law.</em> Let the Commandments show you God's holiness. Let the cross show you His grace. Rest in the finished work."},

  {"week":2,"day":8,"slot":2,
   "title":"Why Was the Law Given? – Galatians 3:19 KJV Explained",
   "labels":["Galatians 3:19","Purpose of Law","KJV","Grace","Dispensational","Schoolmaster"],
   "verse_text":"Wherefore then serveth the law? It was added because of transgressions, till the seed should come to whom the promise was made.",
   "verse_ref":"Galatians 3:19 KJV",
   "intro":"Two words unlock this verse: <em>added</em> and <em>till</em>. The Law was not the eternal plan — it was added, temporary, purposeful. It served until the seed — Christ — should come. When Christ came, the Law's role as a path to righteousness ended.",
   "right_division":"Three purposes of the Law: (1) Expose transgression — Romans 3:20. (2) Serve as a schoolmaster bringing us to Christ — Galatians 3:24. (3) Demonstrate that no flesh can be justified by works. All three purposes are fulfilled in Christ.",
   "application":"The Law was never meant to save you — it was meant to show you that you needed a Saviour. Christ is that Saviour. You have arrived at the destination the Law was pointing toward. Stay there."},

  {"week":2,"day":8,"slot":3,
   "title":"Romans 6:14 – Not Under Law but Under Grace | KJV Right Division",
   "labels":["Romans 6:14","Law vs Grace","KJV","Grace","Holiness","Dispensational"],
   "verse_text":"For sin shall not have dominion over you: for ye are not under the law, but under grace.",
   "verse_ref":"Romans 6:14 KJV",
   "intro":"Two powerful truths in one verse: <em>sin shall not have dominion</em>, and <em>ye are not under the law but under grace.</em> These are directly connected. Sin has dominion under Law — because Law cannot empower obedience, only expose failure. Grace changes the power dynamic entirely.",
   "right_division":"The Law says <em>do this and live</em>. Grace says <em>it is done — now live.</em> The motivation shifts from fear of condemnation to love for the One who freely justified you. Grace is not the enemy of holiness — it is the only force powerful enough to actually produce it.",
   "application":"You are under grace, not law. Let that truth motivate holy living — not from fear of punishment, but from love for the God who, while you were yet a sinner, Christ died for you — Romans 5:8."},

  {"week":2,"day":8,"slot":4,
   "title":"Galatians 3:10 – The Curse of the Law and How Christ Removed It | KJV",
   "labels":["Galatians 3:10","Curse of the Law","KJV","Redemption","Grace","Cross"],
   "verse_text":"For as many as are of the works of the law are under the curse: for it is written, Cursed is every one that continueth not in all things which are written in the book of the law to do them.",
   "verse_ref":"Galatians 3:10 KJV",
   "intro":"The Law demands perfection — <em>all things</em>. Not most things. Not sincere effort. All things. Anyone seeking justification through law-keeping is under a curse — because James 2:10 confirms: offend in one point and you are guilty of all.",
   "right_division":"Christ redeemed us from the curse of the Law — Galatians 3:13 — by becoming a curse for us. He absorbed every demand of the Law at the cross. For those in Christ, Romans 8:1 declares: <em>there is now no condemnation.</em> The curse is fully, finally lifted.",
   "application":"The curse of the Law was borne by Christ so you would never bear it. Walk in freedom today. And if you meet someone crushed under religious guilt, tell them: the curse has been lifted. Christ bore it. Believe it."},

  # ── Day 9 ──
  {"week":2,"day":9,"slot":1,
   "title":"Romans 7 – The Believer's Struggle When Living Under Law | KJV",
   "labels":["Romans 7","Law","Struggle","KJV","Grace","Holy Spirit"],
   "verse_text":"O wretched man that I am! who shall deliver me from the body of this death? I thank God through Jesus Christ our Lord.",
   "verse_ref":"Romans 7:24-25 KJV",
   "intro":"Romans 7 describes the agony of trying to live the Christian life through Law-keeping and self-effort. The more you try not to covet, the more you covet. Sin takes occasion through the very commandment meant to stop it. This is the Law-based Christian experience — and it leads to wretchedness.",
   "right_division":"The answer is Romans 8 — life in the Spirit. The Law of the Spirit of life in Christ Jesus sets free from the law of sin and death — Romans 8:2. Grace does not just pardon; it empowers. What Law could never accomplish, the Spirit achieves.",
   "application":"If Romans 7 sounds like your daily experience, move to Romans 8. Walk in the Spirit — Galatians 5:16 — and you will not fulfill the lust of the flesh. The guarantee is God's, not yours."},

  {"week":2,"day":9,"slot":2,
   "title":"Romans 8:1 – There Is Now NO Condemnation in Christ | KJV Right Division",
   "labels":["Romans 8:1","No Condemnation","KJV","Grace","Security","Christ"],
   "verse_text":"There is therefore now no condemnation to them which are in Christ Jesus.",
   "verse_ref":"Romans 8:1 KJV",
   "intro":"<em>No condemnation.</em> Not <em>less</em> condemnation. Not condemnation only when you sin badly. <strong>No condemnation.</strong> This is the standing of every believer in Christ Jesus — declared by the God who cannot lie, secured by the work of His Son.",
   "right_division":"Under the Law, blessing depended on obedience. Disobedience meant curse. Relationship with God was conditional on performance. Under grace, your standing does not fluctuate with your performance — it is fixed in Christ. God sees you in His Son.",
   "application":"You are not condemned today. Not for yesterday's failure, not for today's weakness. If you are in Christ, God's verdict over your life is <em>no condemnation</em>. Let that verdict shape how you start this day."},

  {"week":2,"day":9,"slot":3,
   "title":"Colossians 2:14 – The Debt Nailed to the Cross | KJV Right Division",
   "labels":["Colossians 2:14","Cross","Debt Cancelled","KJV","Grace","Law"],
   "verse_text":"Blotting out the handwriting of ordinances that was against us, which was contrary to us, and took it out of the way, nailing it to his cross.",
   "verse_ref":"Colossians 2:14 KJV",
   "intro":"The handwriting of ordinances — the written record of every Law you failed to keep — was a certificate of debt against you. Every commandment broken added to the record. Christ took that entire certificate, nailed it to His cross, and cancelled it completely. <strong>The debt is paid.</strong>",
   "right_division":"This is why Colossians 2:16 follows immediately: <em>Let no man judge you in meat, drink, holyday, new moon, or sabbath days.</em> These ordinances no longer hold legal claim over you. They were nailed with Christ. The record is cleared.",
   "application":"No law, no ordinance, no religious calendar holds any debt over you. Christ cancelled the certificate. Live in that freedom — not to indulge, but to serve God freely from a heart of gratitude rather than a ledger of fear."},

  {"week":2,"day":9,"slot":4,
   "title":"The Sabbath – Shadow or Substance? Colossians 2:16-17 KJV",
   "labels":["Sabbath","Colossians 2:16","Shadow","KJV","Grace","Dispensational"],
   "verse_text":"Which are a shadow of things to come; but the body is of Christ.",
   "verse_ref":"Colossians 2:17 KJV",
   "intro":"The Sabbath was a shadow. The substance — the reality casting the shadow — is Christ. Israel observed the Sabbath as a covenant sign — Exodus 31:17 — between God and Israel specifically. No Gentile nation was ever commanded to observe the Sabbath as a covenant obligation.",
   "right_division":"In Christ, we have entered the true Sabbath rest — Hebrews 4:9-10. Not a day of the week but a rest of faith: <em>he that is entered into his rest hath ceased from his own works.</em> Every day is Sabbath when you rest in Christ's finished work.",
   "application":"You are not obligated to observe a Sabbath day. But you are invited to rest in Christ every moment — the true Sabbath rest of completed salvation. Stop working for what has already been freely given."},

  # ── Day 10 ──
  {"week":2,"day":10,"slot":1,
   "title":"Tithing – Mosaic Law or Grace Principle? | 2 Corinthians 9:7 KJV",
   "labels":["Tithing","Giving","2 Corinthians 9:7","KJV","Grace","Law vs Grace"],
   "verse_text":"Every man according as he purposeth in his heart, so let him give; not grudgingly, or of necessity: for God loveth a cheerful giver.",
   "verse_ref":"2 Corinthians 9:7 KJV",
   "intro":"Tithing — giving exactly 10% — was part of the Mosaic system. Israel actually paid multiple tithes annually totaling far more than 10%. This was a covenant obligation, not a freewill offering. Malachi 3:10 was written to Israel under the Law covenant — not to the Church.",
   "right_division":"For the Church in the grace age, the principle is radically generous: not 10% but everything belongs to God. Paul teaches cheerful, purposeful, Spirit-led giving — not legal obligation. Second Corinthians 8-9 describes giving that flows from grace received.",
   "application":"Give generously. Give cheerfully. Give as God has prospered you — not out of obligation to a law, but out of love for the God who gave His own Son for you. Grace always exceeds law in generosity."},

  {"week":2,"day":10,"slot":2,
   "title":"Dietary Laws – Clean and Unclean Foods Set Aside | Acts 10:15 KJV",
   "labels":["Dietary Laws","Clean Unclean","Acts 10:15","KJV","Dispensational","Freedom"],
   "verse_text":"And the voice spake unto him again the second time, What God hath cleansed, that call not thou common.",
   "verse_ref":"Acts 10:15 KJV",
   "intro":"God gave Israel dietary laws in Leviticus 11 — clean and unclean foods — as part of the Mosaic covenant that distinguished Israel from the nations. These served a dispensational purpose. In Acts 10, God showed Peter unclean animals and commanded him to eat.",
   "right_division":"The primary lesson was about Gentiles being received — verse 28. But it also signals the end of food law distinctions. 1 Timothy 4:4-5 — <em>every creature of God is good, and nothing to be refused, if it be received with thanksgiving.</em>",
   "application":"You are free from dietary laws. Eat with thanksgiving. Honor God with your body through wise choices — but not by imposing Levitical food categories that have been graciously set aside in this age of grace."},

  {"week":2,"day":10,"slot":3,
   "title":"Circumcision – Sign of the Covenant or Set Aside? | Galatians 5:6 KJV",
   "labels":["Circumcision","Galatians 5:6","KJV","Grace","Faith","Dispensational"],
   "verse_text":"For in Jesus Christ neither circumcision availeth any thing, nor uncircumcision; but faith which worketh by love.",
   "verse_ref":"Galatians 5:6 KJV",
   "intro":"Circumcision was the sign of Israel's covenant — Genesis 17:11. Jewish believers in Acts 15 insisted Gentiles must be circumcised to be saved. Paul calls this false gospel and opposes it throughout Galatians with an urgency that matches the stakes.",
   "right_division":"In Christ, circumcision means nothing and uncircumcision means nothing — what matters is <em>faith working by love.</em> Romans 2:28-29 — true circumcision is inward, spiritual, by grace. The reality is in the heart, not the flesh.",
   "application":"You are not required to observe any outward sign of the Old Covenant. Your sign is the indwelling Spirit — 2 Corinthians 1:22. Trust the inward reality over outward ritual every time."},

  {"week":2,"day":10,"slot":4,
   "title":"Acts 15 – The Jerusalem Council Settles Law vs Grace | KJV",
   "labels":["Acts 15","Jerusalem Council","Law vs Grace","KJV","Grace","Dispensational"],
   "verse_text":"But we believe that through the grace of the Lord Jesus Christ we shall be saved, even as they.",
   "verse_ref":"Acts 15:11 KJV",
   "intro":"Acts 15 convened to settle the defining question: must Gentile believers keep the Mosaic Law for salvation? Peter stood and declared — <em>we are saved through the grace of the Lord Jesus Christ, even as they.</em> No distinction. No Law addition. Grace won.",
   "right_division":"The Council's decision — Acts 15:19-20 — imposed only minimal practical restrictions for Jewish-Gentile fellowship. The Law as a means of salvation was decisively and permanently rejected at Jerusalem. Paul then settles it eternally in his epistles.",
   "application":"Grace won at Jerusalem in AD 50. Grace wins today. Anytime someone adds a law-condition to salvation, Acts 15 and Galatians answer: <em>grace alone, faith alone, Christ alone.</em>"},

  # ── Day 11 ──
  {"week":2,"day":11,"slot":1,
   "title":"Moses the Lawgiver vs Paul the Grace Apostle | John 1:17 KJV",
   "labels":["Moses","Paul","Law vs Grace","John 1:17","KJV","Dispensational"],
   "verse_text":"For the law was given by Moses, but grace and truth came by Jesus Christ.",
   "verse_ref":"John 1:17 KJV",
   "intro":"John 1:17 sets Law and Grace in contrast — not contradiction, but contrast. Moses faithfully delivered the Law God gave him. But the Law could only show the standard; it could not provide the righteousness. Grace and truth came through Jesus Christ — the full provision of what the Law demanded.",
   "right_division":"Moses wore a veil so Israel would not see the glory fading — 2 Corinthians 3:13. Law is a fading glory. Grace is an abiding glory. Paul writes that the ministry of the Spirit <em>excels in glory</em> — verse 8. We behold God's glory with unveiled faces.",
   "application":"You live in the unveiled glory of grace, not the veiled glory of Law. Let the full light of God's grace in Christ shine on you — unobstructed, unclouded, face to face. This is your privilege in the age of grace."},

  {"week":2,"day":11,"slot":2,
   "title":"Ministry of Condemnation vs Ministry of Righteousness | 2 Corinthians 3 KJV",
   "labels":["2 Corinthians 3","Ministry","Condemnation","Righteousness","KJV","Grace"],
   "verse_text":"For if the ministration of condemnation be glory, much more doth the ministration of righteousness exceed in glory.",
   "verse_ref":"2 Corinthians 3:9 KJV",
   "intro":"Paul calls the Law <em>the ministration of condemnation</em> and <em>the ministration of death.</em> Not because the Law is evil — it is holy and just and good — Romans 7:12 — but because it condemns all who fall short. Applied to sinners, the Law produces death.",
   "right_division":"The Gospel — the ministration of righteousness — exceeds the Law in glory beyond comparison. The Law wrote on stone; the Spirit writes on hearts. The Law was temporary; the Spirit's ministry is permanent. Law produced fear; grace produces transformation from the inside out.",
   "application":"You serve in the ministry of righteousness — sharing news that exceeds every earthly announcement. Share the Gospel of grace this week and watch God transform a life through the most glorious ministry in history."},

  {"week":2,"day":11,"slot":3,
   "title":"Imputed Righteousness – God Credits You with Christ's Perfection | Romans 4:5 KJV",
   "labels":["Imputed Righteousness","Romans 4:5","KJV","Grace","Faith","Justification"],
   "verse_text":"But to him that worketh not, but believeth on him that justifieth the ungodly, his faith is counted for righteousness.",
   "verse_ref":"Romans 4:5 KJV",
   "intro":"Imputation — God counts, credits, reckons righteousness to your account. Not because you earned it. Not because you deserve it. Because you <em>believed</em>. Abraham believed God and it was counted for righteousness — Romans 4:3 — before any religious act. Faith alone.",
   "right_division":"The righteousness imputed is not your own — Philippians 3:9 — <em>not having mine own righteousness, which is of the law, but that which is through the faith of Christ.</em> Christ's perfect righteousness becomes your standing before God. His record replaces yours.",
   "application":"God sees you clothed in Christ's righteousness — perfect, complete, accepted. Stand before God today not in your own record but in His. That is imputation. That is grace. That is your permanent standing."},

  {"week":2,"day":11,"slot":4,
   "title":"Grace Reigns Through Righteousness – Romans 5:21 | KJV",
   "labels":["Romans 5:21","Grace Reigns","KJV","Righteousness","Eternal Life","Grace"],
   "verse_text":"That as sin hath reigned unto death, even so might grace reign through righteousness unto eternal life by Jesus Christ our Lord.",
   "verse_ref":"Romans 5:21 KJV",
   "intro":"Sin once reigned — as a tyrant, producing death everywhere it touched. But grace now reigns — as a sovereign, producing eternal life through righteousness. Grace reigns <em>through</em> righteousness — not despite it. Grace meets God's standard fully in Christ.",
   "right_division":"Romans 5:20 — <em>where sin abounded, grace did much more abound.</em> Grace does not merely equal sin's power — it <em>superabounds</em>. No matter how dark the history, grace is more powerful, more abundant, more triumphant than any sin ever committed.",
   "application":"Grace reigns in your life today. Not sin. Not the Law. <strong>Grace reigns</strong> — unto eternal life, through the righteousness of Jesus Christ. Live under that sovereign reign. Let grace be king in your experience."},

  # ── Day 12 ──
  {"week":2,"day":12,"slot":1,
   "title":"Dead to the Law – Married to the Risen Christ | Romans 7:4 KJV",
   "labels":["Romans 7:4","Dead to Law","KJV","Grace","Marriage","Christ"],
   "verse_text":"Wherefore, my brethren, ye also are become dead to the law by the body of Christ; that ye should be married to another, even to him who is raised from the dead.",
   "verse_ref":"Romans 7:4 KJV",
   "intro":"Death breaks the Law's hold. A widow is freed from the law of her husband by his death. Paul applies the same principle: we died with Christ — Galatians 2:20 — and that death severed our legal relationship to the Law. We are no longer married to the Law. We are married to the risen Christ.",
   "right_division":"The purpose of this new marriage: <em>that we should bring forth fruit unto God.</em> Not the fruit of legal compliance under threat of condemnation, but the fruit of a loving relationship with the risen Christ. The Spirit produces this fruit naturally — Galatians 5:22-23.",
   "application":"You are not married to the Law. You are united to the risen Christ. Let that relationship produce fruit in your life — naturally, freely, joyfully, without striving. A bride does not strive to please — she loves."},

  {"week":2,"day":12,"slot":2,
   "title":"Christ – The End of the Law for Righteousness | Romans 10:4 KJV",
   "labels":["Romans 10:4","End of Law","KJV","Righteousness","Christ","Faith"],
   "verse_text":"For Christ is the end of the law for righteousness to every one that believeth.",
   "verse_ref":"Romans 10:4 KJV",
   "intro":"<em>End</em> — the Greek <em>telos</em> — means goal, completion, terminus. Christ is the goal the Law was always pointing toward, and He is the terminus where the Law's role as a path to righteousness ends. Once you arrive at Christ, you no longer need the sign pointing to Him.",
   "right_division":"Israel pursued righteousness through the Law but did not attain it — Romans 9:31. Why? They sought it through works, not faith — verse 32. They stumbled over the stumbling stone — Christ — because they would not simply believe. For everyone who believes, Christ is the end.",
   "application":"Christ is your righteousness — completely, finally, fully. No more striving for legal standing before God. In Him, you have arrived. Rest in His completed work as your complete righteousness."},

  {"week":2,"day":12,"slot":3,
   "title":"Grace Is Not a License to Sin – Romans 6:1-2 | KJV Right Division",
   "labels":["Romans 6:1-2","Grace","Holiness","KJV","Sanctification","License"],
   "verse_text":"Shall we continue in sin, that grace may abound? God forbid. How shall we, that are dead to sin, live any longer therein?",
   "verse_ref":"Romans 6:1-2 KJV",
   "intro":"The most common objection to the Gospel of grace: <em>Won't people just sin freely if there's no Law?</em> Paul's answer is emphatic — <strong>God forbid.</strong> The question reveals a misunderstanding of what grace actually does. Grace does not leave people unchanged — it kills the old man and raises a new creation.",
   "right_division":"Titus 2:11-12 — <em>the grace of God that bringeth salvation teacheth us to deny ungodliness and worldly lusts.</em> Grace is the most powerful moral force in the universe — not because it threatens punishment, but because it transforms the heart through love.",
   "application":"Grace does not produce sin. Grace produces holiness — motivated by love for the One who gave everything, not fear of the One who condemns. Let grace teach you to say no to ungodliness today."},

  {"week":2,"day":12,"slot":4,
   "title":"Walk in the Spirit and You Will Not Fulfill the Flesh | Galatians 5:16 KJV",
   "labels":["Galatians 5:16","Holy Spirit","Walk","KJV","Grace","Holiness"],
   "verse_text":"This I say then, Walk in the Spirit, and ye shall not fulfil the lust of the flesh.",
   "verse_ref":"Galatians 5:16 KJV",
   "intro":"The solution to sinful living is not more Law — it is the Spirit. Walk in the Spirit — a continuous, step-by-step dependence on the Holy Spirit who indwells every believer. The promise is absolute: <em>ye shall not fulfil the lust of the flesh.</em> God's guarantee, not yours.",
   "right_division":"The fruit of the Spirit — love, joy, peace, longsuffering, gentleness, goodness, faith, meekness, temperance — is not produced by trying harder. It is produced by remaining yielded to the Spirit who produces it through you. You cooperate by yielding, not by striving.",
   "application":"Today's practice: In each moment of temptation, acknowledge Christ's life in you and walk in that life. Yield to the Spirit. The flesh loses its power in the Spirit's presence. This is grace-empowered holy living."},

  # ── Day 13 ──
  {"week":2,"day":13,"slot":1,
   "title":"The Law of Christ – Bearing One Another's Burdens | Galatians 6:2 KJV",
   "labels":["Galatians 6:2","Law of Christ","Love","KJV","Grace","Community"],
   "verse_text":"Bear ye one another's burdens, and so fulfil the law of Christ.",
   "verse_ref":"Galatians 6:2 KJV",
   "intro":"Paul refers to the <em>law of Christ</em> — distinct from the 613 commandments of Sinai. The law of Christ is not a religious code to perform — it is the principle of love expressed in bearing one another's burdens. John 13:34 — <em>love one another as I have loved you.</em>",
   "right_division":"The Mosaic Law said love your neighbor as yourself. The law of Christ says love as Christ loved — self-sacrificially, unconditionally, to the point of death. A higher standard — met only by the Spirit working through us, not by human effort under religious pressure.",
   "application":"Bear someone's burden today. That is the law of Christ in action — not rules to perform, but love to express. Who around you is carrying something heavy? Lift it with them. Let grace flow through you into their life."},

  {"week":2,"day":13,"slot":2,
   "title":"Abraham – Justified by Faith Before the Law Existed | Romans 4:1-5 KJV",
   "labels":["Abraham","Romans 4","Justification","Faith","KJV","Grace"],
   "verse_text":"But to him that worketh not, but believeth on him that justifieth the ungodly, his faith is counted for righteousness.",
   "verse_ref":"Romans 4:5 KJV",
   "intro":"Paul reaches back to Abraham to prove justification by faith. Abraham was declared righteous in Genesis 15:6 — before circumcision (Genesis 17), before the Law (Exodus 20), before any religious act. He simply believed God. That settled it.",
   "right_division":"If Abraham was justified by works, he could boast before God. But he had nothing to boast about before God. His righteousness was counted — credited, imputed — not earned. This is the pattern for every person who is justified in any age: believe God.",
   "application":"Abraham is your father in faith — not by blood, but by the same believing. Follow his example: believe God, and it is counted for righteousness. Faith is the only currency that purchases what grace freely offers."},

  {"week":2,"day":13,"slot":3,
   "title":"Sanctification by Grace – God Does the Work | 1 Thessalonians 5:23 KJV",
   "labels":["Sanctification","1 Thessalonians 5:23","KJV","Grace","Holy Spirit","God's Work"],
   "verse_text":"And the very God of peace sanctify you wholly; and I pray God your whole spirit and soul and body be preserved blameless unto the coming of our Lord Jesus Christ.",
   "verse_ref":"1 Thessalonians 5:23 KJV",
   "intro":"Paul's prayer for sanctification is addressed to God — not to the believers' effort. <em>The very God of peace sanctify you wholly.</em> God is the sanctifier. We are not sanctified by trying harder to keep the Law. We are sanctified by the God of peace working through His indwelling Spirit.",
   "right_division":"Sanctification has two aspects in Paul's letters: positional (you are already sanctified in Christ — 1 Corinthians 1:2) and progressive (God works in you to will and to do — Philippians 2:13). Both are God's work. Your part is yielding, not striving.",
   "application":"Yield yourself to the God of peace today. He is able to sanctify you wholly. What you cannot accomplish through effort, He accomplishes through His own working in you. That is grace-based sanctification."},

  {"week":2,"day":13,"slot":4,
   "title":"Eternal Security – 'I Will Never Leave Thee' | Hebrews 13:5 KJV",
   "labels":["Eternal Security","Hebrews 13:5","KJV","Grace","Assurance","Promise"],
   "verse_text":"For he hath said, I will never leave thee, nor forsake thee.",
   "verse_ref":"Hebrews 13:5 KJV",
   "intro":"Under the Law, blessing depended on obedience — Deuteronomy 28. Disobedience meant curse. The relationship was conditional on performance. But in the age of grace, God says <em>I will never leave thee, nor forsake thee</em> — the Greek is emphatic: never, no not ever, no not ever.",
   "right_division":"Paul confirms in Romans 8:38-39 — neither death, life, angels, principalities, powers, things present, things to come, height, depth, nor any other creature shall separate you from the love of God. The list is exhaustive. Nothing is omitted. You are eternally secure.",
   "application":"God will never leave you. That is not a feeling — it is a promise carved in the eternal faithfulness of God. Rest in His presence today, especially if circumstances make His nearness hard to feel. He said it. He means it. It is settled."},

  # ── Day 14 ──
  {"week":2,"day":14,"slot":1,
   "title":"Law's Shadows vs Grace's Reality – Colossians 2:17 KJV",
   "labels":["Colossians 2:17","Shadows","Substance","KJV","Grace","Christ"],
   "verse_text":"Which are a shadow of things to come; but the body is of Christ.",
   "verse_ref":"Colossians 2:17 KJV",
   "intro":"Shadows versus substance. The entire Levitical system — sacrifices, feasts, new moons, Sabbaths — were shadows cast by the coming reality. A shadow has the shape of the real thing but no substance of its own. When the real thing arrives, the shadow becomes unnecessary.",
   "right_division":"Christ is the substance. The Passover lamb was a shadow — Christ is the Lamb of God. The Day of Atonement was a shadow — Christ is the once-for-all High Priest. The tabernacle was a shadow — Christ is the true Tabernacle. Every shadow points to Him.",
   "application":"You have the substance — Christ Himself. Do not return to the shadows. Every feast, every sacrifice, every ordinance pointed to the glorious reality you now possess. Celebrate the substance, not the shadow."},

  {"week":2,"day":14,"slot":2,
   "title":"The Feasts of Israel – Every One Fulfilled in Christ | KJV",
   "labels":["Feasts of Israel","Passover","Resurrection","KJV","Dispensational","Prophecy"],
   "verse_text":"For even Christ our passover is sacrificed for us: Therefore let us keep the feast, not with old leaven, neither with the leaven of malice and wickedness.",
   "verse_ref":"1 Corinthians 5:7-8 KJV",
   "intro":"The seven feasts of Israel were God's prophetic calendar of redemption. The spring feasts were fulfilled at Christ's first coming: Passover at the crucifixion, Unleavened Bread in His sinless burial, Firstfruits in His resurrection, Pentecost in the Spirit's coming.",
   "right_division":"The fall feasts await Christ's second coming: Trumpets (Rapture/Second Coming), Atonement (Israel's national repentance), Tabernacles (Millennial Kingdom). God wrote the entire redemption calendar in advance through Israel's annual calendar. His precision is breathtaking.",
   "application":"Every feast points to Christ — crucified, buried, risen, and coming again. When you see the feasts, see the Saviour they announced. Celebrate the One every shadow was designed to reveal."},

  {"week":2,"day":14,"slot":3,
   "title":"Christ Our High Priest – Better Than the Levitical Priesthood | Hebrews 7:25 KJV",
   "labels":["High Priest","Hebrews 7:25","KJV","Intercession","Grace","Christ"],
   "verse_text":"Wherefore he is able also to save them to the uttermost that come unto God by him, seeing he ever liveth to make intercession for them.",
   "verse_ref":"Hebrews 7:25 KJV",
   "intro":"The Levitical priests served daily — offering sacrifices that could never finally take away sin. They died and were replaced. Their work was never finished. But Christ — our High Priest after the order of Melchizedek — offered one sacrifice forever and <strong>sat down</strong> — Hebrews 10:12.",
   "right_division":"He ever liveth to make intercession for you. Right now, Jesus is at the Father's right hand, interceding by name for you. Not a rotating priesthood, not a human intermediary — the eternal Son of God, presenting His own blood as the permanent basis of your access.",
   "application":"You need no human priest to access God. You have the greatest High Priest — eternal, perfect, alive, interceding for you this moment. Come boldly to the throne of grace — Hebrews 4:16. He invites you."},

  {"week":2,"day":14,"slot":4,
   "title":"One Sacrifice for Sins Forever – It Is Finished | Hebrews 10:12 KJV",
   "labels":["Hebrews 10:12","One Sacrifice","KJV","Finished","Grace","Salvation"],
   "verse_text":"But this man, after he had offered one sacrifice for sins for ever, sat down on the right hand of God.",
   "verse_ref":"Hebrews 10:12 KJV",
   "intro":"<em>One sacrifice. For sins. For ever. Sat down.</em> Every word is loaded with grace. The Levitical priests never sat — no chairs in the tabernacle — because their work was never complete. But Christ sat down. <strong>His work is finished.</strong> One sacrifice accomplishes what a million animal offerings never could.",
   "right_division":"<em>For ever</em> — not for a season, not until you sin again, not until the next confession. For ever. Your sins — past, present, and future — were all future when Christ died. He bore them all, once, for ever. This is the eternal Gospel of grace.",
   "application":"The sacrifice is made. The work is done. The Priest is seated. Your sins are forgiven — for ever. Rest in that finished work today, tomorrow, and into eternity. It cannot be undone. It is settled in heaven."},

  # ══ WEEK 3 ══ Kingdom vs Church / Prophetic vs Mystery ═══════════════════════
  {"week":3,"day":15,"slot":1,
   "title":"Keys of the Kingdom – What Did Jesus Give Peter? | Matthew 16:19 KJV",
   "labels":["Matthew 16:19","Keys of Kingdom","Peter","KJV","Dispensational","Kingdom"],
   "verse_text":"And I will give unto thee the keys of the kingdom of heaven: and whatsoever thou shalt bind on earth shall be bound in heaven.",
   "verse_ref":"Matthew 16:19 KJV",
   "intro":"The keys of the Kingdom have been used to justify papal authority, spiritual warfare techniques, and institutional Church power. But right division reveals that these keys were given to Peter specifically, in the context of Israel's Kingdom program — not to a religious institution for all time.",
   "right_division":"Peter used the keys at Pentecost — Acts 2 — opening the Kingdom offer to Israel, and in Acts 10 — opening the door to Gentiles in the transition. The keys served their purpose. For the Church age, our authority is in Christ's name — Ephesians 1:21.",
   "application":"You need no papal key to access God. Christ is the door — John 10:9 — <em>by me if any man enter in, he shall be saved.</em> The door is open. Walk through by faith today."},

  {"week":3,"day":15,"slot":2,
   "title":"The Mystery Revealed to Paul – Hidden for Ages | Ephesians 3:1-6 KJV",
   "labels":["Ephesians 3","Mystery","Paul","KJV","Body of Christ","Dispensational"],
   "verse_text":"Which in other ages was not made known unto the sons of men, as it is now revealed unto his holy apostles and prophets by the Spirit.",
   "verse_ref":"Ephesians 3:5 KJV",
   "intro":"Three staggering words define this passage: <em>mystery, hidden, revealed.</em> Not hinted at in the Old Testament. Not partially disclosed. Completely hidden — then fully revealed through Paul. The mystery is that Gentiles are now fellow heirs, of the same body, partakers of the promise in Christ.",
   "right_division":"The Old Testament prophets saw Israel's King coming and returning. They could not see the parenthesis between — this age of grace, the Body of Christ, the mystery. God specifically chose Paul — the former persecutor — as the revealer of this breathtaking secret.",
   "application":"You are living in the mystery. You are a fellow heir — not a second-class citizen grafted into Israel's program, but a full heir in the Body of Christ. That identity is worth meditating on every single day."},

  {"week":3,"day":15,"slot":3,
   "title":"Israel vs the Church – Two Distinct Programs in God's Perfect Plan | KJV",
   "labels":["Israel vs Church","Dispensational","KJV","Two Programs","Body of Christ"],
   "verse_text":"Even the mystery which hath been hid from ages and from generations, but now is made manifest to his saints.",
   "verse_ref":"Colossians 1:26 KJV",
   "intro":"Confusing Israel and the Church is the single greatest source of theological error in Christianity. They are not the same group, do not share the same covenants, do not have the same promises, and do not share the same future. Recognizing the distinction brings immediate clarity to Scripture.",
   "right_division":"Israel: earthly covenants, land promises, national program, Kingdom future. The Church: heavenly position, spiritual blessings in heavenly places, the mystery revealed through Paul, a heavenly destiny with Christ. Both are glorious. Both must be kept distinct.",
   "application":"Knowing you are part of the Body of Christ — not a spiritual Israel — gives you a clear identity, a specific calling, and an unconfused future. Live from that clarity today."},

  {"week":3,"day":15,"slot":4,
   "title":"Romans 11 – Israel's Future: Grafting and All Israel Saved | KJV",
   "labels":["Romans 11","Israel","Olive Tree","KJV","Dispensational","Future"],
   "verse_text":"And so all Israel shall be saved: as it is written, There shall come out of Sion the Deliverer, and shall turn away ungodliness from Jacob.",
   "verse_ref":"Romans 11:26 KJV",
   "intro":"Has God abandoned Israel? Romans 11:1 — <em>God forbid.</em> The gifts and calling of God are without repentance — verse 29. God has temporarily set Israel aside as a nation — not forever — while Gentiles are being saved in the age of grace. But Israel's story is not over.",
   "right_division":"The olive tree belongs to Israel. The wild branches — Gentile believers — have been grafted in through faith. When the fullness of the Gentiles comes in — verse 25 — Israel's blindness lifts, and all Israel will be saved. Romans 11 is replacement theology's greatest refutation.",
   "application":"Love Israel. Pray for Israel. God has not forgotten His people. And if His covenant faithfulness to Israel is certain, His faithfulness to you — a wild branch grafted in by grace — is equally certain."},

  # ── Day 16 ──
  {"week":3,"day":16,"slot":1,
   "title":"Acts 7 – Stephen and the Great Dispensational Transition | KJV",
   "labels":["Acts 7","Stephen","Transition","Paul","KJV","Dispensational"],
   "verse_text":"But he, being full of the Holy Ghost, looked up stedfastly into heaven, and saw the glory of God, and Jesus standing on the right hand of God.",
   "verse_ref":"Acts 7:55 KJV",
   "intro":"Jesus is standing. After His ascension, Christ is always <em>seated</em> at the Father's right hand — Hebrews 10:12. But at Stephen's martyrdom, He stands. As if rising to welcome this faithful witness — and to mark a turning point in dispensational history.",
   "right_division":"Israel's religious leadership heard Stephen's complete review of their history and rejected it with violence. Saul of Tarsus watched. Within chapters, Saul becomes Paul. The transition from Israel's Kingdom program to the mystery of the Body of Christ is now fully underway.",
   "application":"God's plan was never in danger. Stephen's death looked like defeat but was the hinge of a new age. Whatever looks like defeat in your life may be the hinge of God's next great movement. Trust His sovereignty absolutely."},

  {"week":3,"day":16,"slot":2,
   "title":"Kingdom Parables – Earthly Kingdom or Heavenly Mystery? | Matthew 13 KJV",
   "labels":["Kingdom Parables","Matthew 13","KJV","Dispensational","Kingdom"],
   "verse_text":"The kingdom of heaven is like to a grain of mustard seed, which a man took, and sowed in his field.",
   "verse_ref":"Matthew 13:31 KJV",
   "intro":"The parables of Matthew 13 describe the Kingdom of Heaven during the King's absence — the mustard seed growing mixed with the world, the wheat and tares together, the treasure hidden in the field. These are Kingdom truth — describing the world during the current age from Israel's prophetic perspective.",
   "right_division":"These parables are not Church truth — they are Kingdom truth. The Church is not the Kingdom. The Kingdom will be literal, visible, and glorious at the Second Coming. Right now the Kingdom exists in mystery form — the King is away, but returning.",
   "application":"Read the Kingdom parables through dispensational eyes — they reveal the mixed condition of the current age and the certainty of the coming Kingdom. The treasure is worth everything. The King is coming for it."},

  {"week":3,"day":16,"slot":3,
   "title":"The Church as the Body of Christ – Ephesians 1:22-23 | KJV",
   "labels":["Body of Christ","Ephesians 1:22-23","KJV","Church","Head","Mystery"],
   "verse_text":"And gave him to be the head over all things to the church, Which is his body, the fulness of him that filleth all in all.",
   "verse_ref":"Ephesians 1:22-23 KJV",
   "intro":"The Church is not an institution, a building, or a religious organization. The Church is a living organism — the Body of Christ — with Christ as its Head. And this Body is described as His <em>fulness</em> — the fulness of Him who fills all in all. Breathtaking.",
   "right_division":"This Body — revealed to Paul — is comprised of all who are saved during the age of grace, placed into Christ by the baptism of the Spirit at the moment of belief — 1 Corinthians 12:13. Jew and Gentile, slave and free, all equally and permanently in Christ.",
   "application":"You are not just a church member — you are a member of the Body of Christ, organically connected to the Head. His life is your life. His fullness fills you. Live from that reality today."},

  {"week":3,"day":16,"slot":4,
   "title":"Bride of Christ vs Body of Christ – Two Beautiful Images | KJV",
   "labels":["Bride of Christ","Body of Christ","Ephesians 5","Revelation 21","KJV"],
   "verse_text":"For the husband is the head of the wife, even as Christ is the head of the church: and he is the saviour of the body.",
   "verse_ref":"Ephesians 5:23 KJV",
   "intro":"Two images describe God's people — the Body and the Bride. The Body speaks of union, organic connection, and shared life. The Bride speaks of love, covenant, and eternal intimacy. Both are beautiful, both are scriptural, and both require right division to understand fully.",
   "right_division":"Ephesians 5 applies the Bride/Body image to the present Church age relationship with Christ. Revelation 21's Bride — the New Jerusalem — appears in the future, prophetic context of the eternal state. Both point to the same glorious reality: Christ's eternal love for His people.",
   "application":"Christ loves you with a love deeper than any human marriage can illustrate. He gave Himself for you. He is preparing a place for you. He is coming to receive you. That is your eternal story."},

  # ── Day 17 ──
  {"week":3,"day":17,"slot":1,
   "title":"The Great Commission – Matthew 28 vs Paul's Commission | KJV Right Division",
   "labels":["Great Commission","Matthew 28","Paul","KJV","Dispensational","Gospel"],
   "verse_text":"Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost.",
   "verse_ref":"Matthew 28:19 KJV",
   "intro":"Matthew 28 was given to the Eleven — the Jewish apostles of Israel's program — to baptize all nations and teach them everything Jesus commanded. This is Kingdom truth. Paul's commission was different: to reveal the mystery, preach the grace Gospel, and build the Body of Christ.",
   "right_division":"The 144,000 of Revelation — Jewish missionaries during the Tribulation — will fulfill Matthew 28 globally in a way the Church age never has. For us today, Paul's commission applies: 2 Timothy 2:2 — commit to faithful men who will teach others.",
   "application":"Your commission: share the Gospel of Grace — 1 Corinthians 15:1-4 — with every person around you. Not complicated. Not conditional. The death, burial, and resurrection of Christ, offered freely to all who believe."},

  {"week":3,"day":17,"slot":2,
   "title":"Signs and Wonders – Which Dispensation Are They For? | KJV",
   "labels":["Signs and Wonders","Dispensational","Miracles","KJV","2 Corinthians 12:12"],
   "verse_text":"Truly the signs of an apostle were wrought among you in all patience, in signs, and wonders, and mighty deeds.",
   "verse_ref":"2 Corinthians 12:12 KJV",
   "intro":"Signs and wonders were <em>the signs of an apostle</em> — given to authenticate the apostolic message during the Acts transition period. They were signs to Israel — 1 Corinthians 1:22 — confirming the Kingdom offer was going out. As that period closed, their role diminished.",
   "right_division":"Paul left Trophimus sick (2 Tim 4:20), advised wine for Timothy's stomach (1 Tim 5:23), and did not heal Epaphroditus miraculously (Phil 2:27). These are not failures — they are dispensational development. The Word, now complete, is our authority — 2 Timothy 3:16-17.",
   "application":"Build your faith on the Word, not on signs. The completed Scripture is sufficient for doctrine, reproof, correction, and instruction. God still works powerfully — but faith rests on His Word, not on signs as evidence."},

  {"week":3,"day":17,"slot":3,
   "title":"Tongues – A Sign for Unbelieving Israel | 1 Corinthians 14:22 KJV",
   "labels":["Tongues","1 Corinthians 14:22","Israel","Sign Gift","KJV","Dispensational"],
   "verse_text":"Wherefore tongues are for a sign, not to them that believe, but to them that believe not.",
   "verse_ref":"1 Corinthians 14:22 KJV",
   "intro":"Tongues were a covenant sign for Israel — Paul cites Isaiah 28:11 as the precedent. At Pentecost, Jewish diaspora heard the Gospel in their own languages — a miraculous sign that God was moving among His people. Tongues told Israel: the Kingdom offer is going out.",
   "right_division":"Paul's correction of the Corinthian tongue-speakers is extensive — 1 Corinthians 14. <em>I had rather speak five words with my understanding than ten thousand in an unknown tongue.</em> The gift, properly used, required interpretation. Chaotic ecstatic use was not endorsed.",
   "application":"Your access to God does not require a gift of tongues. The Spirit intercedes for you — Romans 8:26-27. You have direct access to the Father in the name of Christ. That is sufficient, glorious, and eternally secure."},

  {"week":3,"day":17,"slot":4,
   "title":"Healing in the Kingdom vs the Age of Grace | KJV Right Division",
   "labels":["Healing","Kingdom","Grace Age","KJV","Dispensational","Trophimus"],
   "verse_text":"My grace is sufficient for thee: for my strength is made perfect in weakness.",
   "verse_ref":"2 Corinthians 12:9 KJV",
   "intro":"During Jesus's ministry, healing was universal and immediate — every sickness healed, every disease cured. This demonstrated Kingdom power — Isaiah 35 prophesied these exact signs. But in Paul's later epistles, the pattern shifts dramatically, revealing dispensational development.",
   "right_division":"Paul left Trophimus sick, gave Timothy medical advice, and watched Epaphroditus nearly die. By the end of his ministry, Paul's emphasis shifted from Kingdom signs to sufficiency of Christ in suffering. <em>My grace is sufficient</em> — that is the grace-age promise.",
   "application":"God still heals sovereignly and miraculously. But we do not have a guaranteed healing covenant in this age. Our promise is: in health or illness, His grace is sufficient. His strength is perfected in your weakness."},

  # ── Day 18 ──
  {"week":3,"day":18,"slot":1,
   "title":"The Rapture – A Mystery Paul Revealed | 1 Thessalonians 4:16-17 KJV",
   "labels":["Rapture","1 Thessalonians 4","Mystery","KJV","Dispensational","Hope"],
   "verse_text":"Then we which are alive and remain shall be caught up together with them in the clouds, to meet the Lord in the air: and so shall we ever be with the Lord.",
   "verse_ref":"1 Thessalonians 4:17 KJV",
   "intro":"Caught up — <em>rapturo</em> in Latin. The Rapture of the Church is a mystery revealed through Paul — 1 Corinthians 15:51: <em>Behold, I shew you a mystery; We shall not all sleep, but we shall all be changed.</em> This specific event was hidden in the Old Testament and revealed to Paul.",
   "right_division":"The Rapture (Church caught up to meet Christ in the air) differs from the Second Coming (Christ descending to earth — Zechariah 14:4). Two distinct events, two distinct groups, separated by at least seven years. The Church is not appointed to wrath — 1 Thessalonians 5:9.",
   "application":"<em>Wherefore comfort one another with these words</em> — 1 Thessalonians 4:18. The Rapture is not a terrifying doctrine — it is a comforting promise. Live ready. Live expectantly. He could come today."},

  {"week":3,"day":18,"slot":2,
   "title":"The Second Coming – Prophetic, Not Mystery | Matthew 24 KJV",
   "labels":["Second Coming","Matthew 24","Prophecy","KJV","Dispensational","Israel"],
   "verse_text":"And they shall see the Son of man coming in the clouds of heaven with power and great glory.",
   "verse_ref":"Matthew 24:30 KJV",
   "intro":"Matthew 24 is not about the Church. Jesus spoke it to His Jewish disciples on the Mount of Olives, answering their question about the temple's destruction and the end of the age. Every sign He describes — wars, famines, the abomination of desolation — belongs to Israel's Tribulation.",
   "right_division":"The Rapture is for the Church — caught up before the Tribulation. The Second Coming is for Israel and the nations — Christ returning to earth, feet on the Mount of Olives, to establish the literal Millennial Kingdom. Both are glorious. Both are certain. Both require right division to distinguish.",
   "application":"The Second Coming should fill you with anticipation — not anxiety. God's plan for Israel and the nations will be completed on schedule. Every wrong made right. Every promise fulfilled. The King is coming."},

  {"week":3,"day":18,"slot":3,
   "title":"Tribulation Saints vs Church Age Believers – Key Differences | KJV",
   "labels":["Tribulation Saints","Church Age","Revelation 7","KJV","Dispensational","Rapture"],
   "verse_text":"These are they which came out of great tribulation, and have washed their robes, and made them white in the blood of the Lamb.",
   "verse_ref":"Revelation 7:14 KJV",
   "intro":"Revelation 7 describes a vast multitude coming out of great tribulation — believers who come to faith during the seven-year Tribulation period after the Church has been raptured. They are not Church age believers. They are a distinct group in God's prophetic calendar.",
   "right_division":"Tribulation saints face conditions the Church age believer never will: enduring to the end (Matthew 24:13), refusing the mark of the beast (Revelation 13), potential martyrdom as the norm. Right division protects you from applying their instructions to your grace-age life.",
   "application":"You live in the age of grace — the most favorable moment in history to be a believer. No tribulation, no mark of the beast, no endure-to-the-end condition. Just the indwelling Spirit and the full mystery revealed. Be deeply grateful."},

  {"week":3,"day":18,"slot":4,
   "title":"Daniel's 70 Weeks – God's Perfect Timetable for Israel | Daniel 9:24 KJV",
   "labels":["Daniel 9","70 Weeks","Israel","Prophecy","KJV","Dispensational"],
   "verse_text":"Seventy weeks are determined upon thy people and upon thy holy city, to finish the transgression, and to make an end of sins.",
   "verse_ref":"Daniel 9:24 KJV",
   "intro":"490 years — 70 weeks of seven years — decreed for Israel's prophetic calendar. Sixty-nine weeks were fulfilled precisely from the decree to rebuild Jerusalem to the crucifixion of Christ. The mathematical precision is breathtaking. Then a gap — and one week remains.",
   "right_division":"The gap between the 69th and 70th week is the Church age — the dispensational parenthesis. Daniel's prophetic clock for Israel stopped. When the Rapture occurs, it resumes. The 70th week — the Tribulation — will complete God's dealings with Israel before the Kingdom.",
   "application":"If God fulfilled 69 weeks to the very day, He will fulfill the 70th with equal precision. His Word is perfect. His timetable never fails. Trust every promise He has made — to Israel and to you."},

  # ── Day 19 ──
  {"week":3,"day":19,"slot":1,
   "title":"Is the Church in the Book of Revelation? | Revelation 4:1 KJV",
   "labels":["Revelation","Church","Rapture","KJV","Dispensational","Revelation 4:1"],
   "verse_text":"Come up hither, and I will shew thee things which must be hereafter.",
   "verse_ref":"Revelation 4:1 KJV",
   "intro":"After chapters 2 and 3 — the letters to the seven churches — John is called up to heaven. <em>Come up hither.</em> From Revelation 4 through 19, the word <em>church</em> does not appear. Instead: the 144,000 Jewish evangelists, Israel, the nations. The Church has been removed.",
   "right_division":"Many dispensational teachers see Revelation 4:1 as a picture of the Rapture — the Church called up before the Tribulation. Revelation 19 brings the Church back with Christ at the Second Coming. The structure of Revelation itself confirms the Church is not in the Tribulation.",
   "application":"The Tribulation judgments of Revelation are not for you. Revelation 3:10 — <em>I also will keep thee from the hour of temptation.</em> Rest in that promise. The Lamb who loves you has made provision for your protection."},

  {"week":3,"day":19,"slot":2,
   "title":"The Millennial Kingdom – Peace on Earth Under King Jesus | Isaiah 2 KJV",
   "labels":["Millennium","Kingdom","Isaiah 2","Zechariah","KJV","Dispensational"],
   "verse_text":"And the LORD shall be king over all the earth: in that day shall there be one LORD, and his name one.",
   "verse_ref":"Zechariah 14:9 KJV",
   "intro":"One thousand years of Christ reigning on earth — Revelation 20:1-6. Not allegory. Not metaphor. Literal. The wolf and lamb together — Isaiah 11:6. Weapons turned to farming tools — Isaiah 2:4. The knowledge of the Lord covering the earth — Isaiah 11:9. The King reigning from Jerusalem.",
   "right_division":"The Church will reign with Christ — Revelation 20:6. Not as Israel in the Kingdom, but as glorified members of the Body of Christ reigning alongside the King. Israel will be the head of the nations. The Church will be glorified co-heirs reigning from the heavenly dimension.",
   "application":"The best is ahead. This broken world will be healed. The King is coming. Peace will cover the earth like the waters cover the sea. Let the certainty of the Kingdom reframe every hardship you face today."},

  {"week":3,"day":19,"slot":3,
   "title":"The Kingdom in Mystery Form – Present Reality | Luke 17:20-21 KJV",
   "labels":["Kingdom of God","Mystery Form","Current Age","KJV","Dispensational","Spirit"],
   "verse_text":"The kingdom of God cometh not with observation: Neither shall they say, Lo here! or, lo there! for, behold, the kingdom of God is within you.",
   "verse_ref":"Luke 17:20-21 KJV",
   "intro":"The Kingdom of God is present in mystery form right now — not in its full literal, political manifestation, but in the spiritual reality of the King living in His people. Romans 14:17 — <em>the kingdom of God is righteousness, and peace, and joy in the Holy Ghost.</em>",
   "right_division":"The Kingdom has come (Christ came, died, rose, sent His Spirit), and the Kingdom is coming (the literal, earthly, political Kingdom awaits the Second Coming). The already-and-not-yet. The Church lives in the mystery form of the Kingdom while awaiting its literal arrival.",
   "application":"You carry the Kingdom within you — the Spirit of the King, the righteousness of Christ, the peace that passes understanding. Let that Kingdom reality shine through your life today as a foretaste of what is coming."},

  {"week":3,"day":19,"slot":4,
   "title":"Spirit Baptism Into the Body – 1 Corinthians 12:13 | KJV",
   "labels":["Spirit Baptism","1 Corinthians 12:13","Body of Christ","KJV","Dispensational"],
   "verse_text":"For by one Spirit are we all baptized into one body, whether we be Jews or Gentiles, whether we be bond or free.",
   "verse_ref":"1 Corinthians 12:13 KJV",
   "intro":"How did you enter the Body of Christ? By one Spirit — all believers — baptized into one body. This is the defining moment of your entrance into the Church. Universal, immediate at salvation, permanent. This is not a second experience you seek — it happened when you believed.",
   "right_division":"Spirit baptism is distinct from water baptism and from speaking in tongues. It is the act of the Holy Spirit placing every believer into the Body of Christ at the moment of faith. Ephesians 4:5 — one baptism. The Spirit baptism into the one Body.",
   "application":"You are in the Body of Christ — not because of any experience or ritual, but because the Spirit placed you there when you believed. That is settled, certain, and gloriously permanent. Rest in it."},

  # ── Day 20 ──
  {"week":3,"day":20,"slot":1,
   "title":"Water Baptism in the Age of Grace – Required for Salvation? | KJV",
   "labels":["Water Baptism","Grace Age","KJV","Dispensational","1 Corinthians 1:17","Salvation"],
   "verse_text":"For Christ sent me not to baptize, but to preach the gospel: not with wisdom of words, lest the cross of Christ should be made of none effect.",
   "verse_ref":"1 Corinthians 1:17 KJV",
   "intro":"Paul — the apostle of the grace age — says Christ did not send him to baptize but to preach the Gospel. If water baptism were required for salvation, this statement would be impossible. Paul deliberately placed baptism outside the essential Gospel definition.",
   "right_division":"In the Kingdom program, Acts 2:38 connects baptism to remission of sins for Israel. In the grace program, Romans 10:9-10 — believe in your heart, confess with your mouth — no water. The thief on the cross was never baptized. Jesus said: <em>today shalt thou be with me in paradise.</em>",
   "application":"Water baptism is a beautiful, meaningful public declaration of what Christ has done in you. But it does not save. Faith alone in Christ alone saves — Ephesians 2:8-9. Believe that with settled confidence."},

  {"week":3,"day":20,"slot":2,
   "title":"The Lord's Supper – Memorial, Not Sacrifice | 1 Corinthians 11:26 KJV",
   "labels":["Lord's Supper","Communion","1 Corinthians 11","KJV","Dispensational","Memorial"],
   "verse_text":"For as often as ye eat this bread, and drink this cup, ye do shew the Lord's death till he come.",
   "verse_ref":"1 Corinthians 11:26 KJV",
   "intro":"<em>Ye do shew the Lord's death till he come.</em> The Lord's Supper is a proclamation — a memorial that looks backward to the cross and forward to His return. Not a re-sacrifice. Not transubstantiation. A memorial, given by Paul by direct revelation — verse 23.",
   "right_division":"The Mass, which claims to re-present Christ's sacrifice, contradicts Hebrews 10:10 — <em>once for all.</em> One sacrifice. Done. The bread and cup declare that finished work until He comes. This is Paul's grace-age instruction for the Body of Christ.",
   "application":"The next time you take the Lord's Supper, take it with deliberate gratitude — remembering His broken body and shed blood given for you. And look forward: <em>till he come.</em> Every communion is a declaration that the King is coming back."},

  {"week":3,"day":20,"slot":3,
   "title":"The Lord's Prayer – Kingdom Prayer or Grace Age Model? | Matthew 6 KJV",
   "labels":["Lord's Prayer","Matthew 6","Kingdom","Grace Age","KJV","Dispensational"],
   "verse_text":"Thy kingdom come. Thy will be done in earth, as it is in heaven.",
   "verse_ref":"Matthew 6:10 KJV",
   "intro":"The Lord's Prayer is beloved and treasured — given by Jesus to His Jewish disciples before the cross, in the context of the Kingdom program. <em>Thy kingdom come</em> is a Kingdom petition — praying for the literal establishment of the earthly Kingdom. Its context is Israel's program.",
   "right_division":"For the grace age, Paul gives a different model: pray in the name of Jesus — John 16:23-24. Pray in the Spirit — Ephesians 6:18. Pray with thanksgiving — Philippians 4:6. Pray without ceasing — 1 Thessalonians 5:17. Access is direct, continuous, and in Christ's name.",
   "application":"Pray freely, pray boldly, pray constantly — in Jesus's name. You have direct access to the Father. No formula required. No formula forbidden. Just a heart that knows its Father and approaches Him with full confidence."},

  {"week":3,"day":20,"slot":4,
   "title":"Kingdom Rewards vs Grace Inheritance – Both Are Glorious | KJV",
   "labels":["Rewards","Inheritance","Romans 8:17","KJV","Grace","Dispensational"],
   "verse_text":"And if children, then heirs; heirs of God, and joint-heirs with Christ.",
   "verse_ref":"Romans 8:17 KJV",
   "intro":"Scripture distinguishes between rewards (earned by faithful service) and inheritance (received as a child of God). In the Kingdom program, rewards are directly linked to performance — Matthew 25's talents. In the grace age, both concepts apply — with a crucial difference at the foundation.",
   "right_division":"The Judgment Seat of Christ — 2 Corinthians 5:10 — evaluates works for rewards, not for salvation. Your eternal life is never at stake there. But your inheritance as a child of God is unconditional — Romans 8:17, Ephesians 1:11. Received freely. Cannot be lost.",
   "application":"Your inheritance is secured by grace — received as God's child. Your rewards are built through faithful service. Serve well — not to earn sonship, but because you already have it and love the Father who gave it."},

  # ── Day 21 ──
  {"week":3,"day":21,"slot":1,
   "title":"Matthew 10 – Instructions to the Twelve: For Israel, Not the Church | KJV",
   "labels":["Matthew 10","Twelve Apostles","Israel","KJV","Dispensational","Commission"],
   "verse_text":"Go not into the way of the Gentiles, and into any city of the Samaritans enter ye not: But go rather to the lost sheep of the house of Israel.",
   "verse_ref":"Matthew 10:5-6 KJV",
   "intro":"If Matthew 10 is the universal commission for all Christians, Paul was disobedient — he was specifically called to the Gentiles. Right division resolves the apparent contradiction instantly: Jesus gave the Twelve a specific commission for a specific dispensational context — Israel's Kingdom program.",
   "right_division":"Matthew 10's instructions — go only to Israel, take no money, shake the dust — are Kingdom-context specific. Verse 23 — <em>ye shall not have gone over the cities of Israel till the Son of man be come</em> — points to Tribulation-period fulfillment, not Church-age practice.",
   "application":"Your commission is Paul's: share the Grace Gospel with everyone around you — Jew, Gentile, all nations. Not just Israel. Not with signs required. Just the death, burial, and resurrection of Christ offered freely to all who believe."},

  {"week":3,"day":21,"slot":2,
   "title":"Paul's Prison Epistles – The Peak of Mystery Revelation | KJV",
   "labels":["Prison Epistles","Ephesians","Philippians","Colossians","KJV","Mystery"],
   "verse_text":"For this cause I Paul, the prisoner of Jesus Christ for you Gentiles.",
   "verse_ref":"Ephesians 3:1 KJV",
   "intro":"From a Roman prison cell, Paul wrote four letters — Ephesians, Philippians, Colossians, Philemon — that represent the highest, fullest revelation of the mystery of the Body of Christ in all of Scripture. Chained physically, he was never more spiritually free or doctrinally elevated.",
   "right_division":"Ephesians: your position — every spiritual blessing in heavenly places. Philippians: your practice — rejoice, the mind of Christ, citizenship in heaven. Colossians: your preeminence — Christ in you the hope of glory, Christ who is all. Philemon: a parable of grace in action.",
   "application":"Set aside time this week to read one prison epistle slowly. Let the mystery of your position in Christ wash over you. You are seated with Him in heavenly places — Ephesians 2:6. That is your reality right now, as you read these words."},

  {"week":3,"day":21,"slot":3,
   "title":"Ephesians 1 – Every Spiritual Blessing Already Yours | KJV Right Division",
   "labels":["Ephesians 1","Spiritual Blessings","Heavenly Places","KJV","Grace","Identity"],
   "verse_text":"Blessed be the God and Father of our Lord Jesus Christ, who hath blessed us with all spiritual blessings in heavenly places in Christ.",
   "verse_ref":"Ephesians 1:3 KJV",
   "intro":"<em>Hath blessed</em> — past tense, completed action. <em>All</em> spiritual blessings — not some. <em>In heavenly places</em> — not earthly, not conditional on circumstances. <em>In Christ</em> — secured in Him, inseparable from Him. This is your starting point, not your destination.",
   "right_division":"Paul then lists them: chosen before the foundation of the world (v.4), predestined unto adoption (v.5), accepted in the Beloved (v.6), redeemed through His blood (v.7), sealed with the Holy Spirit (v.13). Every one is already yours. Given. Sealed. Settled.",
   "application":"You are already blessed with everything God has to give in Christ. Not striving toward it — standing in it. Let that reality of abundance, not scarcity, be the foundation of how you approach every moment of this day."},

  {"week":3,"day":21,"slot":4,
   "title":"New Heavens and New Earth – Eternity's Glorious Distinctions | KJV",
   "labels":["New Heavens","New Earth","Revelation 21","Isaiah 65","KJV","Dispensational","Eternity"],
   "verse_text":"Eye hath not seen, nor ear heard, neither have entered into the heart of man, the things which God hath prepared for them that love him.",
   "verse_ref":"1 Corinthians 2:9 KJV",
   "intro":"Both Isaiah and John speak of new heavens and a new earth. Isaiah 65's description sounds like the Millennial Kingdom — people still born, long lives, building, planting. Revelation 21-22 goes beyond — no more death, no more sea, God Himself as temple and light. Eternity in its fullest expression.",
   "right_division":"Whether Israel and the Church maintain distinct roles in eternity is debated among dispensational teachers. What is certain: God has prepared something for you that no eye has seen, no ear has heard, no heart has imagined. The same God who planned all of history with perfect precision has prepared your eternal home.",
   "application":"Thank you for studying three weeks of right division together. God's plan is comprehensive, precise, and gloriously good. The best is infinitely ahead. Study to shew thyself approved — 2 Timothy 2:15. Amen."},
]

# ─── AUTH ─────────────────────────────────────────────────────────────────────
def get_blogger_service():
    creds = None
    if Path(BLOG_TOKEN_PICKLE).exists():
        with open(BLOG_TOKEN_PICKLE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(BLOG_TOKEN_PICKLE, "wb") as f:
            pickle.dump(creds, f)
    return build("blogger", "v3", credentials=creds)

# ─── GET BLOG ID ──────────────────────────────────────────────────────────────
def get_blog_id(service):
    result = service.blogs().getByUrl(url=f"https://{BLOG_URL}").execute()
    return result["id"]

# ─── TRACK POSTED ─────────────────────────────────────────────────────────────
POSTED_LOG = Path("output/posted_blog.json")
def load_posted():
    if POSTED_LOG.exists():
        return json.loads(POSTED_LOG.read_text())
    return {}

def save_posted(d):
    POSTED_LOG.parent.mkdir(exist_ok=True)
    POSTED_LOG.write_text(json.dumps(d, indent=2))

# ─── POST ─────────────────────────────────────────────────────────────────────
def post_all():
    service = get_blogger_service()
    blog_id = get_blog_id(service)
    print(f"Blog ID: {blog_id}")
    posted = load_posted()

    for i, p in enumerate(POSTS):
        key = f"w{p['week']}d{p['day']}s{p['slot']}"
        if key in posted:
            print(f"  [skip] {key} already posted → {posted[key]['url']}")
            continue

        # Schedule: Day+1 for first 4, Day+2 for next 4, etc.
        day_offset = i // 4 + 1
        slot       = i % 4
        h, m = SCHEDULE_TIMES[slot].split(":")
        publish_dt = datetime.datetime(
            TODAY.year, TODAY.month, TODAY.day,
            int(h), int(m), 0, tzinfo=KST
        ) + datetime.timedelta(days=day_offset)

        body = {
            "title": p["title"],
            "content": make_html(p),
            "labels": p["labels"],
            "published": publish_dt.isoformat(),
        }

        try:
            result = service.posts().insert(
                blogId=blog_id,
                body=body,
                isDraft=False,
            ).execute()

            url = result.get("url", "")
            posted[key] = {"title": p["title"], "url": url, "scheduled": publish_dt.isoformat()}
            save_posted(posted)
            print(f"  ✓ Posted [{key}] {p['title'][:55]}...")
            print(f"    → {url}")
        except Exception as e:
            print(f"  ✗ Failed [{key}]: {e}")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Rightly Dividing KJV – Blogspot Auto-Poster ===")
    print(f"Posting 88 articles to {BLOG_URL}")
    print(f"Scheduled from {TODAY + datetime.timedelta(days=1)} · 4×/day KST\n")
    post_all()
    print("\n✅ Done! All posts submitted to rightlydividing.blogspot.com")
