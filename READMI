# DDoS Light Tester

Uma ferramenta em Python para simulações leves de ataques DDoS com foco em testes de intrusão, estresse de rede e validação de mitigação (WAF/IDS).

## 🚀 Funcionalidades

- **Protocolos Suportados**: TCP, UDP e ICMP.
- **Multi-threading**: Distribuição de carga via threads para aumentar o PPS (Packets Per Second).
- **Interface Interativa**: Configuração via CLI de alvo, porta, duração e volume de pacotes.
- **Monitoramento em Tempo Real**: Exibição de PPS, pacotes enviados e tempo restante durante o teste.
- **Estatísticas Finais**: Relatório de desempenho ao término da simulação.

## 📋 Requisitos

- Python 3.7+
- Scapy 2.8.0+
- **Npcap** (Obrigatório para Windows)

## 🛠️ Instalação

1. **Instale o Npcap (Windows)**
   - Baixe em [npcap.com](https://npcap.com/#download).
   - **Importante**: Durante a instalação, marque a opção **"Install Npcap in WinPcap API-compatible Mode"**.

2. **Instale as dependências Python**
   ```bash
   pip install scapy

🚀 Como Usar
Execute o script e siga o prompt interativo:

bash
Download
Copy code
python ddos_tester.py
Exemplo de Sessão
text
Download
Copy code
==================================================
  Gerador de DDoS Leve para Testes de Invasão
==================================================
Alvo (IP ou Hostname): 192.168.1.100
Protocolo (tcp/udp/icmp) [tcp]: tcp
Porta de destino [80]: 80
Duração em segundos [60]: 30
Número de pacotes [10000]: 5000
Número de threads [4]: 8

Iniciando teste: TCP -> 192.168.1.100:80
Configuração: 30s, 5000 pacotes, 8 threads
[Monitor] Tempo: 1.0s | Pacotes: 482 | PPS: 482.0 | Restante: 4518
...
=== Estatísticas Finais ===
Duração Total: 30.02s
Pacotes Enviados: 5000
PPS Médio: 166.5

⚙️ Parâmetros

Parâmetro	Descrição	Default
Alvo	IP ou Hostname do destino.	-
Protocolo	tcp, udp ou icmp.	tcp
Porta	Porta de destino (TCP/UDP).	80
Duração	Tempo máximo de execução (segundos).	60
Pacotes	Limite total de pacotes a enviar.	10000
Threads	Número de threads de envio.	4

📝 Notas de Segurança

Ambiente Isolado: Execute apenas em redes de laboratório (ex: GNS3, Vagrant, Docker) ou ambientes de teste controlados.
Autorização: Nunca execute contra sistemas de terceiros sem permissão explícita.

Impacto Local: Ajuste o número de threads e o volume de pacotes para evitar saturar a interface de rede local da sua máquina de origem.

📄 Licença

MIT

