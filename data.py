from faker import Faker
faker = Faker('pt_BR')
import pandas as pd
import numpy as np

np.random.seed(42)

# Vendedores
vendedores = pd.DataFrame({
    'Nome': [
        'Lucas Ferreira', 'Ana Paula Souza', 'Carlos Eduardo',
        'Juliana Mendes', 'Felipe Rocha', 'Mariana Oliveira',
        'Bruno Lima', 'Camila Duarte', 'Rafael Costa', 'Isabela Martins'
    ],
    'Vendas': np.random.randint(50, 500, size=10),
    'Foto': [
        'https://randomuser.me/api/portraits/men/32.jpg',
        'https://randomuser.me/api/portraits/women/45.jpg',
        'https://randomuser.me/api/portraits/men/76.jpg',
        'https://randomuser.me/api/portraits/women/15.jpg',
        'https://randomuser.me/api/portraits/men/84.jpg',
        'https://randomuser.me/api/portraits/women/34.jpg',
        'https://randomuser.me/api/portraits/men/21.jpg',
        'https://randomuser.me/api/portraits/women/52.jpg',
        'https://randomuser.me/api/portraits/men/14.jpg',
        'https://randomuser.me/api/portraits/women/60.jpg'
    ],
    'Telefone': [faker.phone_number() for _ in range(10)],
    'Endereço': [faker.address().replace("\n", ", ") for _ in range(10)]
}).sort_values(by='Vendas', ascending=False)


# Dados principais
dates = pd.date_range(start="2022-01-01", periods=100)
df = pd.DataFrame({
    'Sales': np.random.randint(100, 1000, size=100),
    'Customers': np.random.randint(10, 100, size=100),
    'Revenue': np.random.uniform(1000, 5000, size=100)
}, index=dates)


def gerar_vendas_fakes(nome_vendedor, qtd=5):
    vendas = []
    for _ in range(qtd):
        vendas.append({
            'Cliente': faker.name(),
            'Produto': faker.word().capitalize(),
            'Valor (R$)': round(np.random.uniform(50, 5000), 2),
            'Vendedor': nome_vendedor
        })
    return vendas
