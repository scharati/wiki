import dbservice

users = dbservice.get_all_users()
for user in users:
    print(user.username)
    print(user.pwdhash)

user = dbservice.get_user_by_name("user1")
print(user.username)
print(user.pwdhash)

pages = dbservice.get_all_wikipages();
for page in pages:
    print(page.title)
    print(page.content)
    print(page.owner)