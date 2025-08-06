#onlyrootles
#mt manager
import base64
import requests
import subprocess
import os

print("ожидайте...")

ENCRYPTED_KEY_B64 = "ZGxfRHZcZ0ZXZhBMb1xuYRJwVEhDQktqT1UcS2hsQ3FRc1ZfQkZO==" 
XOR_KEY = 37  

def decrypt_key(encoded_key, xor_key):
    encrypted_bytes = base64.b64decode(encoded_key)
    return ''.join([chr(b ^ xor_key) for b in encrypted_bytes])

GEMINI_API_KEY = decrypt_key(ENCRYPTED_KEY_B64, XOR_KEY)


def get_device_info():
    try:
        cpu = subprocess.check_output(["adb", "shell", "cat", "/proc/cpuinfo"]).decode()
        mem = subprocess.check_output(["adb", "shell", "free", "-h"]).decode()
        android_ver = subprocess.check_output(["adb", "shell", "getprop", "ro.build.version.release"]).decode().strip()
        device = subprocess.check_output(["adb", "shell", "getprop", "ro.product.model"]).decode().strip()
        root_status = subprocess.check_output(["adb", "shell", "id"]).decode()

        return f"""
🐠DEVICE: {device}
👁ndroid Version: {android_ver}
🠠CPU Info:
{cpu}
💾 Memory:
{mem}
🐠 Root Status:
{root_status}
"""
    except Exception as e:
        return f" failee!: {e}"


os.makedirs("logs", exist_ok=True)
log_text = get_device_info()
with open("logs/diagnostic_log.txt", "w", encoding="utf-8") as f:
    f.write(log_text)


headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": GEMINI_API_KEY
}


example_script = """
#!/system/bin/sh

LOG="/sdcard/fps_boost_log.txt"
echo "🚀 FPS BOOSTER v2 STARTED" > $LOG

# Проверка root
if [ "$(id -u)" -ne 0 ]; then
  echo "❌ root root!" >> $LOG
  exit 1
fi


echo "📊 BEFORE:" >> $LOG
echo "Memory:" >> $LOG
free -h >> $LOG
echo "---" >> $LOG
top -n 1 -m 5 | grep -v idle >> $LOG

### === 2. Очистка памяти и фона ===
echo "🧹 Cleaning..." >> $LOG
sync; echo 3 > /proc/sys/vm/drop_caches
killall -9 com.miui.analytics com.xiaomi.finddevice com.miui.msa.global >/dev/null 2>&1
echo "✅ RAM Cleared" >> $LOG

### === 3. GPU Performance режим ===
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
  echo "performance" > $cpu/cpufreq/scaling_governor 2>/dev/null
done
echo "✅ CPU governor set" >> $LOG

### === 4. Thermal блокировка ===
if [ -f /sys/class/thermal/thermal_message/sconfig ]; then
  echo "disabled" > /sys/class/thermal/thermal_message/sconfig
  echo "✅ Thermal control off" >> $LOG
fi

### === 5. Двойной SWAP: 520МБ + 956МБ ===
echo "💾 Setting up SWAP..." >> $LOG
SWAP1="/data/swap1"
SWAP2="/data/swap2"

[ ! -f "$SWAP1" ] && dd if=/dev/zero of=$SWAP1 bs=1M count=520 && mkswap $SWAP1
[ ! -f "$SWAP2" ] && dd if=/dev/zero of=$SWAP2 bs=1M count=956 && mkswap $SWAP2

swapon $SWAP1
swapon $SWAP2
echo "✅ SWAP active" >> $LOG

### === 6. Графические твики: фильтры, рендер, anti-alias ===
setprop debug.hwui.disable_scissor_opt true
setprop debug.hwui.renderer opengl
setprop debug.egl.swapinterval 0
setprop persist.sys.ui.hw true
setprop persist.sys.render_type opengles2
setprop ro.opengles.version 131072  # = 2.0

echo "✅ Графические фильтры OFF, OpenGL 2.0 включён" >> $LOG

### === 7. Чистка кэша браузеров и игр ===
rm -rf /data/data/com.android.chrome/cache/*
rm -rf /data/data/org.mozilla.firefox/cache/*
rm -rf /data/data/net.kdt.pojavlaunch/cache/*
echo "✅ Game/browser cache cleared" >> $LOG

### === 8. I/O ускорение и MIP OFF (символически) ===
echo 128 > /sys/block/mmcblk0/queue/read_ahead_kb 2>/dev/null
echo noop > /sys/block/mmcblk0/queue/scheduler 2>/dev/null

### === 9. ПОСЛЕ ===
echo "\n📈 AFTER:" >> $LOG
echo "Memory:" >> $LOG
free -h >> $LOG
echo "---" >> $LOG
top -n 1 -m 5 | grep -v idle >> $LOG

echo "\n✅ BOOST COMPLETE!" >> $LOG
cat $LOG
"""


prompt = f"""
Ты — специалист по root-оптимизации Android. Сгенерируй только рабочий .sh скрипт для FPS Boost, Game Mode, SWAP, RAM очистки, thermal tweak и GPU ускорения.  
Никаких пояснений, только .sh код. Без markdown, без комментариев ИИ.  
Следуй стилю этого скрипта:
{example_script}

📊 Диагностика устройства:
{log_text}
"""

# ✉️ Тело запроса
payload = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    headers=headers,
    json=payload
)

if response.status_code != 200:
    print("❌ Ошибка Gemini:", response.status_code)
    print(response.text)
    exit()

sh_code = response.json()["candidates"][0]["content"]["parts"][0]["text"]
os.makedirs("results", exist_ok=True)
with open("results/auto_boost.sh", "w", encoding="utf-8") as f:
    f.write(sh_code)

print(" Скрипт сохранён/script saved: results/auto_boost.sh")
