// Import the http module
const http = require('http');

// Create a server object
const server = http.createServer((req, res) => 
{
  // Write a response header
  res.writeHead(200, {'Content-Type': 'text/plain'});
  // Write a response body
  res.end('Hello from Docker!\n');
});

// Listen on port 3000
server.listen(8000, () => 
{
  // Log a message when the server starts
  console.log('Server running at http://localhost:8000/');
});