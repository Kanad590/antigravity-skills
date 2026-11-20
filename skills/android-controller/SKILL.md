---
name: android-controller
description: >-
  Use this skill whenever the user asks to control, automate, mirror, type, tap,
  inspect, take screenshots of, or manage Android mobile devices (specifically
  Motorola Edge 50, Redmi 4, or any Android smartphone over USB or Wi-Fi).
  Provides native ADB automation, wireless debugging pairing (Android 11+),
  MIUI security bypass guide for Redmi 4, UI hierarchy dumping, and scrcpy
  live desktop mirroring with dedicated AMD GPU acceleration.
---

# 📱 Android Mobile Controller (Motorola Edge 50 & Redmi 4)

এই স্কিলটি Antigravity-কে ব্যবহারকারীর **Motorola Edge 50** এবং **Redmi 4** (বা যেকোনো অ্যান্ড্রয়েড ফোন) ইউএসবি বা ওয়াইফাইয়ের মাধ্যমে সম্পূর্ণ নিয়ন্ত্রণ, স্ক্রিন মিররিং, টাচ অটোমেশন, টেক্সট টাইপিং, স্ক্রিনশট এবং অ্যাপ ম্যানেজ করার ক্ষমতা দেয়।

---

## 🛠️ সিস্টেমের টুলস ও MCP সার্ভার

সিস্টেমে দুটি শক্তিশালী MCP সার্ভার কনফিগার করা আছে:
1. **`android-control` (`~/.local/bin/android-control-mcp.py`):** ১৭টি উচ্চ-ক্ষমতাসম্পন্ন ডেডিকেটেড টুল (টাচ, সোয়াইপ, টাইপিং, কি-প্রেস, UI ইন্সপেকশন, স্ক্রিনশট, ওয়াইফাই পেয়ারিং, ও Scrcpy লাইভ মিররিং)।
2. **`adb` (`npx -y adb-mcp`):** স্ট্যান্ডার্ড প্যাকেজ ম্যানেজার, লগক্যাট ও লো-লেভেল অ্যাক্টিভিটি ম্যানেজার।

---

## 📲 ডিভাইস সেটআপ ও প্রাথমিক প্রস্তুতি (Device Onboarding Guide)

### ১. 📱 Motorola Edge 50 (Android 14 / 15 Hello UI)

মটোরোলা এজ ৫০ একটি আধুনিক ফোন। এটি **USB তার ছাড়াও সম্পূর্ণ তারবিহীনভাবে (Wireless Debugging)** নিয়ন্ত্রণ করা যায়।

#### সেটআপ ধাপ:
1. **Developer Options চালু করুন:**
   * ফোনের **Settings** > **About phone**-এ যান।
   * নিচে স্ক্রোল করে **"Build number"**-এর ওপর পরপর ৭ বার ট্যাপ করুন (লক স্ক্রিনের পিন দিন)।
2. **USB Debugging চালু করুন:**
   * **Settings** > **System** > **Developer options**-এ যান।
   * **"USB debugging"** অন করুন।
3. **তারবিহীন নিয়ন্ত্রণ (Wireless Debugging - তার ছাড়া চালাতে চাইলে):**
   * কম্পিউটার ও ফোনকে একই ওয়াইফাই বা হটস্পটে কানেক্ট করুন।
   * **Developer options**-এর ভেতর **"Wireless debugging"** অন করুন।
   * তার ওপর ট্যাপ করে ভেতরে ঢুকুন এবং **"Pair device with pairing code"**-এ চাপ দিন।
   * সেখানে একটি **IP Address & Port** এবং **৬ সংখ্যার Pairing Code** দেখতে পাবেন।
   * Antigravity দিয়ে সোজা চালান:
     ```bash
     adb pair <ip>:<port> <pairing_code>
     ```
   * পেয়ার হয়ে গেলে মূল পেজের IP ও Port দেখে চালান:
     ```bash
     adb connect <ip>:<port>
     ```

---

### ২. 📱 Redmi 4 (Xiaomi / MIUI 10/11)

রেডমি ৪-এ MIUI সিস্টেম থাকার কারণে শাওমি কিছু বিশেষ সিকিউরিটি লক দিয়ে রাখে। এটি না খুললে কোনো টাচ বা অটোমেশন কাজ করবে না।

#### সেটআপ ধাপ:
1. **Developer Options চালু করুন:**
   * **Settings** > **About phone**-এ যান।
   * **"MIUI version"**-এর ওপর পরপর ৭ বার ট্যাপ করুন।
2. **Developer Options-এ ৩টি জরুরি সুইচ (সবচেয়ে গুরুত্বপূর্ণ):**
   * **Settings** > **Additional settings** > **Developer options**-এ যান।
   * ✅ **"USB debugging"** -> ON করুন।
   * ⚠️ **"Install via USB"** -> ON করুন।
   * 🚨 **"USB debugging (Security settings)"** -> **বাধ্যতামূলকভাবে ON করুন!**
     *(এটি অন করার সময় শাওমি ৩ বার ৫ সেকেন্ড করে ওয়ার্নিং দেবে, প্রতিবার 'Next' ও 'Accept' করুন। এটি অন না থাকলে মাউস ক্লিক বা টাচ কাজ করবে না।)*
3. কম্পিউটার ও ফোনে USB তার লাগান এবং ফোনের স্ক্রিনে **"Always allow from this computer"** বক্সে টিক মেরে **OK** করুন।

---

## 🎮 Antigravity দিয়ে মোবাইল নিয়ন্ত্রণের প্রধান কমান্ড ও টুলস

### ১. কানেক্টেড মোবাইল তালিকা দেখা:
```bash
adb devices -l
```
*(বা MCP টুল: `android_list_devices`)*

### ২. ডেস্কটপে ফোনের লাইভ স্ক্রিন খোলা (Scrcpy + AMD GPU):
কম্পিউটারের স্ক্রিনে সরাসরি মোবাইল ভেসে উঠবে এবং মাউস-কীবোর্ড দিয়ে ব্যবহার করা যাবে:
```bash
DRI_PRIME=1 scrcpy -s <device_serial> --window-title "Mobile Control"
```
*(বা MCP টুল: `android_scrcpy`)*

### ৩. স্ক্রিনশট নেওয়া:
```bash
adb -s <device_serial> exec-out screencap -p > /home/saman/phone_screen.png
```
*(বা MCP টুল: `android_screenshot`)*

### ৪. টাচ ও জেসচার অটোমেশন:
* **ট্যাপ করা (Click):** `adb shell input tap 500 1200` *(বা MCP: `android_tap(500, 1200)`)*
* **সোয়াইপ / স্ক্রোল করা:** `adb shell input swipe 500 1500 500 500 300` *(বা MCP: `android_swipe`)*
* **টেক্সট টাইপ করা:** `adb shell input text 'Hello'` *(বা MCP: `android_type`)*
* **হোম বা ব্যাক বাটন:** `adb shell input keyevent 3` (Home) বা `4` (Back) *(বা MCP: `android_press_key`)*

### ৫. যেকোনো অ্যাপ সরাসরি চালু করা:
```bash
adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1
```
*(বা MCP টুল: `android_open_app("whatsapp")` বা `android_open_app("youtube")`)*

---

## 🔍 স্ক্রিনের বোতাম ও এলিমেন্ট চিহ্নিত করা (UI Inspection)

স্ক্রিনে কোন বোতাম কোথায় আছে না জেনেও স্বয়ংক্রিয়ভাবে খুঁজে পেতে:
```bash
adb shell uiautomator dump /data/local/tmp/uidump.xml && adb shell cat /data/local/tmp/uidump.xml
```
*(বা MCP টুল: `android_inspect_ui`)*

---

## ⚡ বিশেষ শর্টকাট (Scrcpy Keyboard Shortcuts)

কম্পিউটারে Scrcpy উইন্ডো খোলা অবস্থায়:
* **Alt + h:** Home বাটন
* **Alt + b:** Back বাটন
* **Alt + s:** App Switcher (রিসেন্ট অ্যাপস)
* **Alt + p:** Power বাটন (অন/অফ)
* **Alt + Up / Down:** ভলিউম বাড়ানো / কমানো
* **Alt + f:** ফুল স্ক্রিন মোড
* **কম্পিউটার থেকে যেকোনো ফাইল/APK ড্র্যাগ অ্যান্ড ড্রপ:** সরাসরি ফোনে কপি ও ইনস্টল হবে!
