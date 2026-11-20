---
name: avoid-ai-writing
description: >-
  Audit and rewrite prose to eliminate artificial AI-isms, hollow clichés, repetitive templates,
  and formulaic listicles. Enforces 43-word precision replacement, 21 anti-AI pattern categories,
  and authentic human voice in both English and Bengali.
risk: none
source: https://github.com/conorbronsdon/avoid-ai-writing
---

# Avoid AI Writing (অ্যান্টি-রোবটিক ও মানবিক লেখার স্কিল)

Detects and fixes AI writing patterns ("AI-isms") that make text sound machine-generated, generic, and uninspired. Covers all 21 pattern categories and the complete 43-entry replacement catalog for English and Bengali.

---

## ⚡ ১৫-সেকেন্ডে মূল উদ্দেশ্য (Core Mission)

ChatGPT ও সাধারণ এলএলএম-এর সবচেয়ে বড় দুর্বলতা হলো তারা একঘেয়ে, ভনিতা-ভরা এবং চটুল ভাষায় লেখে (যেমন "In today's fast-paced world...", "Moreover, delve into the tapestry..."). 

এই স্কিলের উদ্দেশ্য হলো:
1. কৃত্রিম ও ফাঁপা শব্দ এবং রোবটিক ক্লিশে ছাঁটাই করা।
2. অপ্রয়োজনীয় ১০-পয়েন্ট তালিকা ও অলঙ্কার বর্জন করে সোজা, প্র্যাকটিক্যাল ও রক্ত-মাংসের মানবিক ভাষায় লেখা।
3. বাংলা ও ইংরেজি উভয় ভাষায় লেখার মেজাজ স্বাভাবিক ও সজীব রাখা।

---

## 📋 ৪৩টি অতি-ব্যবহৃত রোবটিক শব্দের প্রাকৃতিক বিকল্প (The 43-Entry Table)

| ক্রম | এআই-শব্দ (AI-ism) | প্রাকৃতিক বিকল্প (Plainer Alternative) | বাংলা পরিহারযোগ্য রূপ ও সহজ রূপ |
| :--- | :--- | :--- | :--- |
| ১ | Delve / Delve into | Explore, look at, examine | "গভীর অনুসন্ধান করা" $\rightarrow$ দেখা / জানা |
| ২ | Leverage | Use, take advantage of | "কাজে লাগানো / লিভারেজ" $\rightarrow$ ব্যবহার করা |
| ৩ | Tapestry | Mix, collection, variety | "জটিল জালিকা / টেপেস্ট্রি" $\rightarrow$ বৈচিত্র্য |
| ৪ | Foster | Encourage, build, support | "লালন-পালন করা" $\rightarrow$ তৈরি করা / বাড়ানো |
| ৫ | Beacon | Guide, model, example | "আলোকবর্তিকা" $\rightarrow$ পথপ্রদর্শক / উদাহরণ |
| ৬ | Robust | Reliable, strong, sturdy | "মজবুত ও রোবাস্ট" $\rightarrow$ টেকসই / নির্ভরযোগ্য |
| ৭ | Seamless | Smooth, easy, direct | "বাধাহীন ও সিমলেস" $\rightarrow$ সহজ / সরাসরি |
| ৮ | Testament | Proof, sign, evidence | "প্রমাণ বা সাক্ষ্য বহন করে" $\rightarrow$ প্রমাণ |
| ৯ | Realm | Area, field, world | "জগৎ বা রাজ্য" $\rightarrow$ ক্ষেত্র / বিষয় |
| ১০ | Multifaceted | Complex, varied, diverse | "বহুমাত্রিক" $\rightarrow$ নানা দিকসম্পন্ন |
| ১১ | Pivotal | Crucial, key, vital | "যুগান্তকারী / অতীব গুরুত্বপূর্ণ" $\rightarrow$ জরুরি |
| ১২ | Embark / Embark upon | Start, begin, launch | "যাত্রা শুরু করা" $\rightarrow$ শুরু করা |
| ১৩ | Elevate | Improve, raise, lift | "উন্নীত করা" $\rightarrow$ ভালো করা / বাড়ানো |
| ১৪ | Harness | Use, apply, capture | "কাজে লাগানো" $\rightarrow$ ব্যবহার করা |
| ১৫ | Orchestrate | Organize, run, coordinate | "সমন্বয় সাধন করা" $\rightarrow$ সাজানো / পরিচালনা করা |
| ১৬ | Intricate | Complex, detailed | "জটিল ও সূক্ষ্ম" $\rightarrow$ প্যাঁচালো / বিস্তারিত |
| ১৭ | Utilize | Use | "ব্যবহার করা" $\rightarrow$ কাজে লাগানো |
| ১৮ | Bespoke | Custom, tailored | "বিশেষভাবে প্রস্তুত" $\rightarrow$ নিজের মতো তৈরি |
| ১৯ | Synergy | Teamwork, combined effect | "সিনার্জি" $\rightarrow$ যৌথ লাভ / পারস্পরিক সুবিধা |
| ২০ | Paradigm | Model, standard | "প্যারাডাইম" $\rightarrow$ প্রচলিত ধারা / মডেল |
| ২১ | Paramount | Essential, primary | "সর্বোচ্চ গুরুত্ব" $\rightarrow$ সবচেয়ে জরুরি |
| ২২ | Cutting-edge | Modern, new, latest | "অত্যাধুনিক" $\rightarrow$ নতুন / আধুনিক |
| ২৩ | Game-changer | Major shift, big change | "গেম চেঞ্জার" $\rightarrow$ বড় পরিবর্তন |
| ২৪ | Navigate | Deal with, manage, handle | "পথ চলা / অতিক্রম করা" $\rightarrow$ সামলানো |
| ২৫ | Empower | Allow, let, enable | "ক্ষমতায়ন করা" $\rightarrow$ সুযোগ দেওয়া |
| ২৬ | Spearhead | Lead, drive | "নেতৃত্ব দেওয়া" $\rightarrow$ পরিচালনা করা |
| ২৭ | Revolutionize | Transform, reshape | "বিপ্লব ঘটানো" $\rightarrow$ আমূল বদলে দেওয়া |
| ২৮ | In conclusion / Ultimately | [Omit entirely] | "পরিশেষে বলা যায়..." $\rightarrow$ [সরাসরি কাজের কথা] |
| ২৯ | Indelible mark | Lasting impact | "চিরস্থায়ী দাগ" $\rightarrow$ গভীর প্রভাব |
| ৩০ | Quintessential | Classic, typical | "অনবদ্য উদাহরণ" $\rightarrow$ আসল উদাহরণ |
| ৩১ | Holistic | Complete, all-round | "সামগ্রিক দৃষ্টিভঙ্গি" $\rightarrow$ সব দিক মিলিয়ে |
| ৩২ | Plethora | Plenty, many | "প্রচুর আধিক্য" $\rightarrow$ অনেক / প্রচুর |
| ৩৩ | Myriad | Countless, many | "অগণিত" $\rightarrow$ অসংখ্য |
| ৩৪ | Catalyst | Trigger, driver | "অনুঘটক" $\rightarrow$ কারণ / প্রেরণা |
| ৩৫ | Underscore | Highlight, emphasize | "রেখাঙ্কিত করা" $\rightarrow$ তুলে ধরা / জোর দেওয়া |
| ৩৬ | Meticulous | Careful, thorough | "নিখুঁত ও যত্নবান" $\rightarrow$ খুঁটিনাটি দেখে কাজ করা |
| ৩৭ | Unprecedented | Rare, new, unique | "অভূতপূর্ব" $\rightarrow$ আগে দেখা যায়নি এমন |
| ৩৮ | Overarching | Main, primary | "সার্বিক" $\rightarrow$ প্রধান / মূল |
| ৩৯ | Streamline | Simplify, speed up | "গতিশীল করা" $\rightarrow$ সহজ করা |
| ৪০ | Resonate | Connect, appeal | "হৃদয়ে দোলা দেওয়া" $\rightarrow$ মনে ধরা / মানানসই হওয়া |
| ৪১ | Vibrant | Active, energetic | "প্রাণবন্ত ও স্পন্দনশীল" $\rightarrow$ সজীব / সক্রিয় |
| ৪২ | Cornerstone | Foundation, basis | "ভিত্তিপ্রস্তর" $\rightarrow$ মূলভিত্তি |
| ৪৩ | Dynamic | Active, changing | "গতিশীল" $\rightarrow$ পরিবর্তনশীল |

---

## 🚫 এআই লেখার ২১টি কাঠামোগত দুর্বলতা (The 21 Pattern Categories)

1. **ফাঁপা ইন্ট্রোডাকশন (Significance Inflation):** "বর্তমান দ্রুত পরিবর্তনশীল বিশ্বে..." বর্জন করে সরাসরি মূল প্রসঙ্গে আসা।
2. **অতিরিক্ত বোল্ড ও তালিকা নির্ভরতা (Listicle Overuse):** সাধারণ ২ লাইনের যুক্তি বোঝাতে অযৌক্তিক ১০-পয়েন্ট তালিকা না দেওয়া।
3. **ক্লান্তিকর হেজিং (Excessive Hedging):** "এটা হতে পারে, হয়তো বলা যায়, অনেকেই মনে করেন..." $\rightarrow$ আত্মবিশ্বাসী ও স্পষ্ট সুরে কথা বলা।
4. **ট্রানজিশন ক্লিশে (Transition Addiction):** "Moreover, Furthermore, In addition to this..." বাদ দেওয়া।
5. **জেনারিক কনক্লুশন (Generic Conclusions):** শেষে এসে "সর্বোপরি বলা যায় এআই এবং মানুষের মেলবন্ধন এক নতুন দিগন্ত উন্মোচন করবে"—এই ধরনের ফাঁপা নীতিকথা সম্পূর্ণ বাদ দেওয়া।

---

## 🔍 ৪-ধাপের অডিট প্রোটোকল (The 4-Pass Audit)

লেখার পর এই ৪টি ধাপে স্বয়ংক্রিয়ভাবে অডিট সম্পন্ন করতে হবে:
1. **পাস ১ (AI-ism Search):** উপরের ৪৩টি শব্দের তালিকা বা তাদের বাংলা ক্লিশে রূপ আছে কি না স্ক্যান করা।
2. **পাস ২ (Staccato Cadence Check):** সব বাক্য একই দৈর্ঘ্যের কি না পরীক্ষা করা (ছোট ও বড় বাক্যের স্বাভাবিক রিদম আনা)।
3. **পাস ৩ (Cut the Fluff):** কোনো বাক্য না থাকলে লেখার মানের কোনো ক্ষতি হয় কি না দেখে অপ্রয়োজনীয় বাক্য মুছে ফেলা।
4. **পাস ৪ (Human Resonance QA):** লেখাটি পড়ে মনে হচ্ছে কি একজন রক্ত-মাংসের স্পষ্টভাষী মানুষ কথা বলছে? উত্তর হ্যাঁ হলে ডেলিভার করা।
