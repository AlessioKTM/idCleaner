B_EXT_WIN = (".exe", ".bat", ".js", ".vbs", ".src", ".xlsm")
B_EXT_LIN = (".sh", ".bash", ".py", ".desktop", ".run", ".bin", ".pl", ".rb")
BAD_EXT = B_EXT_WIN + B_EXT_LIN

S_EXT_WIN = (
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".rar", ".7z",
    ".iso", ".img", ".cab"
)
S_EXT_LIN = (
    ".pdf", ".odt", ".ods", ".odp",
    ".tar.gz", ".tar.xz", ".tar.bz2", ".gz"
)
SUSPICIOUS_EXT = S_EXT_WIN + S_EXT_LIN

TRACKING_PARAMS = ["user=", "id=", "track=", "open=", "campaign="]
PROMOTIONAL_PARAMS = ["list-unsubscribe", "x-campaign", "x-campaignid", "x-mailchimp-campaign"]
UNSUBSCRIBE_PARAMS = [r'unsubscribe', r'disiscriviti', r'cancella iscrizione', r'preferenze di invio', r'visualizza nel browser']  # Italian + English

HIGH_RISK_KEYWORDS = {
    # Italian
    "urgente": 15, "azione richiesta": 20, "conto bloccato": 25,
    "sospeso": 20, "cripto": 15, "bitcoin": 15, "investimento": 10,
    "eredità": 30, "vincita": 25, "lotteria": 25, "portafoglio": 10,
    "verifica identità": 25, "scadenza": 15, "rinnovo": 10,

    # English
    "urgent": 15, "action required": 20, "account blocked": 25,
    "suspended": 20, "crypto": 15, "investment": 10,
    "inheritance": 30, "winnings": 25, "lottery": 25, "wallet": 10,
    "verify identity": 25, "expiration": 15, "renewal": 10
}
URL_SHORTENERS = ["bit.ly", "goo.gl", "tinyurl.com", "t.co", "is.gd"]

GROQ_SECURITY_SYSTEM_PROMPT = (
    "You are an enterprise email security analyst. Minimize false positives.\n"
    "Analyze the text and determine if it is Phishing, Scam, or aggressive Spam.\n"
    "Respond STRICTLY with this JSON object: {\"is_malevolent\": true} or {\"is_malevolent\": false}.\n"
    "Be extremely conservative: set true ONLY if 100% certain. When in doubt, set false."
)
