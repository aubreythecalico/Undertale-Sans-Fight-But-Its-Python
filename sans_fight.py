import os
import sys
import socket
import threading
import http.server
import socketserver

# 1. Ensure dependencies are installed
try:
    import webview
except ImportError:
    print("Required library 'pywebview' is missing. Attempting to install it automatically...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
        import webview
        print("'pywebview' installed successfully!")
    except Exception as e:
        print(f"\nError: Could not install 'pywebview' automatically: {e}")
        print("Please install it manually by running: pip install pywebview")
        input("\nPress Enter to exit...")
        sys.exit(1)

# 2. Change directory to the location of this script to find local assets
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir:
    os.chdir(script_dir)

# 3. Find an available local port
def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

# 4. Custom HTTP handler to bypass potential Windows registry MIME type corruption
class SafeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()



# Force correct mime types to prevent browser blocking due to strict MIME checks
SafeHTTPRequestHandler.extensions_map.update({
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.html': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.json': 'application/json',
    '.wasm': 'application/wasm',
    '.csv': 'text/csv',
})

def main():
    port = get_free_port()
    
    # 5. Start local web server in a background thread
    # Use ThreadingTCPServer or just TCPServer since it's single-user local traffic
    server = socketserver.TCPServer(("127.0.0.1", port), SafeHTTPRequestHandler)
    
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Local server started on http://127.0.0.1:{port}")
    print("Launching Bad Time Simulator desktop window...")
    
    # 6. Launch pywebview desktop window
    try:
        webview.create_window(
            title='Bad Time Simulator (Sans Fight)',
            url=f'http://127.0.0.1:{port}/index.html',
            width=960,
            height=720,
            resizable=True,
            min_size=(640, 480)
        )
        webview.start()
    except Exception as e:
        print(f"Error launching window: {e}")
    finally:
        # 7. Clean up when window is closed
        print("Shutting down local server...")
        server.shutdown()
        server.server_close()
        print("App closed.")

if __name__ == '__main__':
    main()
