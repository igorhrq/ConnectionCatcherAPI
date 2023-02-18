from flask import Flask, jsonify
import subprocess
import time

app = Flask(__name__)

# O acesso será feito em 2 ou mais servidores, aqui estou usando apenas 2 servidores web, mas voce pode adicionar mais coisas no dicionario
servers = [
    {"name": "web01", "ip": "IPAQUI"},
    {"name": "web02", "ip": "IPAQUI"}
]

#voce deve acessar o http://IPPUBLICO:1904/connections

@app.route("/connections")
def connections():
    result = []
    total_count = 0

    for server in servers:
        count = get_connection_count(server["ip"])
        total_count += count
        result.append({
            "Server is": server["name"],
            "Processes Count": count,
            "generated_at_time": int(time.time())
        })
# Retorna a soma completa em ambos os servidores, mais acima ele também coleta individualmente, e aqui entrega a soma de ambos ou de todos existentes
    return jsonify({
        "allservers_totalcount": total_count,
        "servers": result
    })

  # estou coletando conexoes nos 2 servidores que setei ali na variavel servers, ele faz o login ssh e faz a coleta do que está rodando no estado do TCP/IP
  # como ESTABLISHED
def get_connection_count(ip):
    ss_output = subprocess.run(['ssh', ip, 'ss', '-t', '-a', 'state', 'ESTABLISHED', 'dst', 'IPAQUI:PORTADESEJADA'], capture_output=True).stdout.decode("utf-8")
    return len(ss_output.split("\n")) - 1

# flask no ip publico, na porta 1904
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1904, debug=True)
