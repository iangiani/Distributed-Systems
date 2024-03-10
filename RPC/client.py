import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:8000')

def addinfo():
    topic = input("Enter the topic: ")
    note = input("Enter the note name: ")
    text = input("Enter the note text: ")
    timestamp = input("Enter the timestamp: ")
    print()
    info = server.saveinfo(topic, note, text, timestamp)
    if info:
        print(info)
    else:
        print("The topic was added unsuccessfully.")

def searchtopic():
    topicname = input("Enter the topic to search: ")
    print()
    topic = server.gettopic(topicname)
    if isinstance(topic, list):
        for i in topic:
            print(f"Note name: {i['name']}")
            print(f"Text: {i['text']}")
            print(f"Timestamp: {i['timestamp']}")
    else:
        print(topic)

def searchinfo():
    topic = input("Enter the topic to search on Wikipedia: ")
    print()
    wikipedia = server.searchwiki(topic)
    if isinstance(wikipedia, dict):
        print(f"Title: {wikipedia['title']}")
        print(f"Snippet: {wikipedia['snippet']}")
        print(f"Link: https://en.wikipedia.org/wiki/{wikipedia['title'].replace(' ', '_')}")
    else:
        print(wikipedia)

while True:
    print("\nMenu\n1. Add information\n2. Search Topic\n3. Search Wikipedia information\n4. Exit\n")
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            addinfo()
        elif choice == 2:
            searchtopic()
        elif choice == 3:
            searchinfo()
        elif choice == 4:
            break
        else:
            print("Please enter a number between 1 and 4.")
    except ValueError:
        print("Please enter a valid number.")