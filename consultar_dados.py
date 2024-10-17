# consultar_dados.py

from modelo import session, Produtor, Cultura, Sensor, Leitura, AjusteIrrigacao, AjusteNutrientes
from tabulate import tabulate

def consultar_dados():
    """
    Consulta e exibe todos os dados do banco de dados de forma estruturada.
    """
    # Consultar todos os produtores
    produtores = session.query(Produtor).all()
    
    for produtor in produtores:
        print(f"\nProdutor: {produtor.nome}")
        print(f"Email: {produtor.email}")
        print(f"Telefone: {produtor.telefone}\n")
        
        # Consultar culturas do produtor
        for cultura in produtor.culturas:
            print(f"  Cultura: {cultura.tipo_cultura}")
            print(f"    Plantio: {cultura.data_plantio}")
            print(f"    Colheita: {cultura.data_colheita}\n")
            
            # Consultar sensores da cultura
            for sensor in cultura.sensores:
                print(f"    Sensor ID: {sensor.id_sensor}")
                print(f"      Tipo: {sensor.tipo_sensor}")
                print(f"      Localização: {sensor.localizacao}\n")
                
                # Consultar leituras do sensor
                leituras = sensor.leituras
                if leituras:
                    if sensor.tipo_sensor == "S1":
                        headers = ["Data/Hora", "Umidade (%)"]
                        data = [[leitura.data_hora, leitura.valor_umidade] for leitura in leituras]
                    elif sensor.tipo_sensor == "S2":
                        headers = ["Data/Hora", "pH"]
                        data = [[leitura.data_hora, leitura.valor_pH] for leitura in leituras]
                    elif sensor.tipo_sensor == "S3":
                        headers = ["Data/Hora", "P (kg)", "K (kg)"]
                        data = [[leitura.data_hora, leitura.valor_P, leitura.valor_K] for leitura in leituras]
                    
                    print(f"      Leituras de {sensor.tipo_sensor}:")
                    print(tabulate(data, headers=headers, tablefmt="grid"))
                    print()
                else:
                    print("      Sem leituras registradas.\n")
            
            # Consultar ajustes de irrigação
            ajustes_irrigacao = cultura.ajustes_irrigacao
            if ajustes_irrigacao:
                print("    Ajustes de Irrigação:")
                data_irrigacao = [
                    [ajuste.data_hora, ajuste.quantidade_agua]
                    for ajuste in ajustes_irrigacao
                ]
                print(tabulate(
                    data_irrigacao,
                    headers=["Data/Hora", "Quantidade de Água (litros)"],
                    tablefmt="grid"
                ))
                print()
            else:
                print("    Sem ajustes de irrigação registrados.\n")
            
            # Consultar ajustes de nutrientes
            ajustes_nutrientes = cultura.ajustes_nutrientes
            if ajustes_nutrientes:
                print("    Ajustes de Nutrientes:")
                data_nutrientes = [
                    [ajuste.data_hora, ajuste.quantidade_P, ajuste.quantidade_K]
                    for ajuste in ajustes_nutrientes
                ]
                print(tabulate(
                    data_nutrientes,
                    headers=["Data/Hora", "Quantidade de P (kg)", "Quantidade de K (kg)"],
                    tablefmt="grid"
                ))
                print()
            else:
                print("    Sem ajustes de nutrientes registrados.\n")

if __name__ == "__main__":
    consultar_dados()