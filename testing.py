from pattex.extractors.internet import extract_emails, extract_emails_legacy
from icecream import ic 


# ic(extract_emails("Contact us at info@example.com or support@company.org"))

# ic(extract_emails("dsa  das ads asd..shahmeer@gmail.com"))

result = extract_emails_legacy("shahmeer_-.@gmail.co.uk.in..")
ic(result)