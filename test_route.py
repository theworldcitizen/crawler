import requests
import json

requests.put("http://127.0.0.1:5000/update_by",
             data=json.dumps({'obj': {'title': 'Test5', 'description': 'updated now', 'publication_date': 'updated date',
                                      'link': "https://www.zakon.kz//5085804-v-kazahstane-zapretyat-est-koshek-i.html"}}))
