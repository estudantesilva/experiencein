from django.shortcuts import render, redirect
from perfis.models import Perfil, Convite
from django.contrib.auth.decorators import login_required


from rest_framework import viewsets, response, status, exceptions
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import AllowAny


class perfilviewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return None 
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method == 'POST':
            return (AllowAny(),)
        return super().get_permissions()


@api_view(['GET'])
@renderer_classes((JSONRenderer. BrowsableAPIRenderer))
def get_convites(request, *args, **kwargs):
    perfil_logado = get_perfil_logado(request)
    convites = Convite.objects.filter(convidado=perfil_logado)
    serializer = None
    return response.Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes((JSONRenderer. BrowsableAPIRenderer))
def convidar(request, *args, **kwargs):
    try:
        perfil_a_convidar = Perfil.objects.get(id=kwargs['perfil_id'])
    except:
        raise exceptions.NotFound('Não foi encontrado um perfil com o id informado.')
    perfil_logado = get_perfil_logado(request)
    if perfil_a_convidar != perfil_logado:
        perfil_logado.convidar(perfil_a_convidar)
        return response.Response({'menssagem': f'Convite enviado com sucesso para{ perfil_a_convidar.email}.'}, status=status.HTTP_201_CREATED)
    raise exceptions.ParseError('Você não pode convidar o perfil com id informado.')


@api_view(['POST'])
@renderer_classes((JSONRenderer. BrowsableAPIRenderer))
def aceitar(request, *args, **kwargs):
    perfil_logado = get_perfil_logado(request)
    try:
        convite = Convite.objects.filter(convidado=perfil_logado).get(id=kwargs['convite_id'])    
    except:
        raise exceptions.NotFound('Não foi encontrado um convite com o informado.')
    convite.aceitar()
    return response.Response({'menssagem': 'Convite aceito com sucesso.'}, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
@renderer_classes((JSONRenderer. BrowsableAPIRenderer))
def get_meu_perfil(request, *args, **kwargs):
    perfil_logado = get_perfil_logado(request)
    serializer = None
    return response.Response(serializer.data, status=status.HTTP_200_OK)

def get_perfil_logado(request):
    return request.user.perfil




@login_required
def index(request):
    return render(request, 'index.html', {'perfis': Perfil.objects.all(), 'perfil_logado': get_perfil_logado(request)})


@login_required
def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)

    perfil_logado = get_perfil_logado(request)
    ja_e_contato = perfil in perfil_logado.contatos.all()

    return render(request, 'perfil.html', {'perfil': perfil, "ja_e_contato": ja_e_contato})


@login_required
def convidar(request, perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.convidar(perfil_a_convidar)
    return redirect('index')


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


def get_perfil_logado(request):
    return request.user.perfil
