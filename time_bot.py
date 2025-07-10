from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, functions
import asyncio
import datetime
import pytz

api_id = 26865532
api_hash = '4db5fd680068290104076d1e80511638'

client = TelegramClient('mohammad_session', api_id, api_hash)

def to_digital_font(text):
    digits_map = {
        '０': '𝟶',
        '１': '𝟷',
        '２': '𝟸',
        '３': '𝟹',
        '４': '𝟺',
        '５': '𝟻',
        '６': '𝟼',
        '７': '𝟽',
        '８': '𝟾',
        '９': '𝟿',
        '：': ':'
    }
    return ''.join(digits_map.get(c, c) for c in text)

def create_profile_pic_with_time(base_image_path, output_path, time_text):
    img = Image.open(base_image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype('digital-7.ttf', 50)

    width, height = img.size
    bbox = draw.textbbox((0, 0), time_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = height - text_height - 20

    draw.text((x, y), time_text, font=font, fill=(255, 255, 255, 255))

    img = img.convert('RGB')
    img = img.resize((512, 512))

    img.save(output_path)

def get_iran_time():
    tehran = pytz.timezone("Asia/Tehran")
    return datetime.datetime.now(tehran)

async def sleep_until_next_minute():
    now = get_iran_time()
    seconds = 60 - now.second
    await asyncio.sleep(seconds)

async def update_forever():
    await client.start()

    base_image = 'base.jpg' 
    while True:
        now = get_iran_time()
        time_str = now.strftime('%H:%M')
        digital_time = to_digital_font(time_str)

        output_image = f'profile_with_time_{now.strftime("%H%M")}.jpg'

        create_profile_pic_with_time(base_image, output_image, digital_time)

        try:
            file = await client.upload_file(output_image)
            await client(functions.photos.UploadProfilePhotoRequest(photo=file))
            print(f'✅ عکس پروفایل آپدیت شد: {time_str}')
        except Exception as e:
            print(f'❌ خطا در آپدیت عکس پروفایل: {e}')

        fancy_name = f'MOHAMMAD | {digital_time}'
        fancy_bio = f'دیگه پسر خوبی شدم :) | {digital_time}'

        try:
            await client(functions.account.UpdateProfileRequest(
                first_name=fancy_name,
                about=fancy_bio
            ))
            print(f"✅ آپدیت شد → {fancy_name}")
        except Exception as e:
            print(f"❌ خطا: {e}")

        await sleep_until_next_minute()

async def main():
    await client.start()
    await update_forever()

with client:
    client.loop.run_until_complete(main())
