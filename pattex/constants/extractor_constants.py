from typing import Literal
from enum import Enum

EMAIL_MODES = Literal["practical", "rfc5322"]
# TODO: Merge both of them in a way that we can have both the benefits of type safety and ease of use.
# e.g. write a function in EmailProvider class that returns list of literals of all providers, 
# and then use that function to define the EMAIL_PROVIDERS literal.
EMAIL_PROVIDERS = Literal["gmail", "yahoo", "outlook", "icloud", "zoho", "proton"]

class EmailProvider(str, Enum): 
    GMAIL = "gmail"
    YAHOO = "yahoo"
    OUTLOOK = "outlook"
    ICLOUD = "icloud"
    ZOHO = "zoho"
    PROTON = "proton"


# ── Known URL schemes ────────────────────────────────────────────────────────
 
STRICT_SCHEMES = frozenset({"http", "https", "ftp", "ftps", "sftp", "ws", "wss"})
 
SCHEME_PATTERN = r"(?:https?|ftps?|sftp|wss?)"
 
# ── Curated common TLDs (~200 most common) ───────────────────────────────────
# Used in permissive mode to validate bare-domain URLs (no scheme).
# Not exhaustive — intentionally curated to balance recall vs false positives.
 
COMMON_TLDS = frozenset({
    # Generic
    "com", "org", "net", "edu", "gov", "mil", "int",
    # New generic
    "io", "ai", "co", "app", "dev", "api", "web", "cloud",
    "tech", "info", "biz", "name", "pro", "mobi", "coop",
    "aero", "museum", "travel", "jobs", "tel", "cat", "post",
    "xxx", "arpa", "example",
    # Popular new gTLDs
    "online", "site", "website", "store", "shop", "blog",
    "media", "news", "agency", "studio", "design", "digital",
    "software", "systems", "solutions", "services", "group",
    "network", "global", "world", "zone", "space", "live",
    "stream", "video", "audio", "photo", "image", "gallery",
    "social", "chat", "email", "mail", "marketing", "ads",
    "finance", "money", "bank", "insurance", "invest",
    "health", "clinic", "hospital", "doctor", "care",
    "school", "academy", "university", "college", "training",
    "law", "legal", "attorney", "accountant",
    "realty", "property", "estate", "homes", "house",
    "auto", "cars", "bike", "taxi", "flights", "hotel",
    "food", "bar", "cafe", "restaurant", "pizza",
    "game", "games", "play", "sport", "fit", "yoga",
    "music", "art", "fashion", "style", "beauty",
    "plus", "pro", "expert", "guru", "ninja", "rocks",
    "run", "works", "build", "tools", "support", "help",
    "today", "now", "new", "top", "best", "one", "first",
    "link", "click", "download", "open", "free",
    # Country codes (most common)
    "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao",
    "aq", "ar", "as", "at", "au", "aw", "ax", "az",
    "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "bj", "bm",
    "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz",
    "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm",
    "cn", "co", "cr", "cu", "cv", "cx", "cy", "cz",
    "de", "dj", "dk", "dm", "do", "dz",
    "ec", "ee", "eg", "er", "es", "et", "eu",
    "fi", "fj", "fk", "fm", "fo", "fr",
    "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm",
    "gn", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy",
    "hk", "hm", "hn", "hr", "ht", "hu",
    "id", "ie", "il", "im", "in", "io", "iq", "ir", "is", "it",
    "je", "jm", "jo", "jp",
    "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz",
    "la", "lb", "lc", "li", "lk", "lr", "ls", "lt", "lu", "lv", "ly",
    "ma", "mc", "md", "me", "mg", "mh", "mk", "ml", "mm", "mn", "mo",
    "mp", "mq", "mr", "ms", "mt", "mu", "mv", "mw", "mx", "my", "mz",
    "na", "nc", "ne", "nf", "ng", "ni", "nl", "no", "np", "nr", "nu", "nz",
    "om",
    "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", "pr", "ps",
    "pt", "pw", "py",
    "qa",
    "re", "ro", "rs", "ru", "rw",
    "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl",
    "sm", "sn", "so", "sr", "st", "su", "sv", "sy", "sz",
    "tc", "td", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to",
    "tp", "tr", "tt", "tv", "tw", "tz",
    "ua", "ug", "uk", "um", "us", "uy", "uz",
    "va", "vc", "ve", "vg", "vi", "vn", "vu",
    "wf", "ws",
    "ye", "yt",
    "za", "zm", "zw",
})