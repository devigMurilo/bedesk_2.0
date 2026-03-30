from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agendamento, PostagemBlog
from datetime import date


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Nome', required=True)
    last_name = forms.CharField(max_length=50, label='Sobrenome', required=True)
    email = forms.EmailField(label='E-mail', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Nome de usuário'


class AgendamentoForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': str(date.today())}),
        label='Data',
    )
    horario = forms.ChoiceField(label='Horário', widget=forms.Select(attrs={'class': 'form-control'}))
    descricao = forms.CharField(
        required=False,
        label='Motivo / Descrição',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )

    class Meta:
        model = Agendamento
        fields = ['data', 'descricao']

    def __init__(self, *args, slots=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('', '--- Selecione um horário ---')]
        if slots:
            for inicio, fim in slots:
                label = f"{inicio:%H:%M} – {fim:%H:%M}"
                value = f"{inicio:%H:%M}"
                choices.append((value, label))
        self.fields['horario'].choices = choices

    def save(self, commit=True):
        instance = super().save(commit=False)
        horario_str = self.cleaned_data['horario']
        from datetime import datetime, timedelta
        from .models import gerar_horarios_disponiveis
        slots = gerar_horarios_disponiveis()
        hora_inicio = datetime.strptime(horario_str, '%H:%M').time()
        hora_fim = None
        for inicio, fim in slots:
            if inicio == hora_inicio:
                hora_fim = fim
                break
        instance.hora_inicio = hora_inicio
        instance.hora_fim = hora_fim
        if commit:
            instance.save()
        return instance


class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Nome', 'last_name': 'Sobrenome', 'email': 'E-mail'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostagemBlogForm(forms.ModelForm):
    class Meta:
        model = PostagemBlog
        fields = ['titulo', 'categoria', 'resumo', 'conteudo', 'imagem', 'imagem_arquivo', 'destaque', 'publicado']
        labels = {
            'titulo': 'Titulo',
            'categoria': 'Categoria',
            'resumo': 'Resumo',
            'conteudo': 'Conteudo',
            'imagem': 'URL da imagem de capa',
            'imagem_arquivo': 'Arquivo da imagem de capa',
            'destaque': 'Definir como destaque',
            'publicado': 'Publicar agora',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Como organizar sua semana'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Produtividade'}),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Resumo curto para os cards do blog'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Escreva o conteudo completo da postagem'}),
            'imagem': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'imagem_arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destaque'].widget.attrs['class'] = 'form-check-input'
        self.fields['publicado'].widget.attrs['class'] = 'form-check-input'

    def clean(self):
        cleaned_data = super().clean()
        imagem_url = cleaned_data.get('imagem')
        imagem_arquivo = cleaned_data.get('imagem_arquivo')

        if not imagem_url and not imagem_arquivo:
            raise forms.ValidationError('Informe uma URL de imagem ou envie um arquivo para a capa.')

        return cleaned_data
