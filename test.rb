require 'net/http/post/multipart'

def params()
  params = { "id" => "harkame" }
  params = { "pass" => "Palavas34250"}
  params
end

url = URI.parse('https://www5.yggtorrent.pe/user/login')
req = Net::HTTP::Post::Multipart.new(url.path, params())
res = Net::HTTP.start(url.host, url.port) do |http|
  print http.request(req).code
end
