from django.shortcuts import render, redirect
from perfis.models import Perfil, Convite
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def index(request):
   print(request.user.username)
   print(request.user.email)
   print(request.user.has_perm('perfis.add_convite'))
   print(request.user.has_perm('perfis.redirect'))
   return render(request, 'index.html', {'perfis' : Perfil.objects.all(), 'perfil_logado': get_perfil_logado(request)})

@login_required
def exibir(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	ja_e_contato  = perfil in perfil_logado.contatos.all()
#	return render(request, 'perfil.html', {'perfil': perfil, 'perfil_logado': get_perfil_logado(request), 'ja_e_contato': ja_e_contato})
	return render(request, 'perfil.html', {'perfil':perfil, 'ja_e_contato':ja_e_contato})

@permission_required('perfis.add_convite', raise_exception=True)
@login_required
def convidar(request, perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	perfil_logado.convidar(perfil_a_convidar)
	return redirect('index')
#	return render(request, 'perfil.html', {'perfil':perfil, 'perfil_logado':get_perfil_logado(request)})

@login_required
def get_perfil_logado(request):
#	return request.perfil
#	return Perfil.objects.get(id=1)
	return request.user.perfil

@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id=convite_id)
	convite.aceitar()
	return redirect('index')
