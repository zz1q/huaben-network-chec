from flask import Flask, send_from_directory, request, jsonify
import os
import socket
from dns import resolver

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'network_check.html')

@app.route('/get_network_info')
def get_network_info():
    # Get client IP
    client_ip = request.remote_addr
    
    # Get DNS resolution for common domains
    dns_results = {}
    domains = ['www.baidu.com', 'www.qq.com', 'www.aliyun.com']
    
    for domain in domains:
        try:
            answers = resolver.resolve(domain, 'A')
            dns_results[domain] = [str(rdata) for rdata in answers]
        except Exception as e:
            dns_results[domain] = f"解析失败: {str(e)}"
    
    return jsonify({
        'client_ip': client_ip,
        'dns_results': dns_results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
