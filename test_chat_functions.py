#!/usr/bin/env python3
"""
Teste rápido das funcionalidades do chat J.A.R.V.I.S. M-13
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import JarvisLogger
from actions import SystemActions

def test_functions():
    """Testa as funções que devem aparecer no chat"""
    print("🤖 TESTANDO FUNCIONALIDADES DO CHAT J.A.R.V.I.S. M-13")
    print("=" * 60)
    
    logger = JarvisLogger()
    actions = SystemActions(logger)
    
    # Teste 1: Cotação
    print("\n💱 TESTE 1: COTAÇÃO DO DÓLAR")
    result_cotacao = actions.get_currency_final('dólar')
    print(f"Retorno: {result_cotacao}")
    print(f"Tipo: {type(result_cotacao)}")
    print(f"Contém 'R$': {'Sim' if 'R$' in result_cotacao else 'Não'}")
    
    # Teste 2: Clima
    print("\n🌤️ TESTE 2: CLIMA")
    result_clima = actions.get_weather_votorantim()
    print(f"Retorno: {result_clima}")
    print(f"Tipo: {type(result_clima)}")
    print(f"Contém '°C': {'Sim' if '°C' in result_clima else 'Não'}")
    
    # Teste 3: Notícias
    print("\n📰 TESTE 3: NOTÍCIAS")
    result_noticias = actions.get_news_headlines()
    print(f"Retorno: {result_noticias}")
    print(f"Tipo: {type(result_noticias)}")
    print(f"Contém 'G1': {'Sim' if 'G1' in result_noticias else 'Não'}")
    
    print("\n✅ TESTES CONCLUÍDOS!")
    print("Se todos os retornos são strings e contêm os valores esperados,")
    print("então as funções estão prontas para o chat.")

if __name__ == "__main__":
    test_functions()
