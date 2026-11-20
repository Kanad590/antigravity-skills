---
name: indian-puppet-animation
description: >-
  Create viral 2D Indian Cutout Puppet / Kathputli animation reels in the style of Project Chanakya,
  Pattachitra, and Shadow Puppets. Features procedural parchment background, joint-rivet puppet rigging
  with thin control rods, glowing carnival bulb counter badges, Edge-TTS/Piper neural voiceovers,
  and word-by-word synced subtitles rendered at 1,700+ fps with zero GPU/CPU lag.
risk: safe
source: local
---

# 🎭 Indian Cutout Puppet Animation Skill (ভারতীয় কাঠপুতলি ও চাণক্য পাপেট শৈলী)

এই স্কিলটি ব্যবহার করে ইনস্টাগ্রাম ও ইউটিউব শর্টসের ভাইরাল **চাণক্য নীতি ও ভারতীয় পৌরাণিক কাঠপুতলি / শ্যাডো পাপেট শৈলী (2D Cutout Puppet)** তৈরি করা যায়।

---

## ⚡ মূল আর্কিটেকচার ও উপাদানসমূহ (Core Components)

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. ভিন্টেজ তালপাতার ব্যাকগ্রাউন্ড (Aged Papyrus / Parchment Canvas)│
│ 2. টপ UI ও কার্নিভাল বাল্ব প্লাক (SOME SAY: BITTER TRUTH)          │
│ 3. ডায়নামিক ব্যাজ কাউন্টার (14, 15, 16, 17 - পয়েন্ট অনুযায়ী আলো)   │
│ 4. পাপেট চরিত্র (চাণক্য ও শিষ্য - জয়েন্টে সাদা রিভেট ও কাঠি)        │
│ 5. সিঙ্ক করা ভয়েসওভার ও সাবটাইটেল (Edge-TTS + Karaoke Caption)    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ প্রডাকশন পাইপলাইন ও স্ক্রিপ্টস (Production Workflow)

### ১. ক্যারেক্টার কাটআউট ও রিগিং:
* চরিত্রগুলোকে স্বচ্ছ ব্যাকগ্রাউন্ডে (`RGBA`) মাথা, ধড় এবং হাত-পা আলাদা করে রাখা হয়।
* প্রতিটি জয়েন্টে সাদা বৃত্তাকার পিভট ডট (White Rivet Pin) থাকে।
* পায়ের নিচ থেকে সোজা নিচের দিকে একটি পাতলা কন্ট্রোল রড (`width=2, color=(95, 75, 55)`) আঁকা হয়।

### ২. কথা বলার সাথে মোশন:
* **মাথা নোয়ানো (Head Nod):** `angle = 3.5 * math.sin(t * 7.5)` ডিগ্রিতে ঘাড়ের পিভট বিন্দু অনুযায়ী রোটেট হয়।
* **শরীরের শ্বাসের ওঠানামা (Breathing Sway):** `y = base_y + 3.0 * math.sin(t * 3.5)`।
* **সফট ড্রপ শ্যাডো:** ক্যারেক্টারের পেছনে ১২ পিক্সেল বামে এবং ৬ পিক্সেল নিচে ২৮% অপাসিটিতে ব্লার শ্যাডো দেওয়া হয়।

### ৩. অডিও ও ভয়েসওভার:
* **ভয়েস:** `edge-tts --voice "hi-IN-MadhurNeural" --pitch="-5Hz" --rate="-4%"` দিয়ে গম্ভীর প্রাচীন ঋষির কণ্ঠ তৈরি।
* **অ্যাম্বিয়েন্স:** প্রাচীন তম্বুরার সুর (D/Sa Harmonic Drone - 146.8Hz, 220Hz, 293.6Hz) -18dB-তে ব্যাকগ্রাউন্ডে মিক্স করা।
* **হুক SFX:** 0.0 সেকেন্ডে একটি ভারী ড্রাম বা মন্দিরের ঘণ্টার আওয়াজ (Bell Hit)।

### ৪. রেন্ডারিং স্পিড:
* পাইথন + Pillow + FFmpeg পাইপ দিয়ে 720×1280 রেজোলিউশনে প্রতি সেকেন্ডে ১,৭০০ ফ্রেম রেন্ডার হয়।
* ২০ সেকেন্ডের পুরো রিল মাত্র ১০-১৫ সেকেন্ডের মধ্যে সম্পূর্ণ রেন্ডার হয়ে যায়।

---

## 📁 রেফারেন্স প্রজেক্ট ফাইল:
* স্যাম্পল স্ক্রিপ্ট ও রেন্ডারার: `/home/saman/Antigravity/Projects/ai_reels_study/chanakya_reel/render_chanakya_reel.py`
* ফাইনাল রিল: `/home/saman/Antigravity/Projects/ai_reels_study/chanakya_reel/chanakya_puppet_reel.mp4`
