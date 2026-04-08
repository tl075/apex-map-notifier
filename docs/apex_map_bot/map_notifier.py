import os
import requests
import datetime

def get_map_rotation(api_key):
    url = f"https://api.mozambiquehe.al/maprotation?auth={api_key}&version=2"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def send_to_discord(webhook_url, embed):
    data = {"username": "Apexランクマップ通知", "embeds": [embed]}
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Discord Error: {e}")

def main():
    api_key = os.getenv("APEX_API_KEY")
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not api_key or not webhook_url: return
    data = get_map_rotation(api_key)
    if not data: return
    ranked = data.get("ranked", {}).get("current", {})
    br = data.get("battle_royale", {}).get("current", {})
    mixtape = data.get("ltm", {}).get("current", {})
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    time_str = now.strftime("%Y/%m/%d %H:%M")
    embed = {
        "title": "🏆 Apex Legends マップローテーション",
        "description": f"現在のマップ情報 ({time_str} JST)",
        "color": 15158332,
        "fields": [
            {"name": "🔴 ランクマッチ", "value": f"**{ranked.get('map', '不明')}**\n残り: `{ranked.get('remainingTimer', '--:--')}`"},
            {"name": "⚪ カジュアル (BR)", "value": f"**{br.get('map', '不明')}**", "inline": True},
            {"name": "🔵 ミックステープ", "value": f"**{mixtape.get('map', '不明')}**", "inline": True}
        ],
        "footer": {"text": "Data provided by Apex Legends Status"}
    }
    send_to_discord(webhook_url, embed)

if __name__ == "__main__":
    main()
