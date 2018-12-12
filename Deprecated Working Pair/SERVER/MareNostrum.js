var http = require('http');
var fs = require('fs');
var url = require('url');
var MongoClient = require('mongodb').MongoClient;

var url_db = "mongodb://localhost:27017/";
const querystring = require('querystring');

//Marks?{"subject": "DSBM", "mark": {"$gte":8}}&limit=1
http.createServer( function (request, response) {
    var query = request.url
    console.log("[SRV] Received " + query + " as query.")
    if (query == "/"){
        console.log("[HTM] Response as webpage")
        show_API_info(response)
    }else{
        console.log("[API] Response as API")
        request_db(query, response)
    }
    console.log("[SRV] Done with user\n")
}).listen(8081);

console.log('Server running at http://127.0.0.1:8081/\n');

function show_API_info(response){
    fs.readFile("index.html", function (err, data) {
        if (err) {
            console.log(err);
            response.writeHead(404, {'Content-Type': 'text/html'});
        } else {
            response.writeHead(200, {'Content-Type': 'text/html'});
            response.write(data.toString());
        }
        response.end();
    });
}


function request_db(path, response){
    //var uid= path.split('@')[0];
	var collection = path.split('?')[0]
	var query = JSON.parse('{"uid": "8BBBF395"}');
	console.log(query)
    MongoClient.connect(url_db, { useNewUrlParser: true }, query, collection, function(err, db) {
        if (err) throw err;
        var database = db.db("suparurdinado");
        database.collection(collection).find(query).toArray( function(err, result) {
            if (err) {
                console.log(err);
                response.writeHead(404, {'Content-Type': 'text/html'});
            } else {
                response.writeHead(200, {'Content-Type': 'text/html'});
				console.log(result)
                response.write(JSON.stringify(result));
				console.log(JSON.stringify(result));
            }
            db.close();
            response.end();
        });
    });
}

