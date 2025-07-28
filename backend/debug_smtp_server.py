import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.policy import default

class DebugHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message received:')
        
        msg = message_from_bytes(envelope.content, policy=default)
        
        print(f"Subject: {msg['Subject']}")
        print(f"From: {msg['From']}")
        print(f"To: {msg['To']}\n")
        
        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                content_disposition = part.get_content_disposition()
                
                if content_disposition == 'attachment':
                    filename = part.get_filename()
                    payload = part.get_payload(decode=True)
                    if filename and filename.lower().endswith('.pdf'):
                        print(f"[Attachment detected] PDF: {filename}, size: {len(payload)} bytes")
                    else:
                        print(f"[Attachment detected] Non-PDF or unknown filename: {filename}")
                
                elif content_type == 'text/plain':
                    print("Body (text/plain):")
                    print(part.get_content())
                    print()
                
                elif content_type == 'text/html':
                    print("Body (text/html):")
                    print(part.get_content())
                    print()
        
        else:
            print("Body:")
            print(msg.get_content())
        
        print('End of message\n')
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    controller = Controller(DebugHandler(), hostname='localhost', port=1025)
    controller.start()
    print("Debug SMTP server running on localhost:1025. Press Ctrl+C to quit.")
    try:
        asyncio.run(asyncio.Event().wait())
    except KeyboardInterrupt:
        pass
