from telethon import TelegramClient, events
import asyncio

# Thay thế bằng thông tin của bạn
api_id = '27189205'  # Thay thế bằng API ID của bạn
api_hash = '1099f4f2d011b3001707dfd2ad1ae454'  # Thay thế bằng API Hash của bạn
phone = '+84789500627'  # Số điện thoại của bạn
source_channel = -1001786511698  # ID của kênh nguồn
destination_channel = '@congkhaiii'  # ID của kênh đích

# Khởi tạo client
client = TelegramClient('session_autocopy', api_id, api_hash)


async def get_existing_file_ids(channel):
    """Lấy tất cả file_id từ kênh đích cho các media (video và photo)."""
    existing_file_ids = set()

    async for message in client.iter_messages(channel):
        if message.media:
            if hasattr(message.media, 'photo'):  # Kiểm tra nếu là ảnh
                existing_file_ids.add(message.media.photo.id)
            elif hasattr(message.media, 'document'):
                if message.media.document.mime_type.startswith('video/'):  # Kiểm tra nếu là video
                    existing_file_ids.add(message.media.document.id)
                elif message.media.document.mime_type.startswith('image/'):  # Kiểm tra nếu là ảnh
                    existing_file_ids.add(message.media.document.id)

    return existing_file_ids


@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    # Lấy tin nhắn mới
    message = event.message

    if message.media:
        file_id = None

        if hasattr(message.media, 'photo'):  # Nếu tin nhắn là ảnh
            file_id = message.media.photo.id
        elif hasattr(message.media, 'document'):  # Kiểm tra nếu là video hoặc ảnh
            if message.media.document.mime_type.startswith('video/'):
                file_id = message.media.document.id
            elif message.media.document.mime_type.startswith('image/'):
                file_id = message.media.document.id

        # Kiểm tra xem file_id đã có trong kênh đích chưa
        if file_id and file_id not in existing_file_ids:
            # Gửi tin nhắn đến kênh đích
            await client.send_message(destination_channel, message)
            print(f"Đã sao chép tin nhắn ID {message.id} từ {source_channel} sang {destination_channel}")
        elif file_id:
            print(f"Tin nhắn với file_id {file_id} đã tồn tại trong kênh đích, bỏ qua.")


async def main():
    await client.start()
    print("Bot đã khởi động và đang lắng nghe tin nhắn mới...")

    # Lấy các file_id đã có trong kênh đích
    global existing_file_ids
    existing_file_ids = await get_existing_file_ids(destination_channel)

    try:
        await client.run_until_disconnected()  # Chạy cho đến khi ngắt kết nối
    except KeyboardInterrupt:
        print("Chương trình đã dừng.")
    finally:
        await client.disconnect()  # Ngắt kết nối client


if __name__ == "__main__":
    asyncio.run(main())
