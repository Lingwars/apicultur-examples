#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LematizadorExample
==================
En este ejemplo se muestra un servicio que trabaja sobre la respuesta devuelta por la API
correspondiente para extraer un dato del json de respuesta y será este dato el que se
devuelva al usuario (ver [issue#3](https://github.com/jgsogo/apicultur-python/issues/4))

El endpoint `lematiza2` devuelve un json con todo este contenido:

```
{
    'palabra':'meses',
    'lemas':[
        {
            'lema':'mes',
            'categoria':'NCMP000'
        },
        {
            'lema':'mesar',
            'categoria':'VMSP2S0'
        }
    ]
}
```

lo que se realiza dentro de la función `LematizadorExample::handle_response` es seleccionar el lema
de la primera acepción y devolver únicamente esa cadena de texto: 'mes'.

Ejemplo mínimo de uso (ver final de este archivo)
"""

from apicultur.service import Service

class LematizadorExample(Service):
    version = '1.0.0'
    endpoint = 'lematiza2'
    func_name = 'lematiza'
    method = 'GET'
    arguments = ['word',]

    def get_endpoint(self):
        return self._join_url(self.endpoint, self.version, '%(word)s')

    def handle_response(self, response):
        lemmas = super(LematizadorExample, self).handle_response(response)
        # Devolverá el primer lema (ejemplo)
        if lemmas:
            lema = lemmas['lemas'][0]  # TODO: Desambiguation!
            return lema['lema']
        else:
            return None


if __name__ == '__main__':
    import os
    dirname = os.path.dirname(os.path.abspath(__file__))
    import sys; sys.path.append(os.path.dirname(dirname))

    from secret import ACCESS_TOKEN
    from apicultur import Apicultur

    api = Apicultur(ACCESS_TOKEN)

    api.add_services(dirname=dirname)
    print(u"Listado de servicios accesibles:")
    api.list_services()  # Podemos comprobar cómo se ha añadido este servicio.

    print(u"Realizando la llamada a la API...")
    data = api.lematiza(word='meses')
    print(data)  # Debe imprimirse la palabra 'mes' por pantalla.