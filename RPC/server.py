from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as etree
import requests

tree = etree.parse('/Users/iangani/Desktop/RPC/db.xml')
root = tree.getroot()

def saveinfo(topic, note, text, timestamp):
    try:
        topicname = root.find(f'.//topic[@name="{topic}"]')
        if topicname is None:
            topicname = etree.SubElement(root, 'topic')
            topicname.set('name', topic)
        notename = etree.SubElement(topicname, 'note')
        notename.set('name', note)
        textcontent = etree.SubElement(notename, 'text')
        textcontent.text = text
        time = etree.SubElement(notename, 'timestamp')
        time.text = timestamp
        tree.write('/Users/iangani/Desktop/RPC/db.xml')
        return "The topic was added successfully."
    except Exception as e:
        return f"Error for adding topic: {str(e)}"

def gettopic(topic):
    try:
        topicname = root.find(f'.//topic[@name="{topic}"]')
        if topicname is not None:
            notes = []
            for i in topicname.findall('note'):
                note = {
                    'name': i.get('name'),
                    'text': i.find('text').text,
                    'timestamp': i.find('timestamp').text
                }
                notes.append(note)
            return notes
        else:
            return "Can not find the topic."
    except Exception as e:
        return f"Error for searching the topic information: {str(e)}"

def searchwiki(topic):
    try:
        response = requests.get(f'https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={topic}')
        response.raise_for_status() 
        wiki = response.json()
        if 'query' in wiki and 'search' in wiki['query']:
            wikicontent = wiki['query']['search'][0]
            saveinfo(topic, "Wikipedia", wikicontent['snippet'], "")
            return wikicontent
        else:
            return "Can not find the Wikipedia content."
    except requests.exceptions.RequestException as e:
        return f"Error for querying Wikipedia API: {str(e)}"

server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
server.register_function(saveinfo, 'saveinfo')
server.register_function(gettopic, 'gettopic')
server.register_function(searchwiki, 'searchwiki')
print("Server is ready.")
server.serve_forever()
