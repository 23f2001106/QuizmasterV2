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

        def process_part(part, level=0):
            indent = "  " * level
            content_type = part.get_content_type()
            content_disposition = part.get_content_disposition()

            if part.is_multipart():
                for subpart in part.iter_parts():
                    process_part(subpart, level + 1)
            else:
                if content_disposition == 'attachment':
                    filename = part.get_filename()
                    payload = part.get_payload(decode=True)
                    if filename and filename.lower().endswith('.pdf'):
                        print(f"{indent}[Attachment detected] PDF: {filename}, size: {len(payload)} bytes")
                    else:
                        print(f"{indent}[Attachment detected] Non-PDF or unknown filename: {filename}")
                elif content_type == 'text/plain':
                    print(f"{indent}Body (text/plain):")
                    print(indent + part.get_content().replace("\n", f"\n{indent}"))
                    print()
                elif content_type == 'text/html':
                    print(f"{indent}Body (text/html):")
                    print(indent + part.get_content().replace("\n", f"\n{indent}"))
                    print()

        if msg.is_multipart():
            process_part(msg)
        else:
            print("Body:")
            print(msg.get_content())

        print('End of message\n')
        return '250 Message accepted for delivery'


# Start the SMTP server
if __name__ == '__main__':
    controller = Controller(DebugHandler(), hostname='localhost', port=1025)
    controller.start()
    print("Debug SMTP server running on localhost:1025. Press Ctrl+C to quit.")
    try:
        asyncio.run(asyncio.Event().wait())
    except KeyboardInterrupt:
        print("SMTP server stopped.")

