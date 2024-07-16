const http = require('http');
const fs = require('fs');
const urlModule = require('url');
const https = require('https');

http.createServer((req, res) => {
  if (req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/html' });

    if (req.url === '/') {
      fs.readFile('index.html', (err, data) => {
        if (err) {
          res.write('Error reading HTML file');
        } else {
          res.write(data);
        }
        return res.end();
      });
    } else if (req.url.startsWith('/fetch?url=')) {
      const url = urlModule.parse(req.url, true).query.url;

      https.get(url, (remoteRes) => {
        let remoteData = '';

        remoteRes.on('data', (chunk) => {
          remoteData += chunk;
        });

        remoteRes.on('end', () => {
          res.write(remoteData);
          return res.end();
        });
      }).on('error', (e) => {
        res.write(`Error fetching remote file: ${e.message}`);
        return res.end();
      });
    } else {
      res.write('Invalid URL');
      return res.end();
    }
  }
}).listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
