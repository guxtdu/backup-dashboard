# 📦 Backup Dashboard – Docker & Mailversand

Ein vollständiges Web-Dashboard für tägliche Proxmox-Backups mit:

- Kundenübersicht
- HTML-Reports
- Uploadschutz (Token + IP)
- E-Mail-Versand der Tagesreports
- Adminpanel mit IP, Kundennummer und Mail

## 🚀 Start

```bash
cp .env.example .env
docker-compose up -d
```

## 📩 E-Mail-Versand

Täglicher Versand an hinterlegte Adresse:
```bash
python send-report-mails.py
```

## 🛠 Cron-Vorschläge

```cron
0 8 * * * python3 /opt/backup-upload/json-export.py
10 8 * * * python3 /opt/backup-upload/upload.py
15 8 * * * python3 /opt/backup-dashboard/send-report-mails.py
```
