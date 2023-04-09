from xml.dom import minidom
# assume vector of dictionaries, each dictionary is <key, vector<vector<Point>>>
# each user is a key, each vector of vectors corresponds to a gesture, each vector of points corresponds to an individual instance of a gesture

def SendToXML():
    user_data = {"s01": [[0,0,0,0], [0,0,0,0]], "s02": [[0,0,0,0], [0,0,0,0]]}
    for name, gestures in user_data:
        for gesture in gestures:
            doc = minidom.Document()
            root = doc.createElement('Gesture')
            root.setAttribute('Name', name)
            doc.appendChild(root)
            for point in gesture:
                leaf = doc.createElement('')
            xml_str = doc.toprettyxml(indent="  ")
            with open("minidom_example.xml", "w") as f:
                f.write(xml_str)



if __name__ == "__main__":
    SendToXML()