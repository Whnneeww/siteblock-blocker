from http.server import BaseHTTPRequestHandler, HTTPServer 
import urllib.parse 
class MyHandler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        # URLからパラメータを取得 
        parsed_url = urllib.parse.urlparse(self.path) 
        query_params = urllib.parse.parse_qs(parsed_url.query) 
    url = query_params.get('url', [None])[0] 
    if url is None: 
        self.send_error(400, "URLパラメータ 'url' が指定されていません") 
        return 
 
    try: 
        # ファイルを取得 
        with urllib.request.urlopen(url) as response: 
            file_content = response.read().decode('utf-8')  # デコードを追加 
 
        # HTTPレスポンスを設定 
        self.send_response(200) 
        self.send_header('Content-type', 'text/html')  # コンテンツタイプをHTMLに設定 
        self.end_headers() 
 
        # ファイルの内容をHTMLとして送信 
        self.wfile.write(bytes(f"&lt;html&gt;&lt;body&gt;&lt;pre&gt;{file_content}&lt;/pre&gt;&lt;/body&gt;&lt;/html&gt;", 'utf-8')) 
 
    except Exception as e: 
        self.send_error(500, f"ファイルの取得に失敗しました: {e}") 