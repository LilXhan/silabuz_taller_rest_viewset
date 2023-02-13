# Taller

Para este taller vamos a recordar el funcionamiento del ViewSet y vamos a comenzar a hacer usos de los distintos filtros que este puede utilizar al momento de retornar resultados.

Tenemos 4 tipos de ViewSets:

-   ViewSet
-   GenericViewSet
-   ModelViewSet
-   ReadOnlyModelViewSet

Ahora implementaremos un ModelViewSet básico, de forma similar a un APIView

Pero ¿qué diferencia hay?

En el caso de un APIView, tenemos que se puede realizar la implementación de los métodos GET, POST, UPDATE, DELETE, etc. Por otro lado, un ViewSet permite el mismo tipo de implementación pero sus funciones están más orientadas a los objetos y peticiones de una API normal.

Por ejemplo, dentro de un ViewSet encontramos las siguiente operaciones.

-   list -GET
    
-   create-POST
    
-   retrieve-GET un registro en específico
    
-   update-POST un registro en específico
    
-   partial_update- PATCH un registro en específico
    
-   destroy — DELETE
    

Si recuerdas, en la anterior sesión para implementar las operaciones de un TODO individual, tuvimos que crear otra vista distinta, en este caso con el ViewSet solo se hace la implementación de una única vista que soporta este tipo de operaciones tanto grupales como individuales.

## Implementación de un ViewSet

Para hacer la primera implementación de nuestro ViewSet, crearemos la clase `TodoViewSetCustom`, en `todos/api.py`.

```py
class TodoViewSetCustom(viewsets.ModelViewSet):
    queryset = Todo.objects.all()

    def get_serializer_class(self):
        return TodoSerializer

    def list(self, request):
        pass
```

Ahora, añadiremos nuestra nueva vista a las rutas en `todos/urls.py`.

```py
from rest_framework import routers
from .api import TodoViewSetCustom

router = routers.DefaultRouter()

router.register('api/v3/todo', TodoViewSetCustom, 'todosCustom')

# ...
```

En este caso el default router incluye una vista por defecto para nuestra API, que retorna una lista de vínculos, con la lista de todas las vistas.

Ahora que lo tenemos registrado, podemos ver en nuestra vista principal lo siguiente:

![Nueva ruta](https://photos.silabuz.com/uploads/big/3cb58bdf9d47872456f0b9bf0dd17c67.PNG)

Nuestra nueva ruta se encuentra registrada correctamente.

### GET Methods

Para los get, tenemos tanto el `list`, como el `retrieve`, la implementación sería la siguiente.

```py
class TodoViewSetCustom(viewsets.ModelViewSet):
    def list(self, request):
        queryset = Todo.objects.all()
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Todo.objects.all()
        todo = get_object_or_404(queryset, pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
```

Ahora que tenemos incluida nuestra ruta si hacemos uso de ella, tendremos la vista de nuestros registros de forma correcta.

![List](https://photos.silabuz.com/uploads/big/d901e123d0df012c24e95b5f70657387.PNG)

![Instance](https://photos.silabuz.com/uploads/big/c93c8521e9fe7c658bd2d8b618dddd89.PNG)

En la parte de los títulos, al inicio vemos que es un list y luego una instancia, mostrando como DRF reconoce los métodos por separado.

### POST Methods

Para la parte de los métodos POST, vamos a crear la opción para ingresar elementos en una lista de JSON.

#### Creación simple y múltiple

Para que nuestra API admita la opción de la creación de múltiples registros, añadimos las siguientes líneas.

```py
class TodoViewSetCustom(viewsets.ModelViewSet):
    # ...
    def create(self, request):
        if isinstance(request.data, list):
            serializer = TodoSerializer(data=request.data, many = True)
        else:
            serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Para la creación múltiple tenemos que se verifica que los datos sean del tipo list, si es el caso es que se hace uso de `many = True`, si no se hace uso de la creación para un solo dato.

Si probamos nuestro nuevo método obtenemos la siguiente respuesta:

![Múltiple](https://photos.silabuz.com/uploads/big/3e9498fe735fa26e9e90a77277b7440b.PNG)

![Creado](https://photos.silabuz.com/uploads/big/95c7c9c4f8a7f96d67d00f781d7ca5e8.PNG)

#### Modificación de registros

Para agregar las operaciones de PUT y PATCH, añadimos las siguientes líneas:

```py
class TodoViewSetCustom(viewsets.ModelViewSet):
    # ...

    def update(self, request, pk=None):
        queryset = Todo.objects.all()
        todo = get_object_or_404(queryset, pk=pk)
        serializer = TodoSerializer(todo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Todo.objects.all()
        todo = get_object_or_404(queryset, pk=pk)
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
```

En este caso, tenemos que update corresponde al PUT, y partial_update a PATCH, mucho más sencillo de implementar ¿no?.

Si hacemos uso de las nuevas operaciones obtenemos el siguiente resultado.

-   PUT
    
    ![PUT](https://photos.silabuz.com/uploads/big/1f7868c023dc968cf4d3a882aeba9894.PNG)
    
    ![PUT Completado](https://photos.silabuz.com/uploads/big/204e9d67cc05895bb7b315dd822b2197.PNG)
    
-   PATCH
    
    ![PATCH](https://photos.silabuz.com/uploads/big/42226b0c438e4b7b75e21f04b33accf7.PNG)
    
    ![PATCH Completado](https://photos.silabuz.com/uploads/big/f423cb8d257eac00a9041040741a824f.PNG)
    

### DELETE

Por último, para agregar el DELETE a nuestra API, vamos a crear el método `destroy`.

```py
class TodoViewSetCustom(viewsets.ModelViewSet):
    # ...

    def destroy(self, request, pk=None):
        queryset = Todo.objects.all()
        todo = get_object_or_404(queryset, pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Si ejecutamos nuestro nuevo método, deberíamos obtener el siguiente resultado.

![GET](https://photos.silabuz.com/uploads/big/0cd7d62a99f779f7876e6254c876b3ba.PNG)

![Eliminado](https://photos.silabuz.com/uploads/big/ebea7f57a29f5084258019367345d055.PNG)

Con este último método, tendríamos implementados las principales operaciones de una API común.

## Filtros

Antes de comenzar con esta sección. Hacer la creación de registros a partir del siguiente JSON:

[https://gist.github.com/silabuz/2b39ea4e53e3a7eff7ee0b2d766f1053](https://gist.github.com/silabuz/2b39ea4e53e3a7eff7ee0b2d766f1053)

Luego de haber agregado todo los datos, no se pueden ver de forma cómoda ¿no?. Por lo que, agregaremos filtros a nuestra API para que nuestros datos sean leídos de una mejor forma.

### Paginación

Primero añadiremos la paginación para que nuestros datos sean leídos de mejor forma. El resultado a obtener al momento de hacer un GET debería ser de la siguiente forma.

```response
HTTP 200 OK
{
    "count": 1023,
    "next": "https://api.example.org/accounts/?page=5",
    "previous": "https://api.example.org/accounts/?page=3",
    "results": [
       …
    ]
}
```

Entonces, para realizar la paginación, existen dos formas de realizar dicho proceso.

-   Global: La paginación se crea para todas las vistas.
    
-   Clase: La paginación se crea para una sola clase en específico
    

Por ejemplo, para crear la paginación global, debemos modificar el `settings.py` y añadir las siguientes líneas.

```py
REST_FRAMEWORK = {
    # ...
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

Donde `PAGE_SIZE` indica el tamaño que van a tener los resultados por página.

Pero para nuestra vista vamos a crear una paginación propia.

Creamos el archivo `pagination.py`, dentro de nuestra app `todos`.

Luego de hacer creado el archivo creamos la siguiente clase para crear nuestro paginador.

```py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
```

`page_size` define el tamaño de los resultados mostrados por página.

Luego de haber creado el paginador, es momento de añadirlo a nuestra vista.

```py
from .pagination import StandardResultsSetPagination

class TodoViewSetCustom(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    pagination_class = StandardResultsSetPagination
    # ...

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
```

En este caso, aparte de añadir la clase que va a realizar la paginación, necesitamos crear el paginador dentro de nuestro método `list`.

Ahora que tenemos la paginación realizada, si recargamos nuestra vista, obtenemos la siguiente respuesta.

![Paginación](https://photos.silabuz.com/uploads/big/a7103bb6a642a3e5cb66fd0b7f7d4b33.PNG)

¡Obtenemos nuestros resultados paginados!

### Otro filtros

Dentro de nuestras vistas, también podemos añadir otros tipos de filtros.

-   Búsqueda
    
-   Ordenamiento
    

Para hacer uso de ellos, vamos a crear una nueva vista genérica, sin sobrescribir los métodos.

```py
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = StandardResultsSetPagination
```

Luego de crearla la registramos en `todos/urls.py`:

```py
# ...
from .api import TodoViewSet
# ...
router.register('api/v4/todo', TodoViewSet, 'todos')

# ...
```

#### Filtro de búsqueda

Podemos añadir filtros para buscar campos en específico.

```py
class TodoViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']
```

Dentro de nuestra vista nos aparecerá un nuevo campo que podemos utilizar.

![Filtros](https://photos.silabuz.com/uploads/big/d8629bc6f96b7b6bd9754e81b4827cb2.PNG)

Ahora podemos hacer uso del filtro. Si ingresamos alguna búsqueda, la query se realizará tanto para el título como para el cuerpo del todo.

![Búsqueda](https://photos.silabuz.com/uploads/big/46bc7453936145c6a3102f98cf3f4254.PNG)

![Resultado](https://photos.silabuz.com/uploads/big/46bc7453936145c6a3102f98cf3f4254.PNG)

## Tarea

-   Implementar las dos vistas realizadas en el taller.

> Recordar de hacer la prueba de cada método implementado

-   Añadir el filtro en `TodoViewSet` para ordenar los resultados, ordenarlos por la fecha de creación.
    
-   Realizar el ordenamiento por el título.
    
-   Realizar el ordenamiento por el id
    
-   Modificar la paginación para que muestre 150 resultados por página
    
-   Añadir la paginación de forma global y probarlo en ambas vistas creadas.
    

Responder ¿por qué `TodoViewSetCustom` y `TodoView` funcionan casi de la misma forma cuando uno tiene métodos implementados y el otro no?.

## Tarea opcional

Implementar el ordenamiento en `TodoViewSetCustom`.

LINKS

[Diapositivas](https://docs.google.com/presentation/d/e/2PACX-1vQGX975Nq_nurjgY2buzqwnKfnax3vKw3j5uvku4gDYT52qapzMY7QcRRP8siupxB6KPRGWrQr2Mpdk/embed?start=false&loop=false&delayms=3000&slide=id.g143f30675af_0_0)

LINKS YOUTUBE

[Teoria](https://www.youtube.com/watch?v=KqR611j8Zgg&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=10&ab_channel=Silabuz)
[Practica](https://www.youtube.com/watch?v=qrQxmx_4ETo&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=11&ab_channel=Silabuz)