require 'socket'
require 'time'
require 'rack/utils'

server = TCPServer.open('127.0.0.1', 5678)

# 1
app = Proc.new do |env|
  body = "Hello world!"
  ['200', {'Content-Type' => 'text/html', "Content-Length" => body.length.to_s}, ["Hello world!"]]
end

while connection = server.accept
  # 2
  status, headers, body = app.call({})

  head = "HTTP/1.1 200\r\n" \
  "Date: #{Time.now.httpdate}\r\n" \
  "Status: #{Rack::Utils::HTTP_STATUS_CODES[status]}\r\n" 

  # 3
  headers.each do |k,v|
    head << "#{k}: #{v}\r\n"
  end

  connection.write "#{head}\r\n"

  # 3
  body.each do |part| 
    connection.write part
  end

  body.close if body.respond_to?(:close)

  connection.close 
end
