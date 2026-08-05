from imap_tools import AND, MailMessageFlags
from src.utils import FOLDER_NAMES
from .base_cleaner import BaseFolderCleaner
from .helpers.security.deep_scanner import DeepScanner


class BombSquadFolderCleaner(BaseFolderCleaner):
    def __init__(self, thread_name, folder_name, stopper, record, imap_data, vt_groq_data, queue_update):
        super().__init__(thread_name, folder_name, stopper, record, imap_data)

        self.vt_groq_data = vt_groq_data or {}
        self.queue_update = queue_update
        self.scanner = DeepScanner(logger=self.record)

    def _bucking(self, mailbox):
        categories = {"malevolent": [], "clean": []}

        try:
            messages = list(mailbox.fetch(AND(all=True)))
        except Exception as e:
            self.record.write(f"Error fetching emails: {e}")
            return categories

        for msg in messages:
            if self.stopper.is_set():
                break
            if not msg.attachments:
                categories["clean"].append(msg)
                continue

            is_malevolent = False
            for att in msg.attachments:
                is_bad, reason = self.scanner.analyze(att)
                if is_bad:
                    self.record.write(f"Threat Detected: {reason} from {msg.from_}.")
                    is_malevolent = True
                    break

            if is_malevolent:
                categories["malevolent"].append(msg)
            else:
                categories["clean"].append(msg)

        return categories
    # ========== ========== ==========


    def _applying(self, mailbox, categories):
        if not categories:
            return

        # Handle malevolent emails
        malevolent_msgs = categories.get("malevolent", [])
        if malevolent_msgs:
            for msg in malevolent_msgs:
                self.queue_update.put({"action": "add_blacklist", "value": msg.from_})
                self.record.write(f"Blacklist: Sender {msg.from_} added to blacklist.")

            try:
                mailbox.move([msg.uid for msg in malevolent_msgs], FOLDER_NAMES["bin"])
            except Exception as e:
                self.record.write(f"Error moving to trash: {e}")

        # Restore clean emails back to Inbox
        clean_msgs = categories.get("clean", [])
        if clean_msgs:
            for msg in clean_msgs:
                self.queue_update.put({"action": "add_graylist", "value": msg.from_})
                self.record.write(f"Restore: Restoring email from {msg.from_} to inbox.")

            try:
                mailbox.flag(uids, [MailMessageFlags.SEEN], True)
                mailbox.move(uids, FOLDER_NAMES["inbox"])
            except Exception as e:
                self.record.write(f"Error restoring to inbox: {e}")
