import json


person = '{"name": "Bob", "languages": ["English", "Fench"]}'



person_dict = json.loads(person)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print( person_dict)

# Output: ['English', 'French']
print(person_dict['languages'])




















hnna_test = {
    "header": {
        "timestamp": "1594694553.324941158",
        "target": [
            "dialog",
            "planning"
        ],
        "source": "perception",
        "content": [
            "human_speech"
        ]
    },
    "human_speech": {
        "name": "이병현",
        "speech": "오냐."
    }
}

if hnna_test["header"]["target"] == ["dialog","planning"] and hnna_test["header"]["source"] == "perception" and hnna_test["header"]["content"] == "human_speech":
    print(hnna_test["human_speech"]["speech"])
