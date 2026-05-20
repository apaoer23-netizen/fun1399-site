#!/usr/bin/env python3
"""
Send backup files via email
- Tries to attach files if small enough
- Falls back to download paths if too large
"""

import os
import sys
import subprocess
from datetime import datetime

# Configuration
RECIPIENT = "yux0468@gmail.com"
BACKUP_DIR = "/root/.openclaw/backups"
MAX_ATTACHMENT_MB = 20  # Maximum attachment size in MB

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def create_email_body(date_str, files_info, download_paths):
    """Create email body"""
    body = f"""【fun1399備份】網站+系統備份 - {date_str[:4]}/{date_str[4:6]}/{date_str[6:]}

備份時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

檔案清單：
"""
    for name, size, status in files_info:
        body += f"  - {name} ({size}) - {status}\n"
    
    body += "\n下載路徑：\n"
    for path in download_paths:
        body += f"  - {path}\n"
    
    body += "\n━━━━━━━━━━━━━━━\n備份由 OpenClaw 自動生成\n"
    return body

def send_email_with_msmtp(subject, body, attachments=None):
    """Send email using msmtp directly"""
    from_email = "jie9997777@gmail.com"
    to_email = RECIPIENT
    
    # Build MIME email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    import mimetypes
    from email import encoders
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    # Attach body
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Attach files if any
    if attachments:
        for filepath in attachments:
            filename = os.path.basename(filepath)
            
            # Guess MIME type
            ctype, encoding = mimetypes.guess_type(filepath)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            
            with open(filepath, 'rb') as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(part)
    
    # Send via msmtp
    try:
        proc = subprocess.Popen(
            ['msmtp', '--read-envelope-from', '--read-recipients', to_email],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(input=msg.as_bytes())
        
        if proc.returncode == 0:
            return True
        else:
            print(f"msmtp stderr: {stderr.decode()}")
            return False
    except Exception as e:
        print(f"Email send error: {e}")
        return False

def main():
    date_str = datetime.now().strftime('%Y%m%d')
    
    # Files to potentially send
    website_backup = os.path.join(BACKUP_DIR, f"fun1399-backup-{date_str}.zip")
    system_backup = os.path.join(BACKUP_DIR, f"openclaw-backup-{date_str}.zip")
    
    files_to_check = [
        ("fun1399 網站備份", website_backup),
        ("OpenClaw 系統備份", system_backup),
    ]
    
    files_info = []
    attachments = []
    download_paths = []
    
    for name, filepath in files_to_check:
        if os.path.exists(filepath):
            size_mb = get_file_size_mb(filepath)
            size_str = f"{size_mb:.1f}MB"
            
            if size_mb <= MAX_ATTACHMENT_MB:
                attachments.append(filepath)
                files_info.append((name, size_str, "✅ 已附加"))
            else:
                files_info.append((name, size_str, "⚠️ 檔案過大，請手動下載"))
            
            download_paths.append(filepath)
        else:
            files_info.append((name, "N/A", "❌ 檔案不存在"))
    
    # Create email
    date_display = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
    subject = f"【fun1399備份】網站+系統備份 - {date_display}"
    body = create_email_body(date_str, files_info, download_paths)
    
    # Send email
    success = send_email_with_msmtp(subject, body, attachments if attachments else None)
    
    if success:
        print(f"✅ Email sent successfully to {RECIPIENT}")
        print(f"   Subject: {subject}")
        print(f"   Attachments: {len(attachments)} file(s)")
        for att in attachments:
            print(f"     - {os.path.basename(att)}")
    else:
        print(f"❌ Failed to send email to {RECIPIENT}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
