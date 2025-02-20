from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import socket
from dns import resolver
import subprocess
import platform

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'network_check.html')

@app.route('/get_network_info')
def get_network_info():
    try:
        # Get client IP
        client_ip = request.remote_addr
        
        # Get DNS resolution for common domains
        dns_results = {}
        domains = ['ihuaben.com', 'www.baidu.com', 'www.qq.com']
        
        for domain in domains:
            try:
                answers = resolver.resolve(domain, 'A')
                dns_results[domain] = [str(rdata) for rdata in answers]
            except Exception as e:
                dns_results[domain] = f"解析失败: {str(e)}"
        
        # 执行 traceroute
        trace_results = []
        target = 'ihuaben.com'
        
        if platform.system().lower() == 'windows':
            cmd = ['tracert', '-h', '30', '-w', '1000', target]
        else:
            cmd = ['traceroute', '-m', '30', '-w', '1', target]
            
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(timeout=30)
            trace_results = output.split('\n')
        except Exception as e:
            trace_results = [f"Traceroute 失败: {str(e)}"]
        
        return jsonify({
            'status': 'success',
            'client_ip': client_ip,
            'dns_results': dns_results,
            'trace_results': trace_results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
