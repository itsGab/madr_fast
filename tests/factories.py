from random import randint

import factory.fuzzy

from madr_fast.models import Livro, Romancista, Usuario


class UsuarioFactory(factory.Factory):
    class Meta:
        model = Usuario

    username = factory.Sequence(lambda n: f'usuario{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}-segredo')


class RomancistaFactory(factory.Factory):
    class Meta:
        model = Romancista

    nome: str = factory.Sequence(lambda n: f'Nome {n}')


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    titulo: str = factory.Sequence(lambda n: f'Livro {n}')
    ano: int = randint(1999, 2024)
    romancista_id = 1  # romancista valido
