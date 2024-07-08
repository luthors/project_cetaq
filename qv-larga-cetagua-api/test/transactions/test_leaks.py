import json
import os
import io
from django.urls import reverse
from test.test_setup import TestSetUp
from test.factories.transactions.transactions_factories import TransactionsFactories
from rest_framework import status
import mimetypes

from codecs import encode

from django.core.files.base import ContentFile


class LeaksTestCase(TestSetUp):
    def test_leaks(self):

        #######################################################33
        with open('/home/oem/Luthors/Cetaqua/archivos de prueba/leaks/prueba.xlsx', 'rb') as f:
            file = ContentFile(f.read(), name='prueba.xlsx')
        parameters = TransactionsFactories().get_parameters()
        
        parameters= json.dumps(parameters)
        
        data= {
            'Parameters': str(parameters),
            # 'File': file,
        }
        
        
        
        url = reverse('leaks_search')
        
        headers = {
            'City': 'Roquetas de Mar',
            'Analize-Days': 14,
            'Indicators-Days': 1,
            # 'Content-Type': 'application/json',
            # 'Cookie': 'csrftoken=r7hs9dgR9cdqAUEmU5KuSnG6e0313dr3'
        }

        response = self.client.post(
            url,
            headers=headers,
            data=data,
            format='json',            
        )

        import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
